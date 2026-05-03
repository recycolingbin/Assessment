from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import json

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin, EmailVerification, GoogleAuthRequest, UserUpdate, ForgotPasswordRequest, ResetPasswordRequest
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from app.utils.email import generate_verification_token, verify_token, send_verification_email, generate_reset_token, verify_reset_token, send_password_reset_email
from app.utils.oauth import verify_google_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Generate verification token
    verification_token = generate_verification_token(user.email)

    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_verified=False,
        verification_token=verification_token,
        verification_token_expires=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send verification email (don't fail if email sending fails)
    try:
        send_verification_email(user.email, verification_token)
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        # Continue anyway - user is created and token is saved

    return new_user

@router.post("/verify-email")
def verify_email(verification: EmailVerification, db: Session = Depends(get_db)):
    # Verify token
    email = verify_token(verification.token, max_age=3600)  # 1 hour expiry
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    # Update user
    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    db.commit()

    return {"message": "Email verified successfully"}

@router.post("/resend-verification")
def resend_verification(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    # Generate new token
    verification_token = generate_verification_token(email)
    user.verification_token = verification_token
    user.verification_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    # Send email (don't fail if email sending fails)
    try:
        send_verification_email(email, verification_token)
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        # Continue anyway - token is saved in database

    return {"message": "Verification email sent"}

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if email is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/google", response_model=Token)
async def google_auth(auth_request: GoogleAuthRequest, db: Session = Depends(get_db)):
    # Verify Google token
    user_info = await verify_google_token(auth_request.credential)

    # Check if user exists
    user = db.query(User).filter(User.google_id == user_info['google_id']).first()

    if not user:
        # Check if email already exists
        user = db.query(User).filter(User.email == user_info['email']).first()
        if user:
            # Link Google account to existing user
            user.google_id = user_info['google_id']
            user.oauth_provider = 'google'
            user.is_verified = True  # Google emails are pre-verified
            if not user.full_name and user_info.get('name'):
                user.full_name = user_info['name']
            if not user.avatar_url and user_info.get('picture'):
                user.avatar_url = user_info['picture']
        else:
            # Create new user
            username = user_info['email'].split('@')[0]
            # Ensure unique username
            base_username = username
            counter = 1
            while db.query(User).filter(User.username == username).first():
                username = f"{base_username}{counter}"
                counter += 1

            user = User(
                email=user_info['email'],
                username=username,
                google_id=user_info['google_id'],
                oauth_provider='google',
                is_verified=True,
                full_name=user_info.get('name'),
                avatar_url=user_info.get('picture')
            )
            db.add(user)

        db.commit()
        db.refresh(user)

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Update username if provided
    if user_update.username and user_update.username != current_user.username:
        # Check if username is taken
        existing = db.query(User).filter(User.username == user_update.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = user_update.username

    # Update profile fields
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.phone is not None:
        current_user.phone = user_update.phone

    # Update password if provided
    if user_update.new_password:
        if not user_update.current_password:
            raise HTTPException(status_code=400, detail="Current password required to set new password")

        # Verify current password
        if not current_user.hashed_password or not verify_password(user_update.current_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        # Set new password
        current_user.hashed_password = get_password_hash(user_update.new_password)

    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Password Reset endpoints
@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset email"""
    user = db.query(User).filter(User.email == request.email).first()

    # Always return success to prevent email enumeration
    if not user:
        return {"message": "If the email exists, a password reset link has been sent"}

    # Don't allow password reset for OAuth users without password
    if not user.hashed_password:
        return {"message": "If the email exists, a password reset link has been sent"}

    # Generate reset token
    reset_token = generate_reset_token(user.email)
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    # Send reset email (don't fail if email sending fails)
    try:
        send_password_reset_email(user.email, reset_token)
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
        # Continue anyway - token is saved in database

    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password with token"""
    # Verify token
    email = verify_reset_token(request.token, max_age=3600)  # 1 hour expiry
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if token matches
    if user.reset_token != request.token:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    # Check if token is expired
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token has expired")

    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()

    return {"message": "Password reset successfully"}
