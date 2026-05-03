# PortfolioIQ - Setup Instructions

## New Features Implemented

### 1. Profile Settings
- Edit username, full name, and phone number
- Change password with validation
- View account verification status
- OAuth provider information

### 2. Email Verification
- Email verification required for new registrations
- Verification link sent to user's email
- Token-based verification with 1-hour expiry
- Resend verification option

### 3. Enhanced Password Security
- Minimum 8 characters required
- Must include uppercase letter
- Must include lowercase letter
- Must include number
- Must include special character (!@#$%^&*(),.?":{}|<>)
- Real-time password strength indicator
- Visual validation checklist

### 4. Google OAuth Login
- One-click sign-in with Google
- Automatic account creation for new users
- Links Google account to existing email
- Pre-verified email for Google users

### 5. Passkey/WebAuthn Login
- Biometric authentication support
- Register passkeys from profile settings
- Passwordless login option
- Secure hardware-backed authentication

## Setup Instructions

### Backend Setup

1. **Install new dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Update database schema:**
   ```bash
   # The new User model includes additional fields
   # You may need to run migrations or recreate the database
   alembic revision --autogenerate -m "Add email verification and OAuth fields"
   alembic upgrade head
   ```

3. **Configure environment variables:**
   Copy `.env.example` to `.env` and update:
   ```bash
   cp .env.example .env
   ```

   Required configurations:
   - `FRONTEND_URL`: Your frontend URL (default: http://localhost:3000)
   - `SECRET_KEY`: Generate with `openssl rand -hex 32`

   **For Email Verification (Optional but recommended):**
   - `SMTP_HOST`: SMTP server (e.g., smtp.gmail.com)
   - `SMTP_PORT`: SMTP port (e.g., 465)
   - `SMTP_USER`: Your email address
   - `SMTP_PASSWORD`: App password (for Gmail: https://support.google.com/accounts/answer/185833)
   - `SMTP_FROM`: From email address

   **For Google OAuth (Optional):**
   - `GOOGLE_CLIENT_ID`: From Google Cloud Console
   - `GOOGLE_CLIENT_SECRET`: From Google Cloud Console

4. **Start the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Configure environment variables:**
   Update `frontend/.env.local`:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
   ```

2. **Install dependencies (if needed):**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm run dev
   ```

### Google OAuth Setup (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized JavaScript origins: `http://localhost:3000`
   - Authorized redirect URIs: `http://localhost:3000`
5. Copy Client ID and Client Secret
6. Add Client ID to frontend `.env.local`
7. Add both to backend `.env`
pwd: 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
id: 402883753406-d9jtfbb4m1elokj9tbbjjika3jmpcpdo.apps.googleusercontent.com
### Email Configuration (Optional)

**For Gmail:**
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://support.google.com/accounts/answer/185833
3. Use the app password in `SMTP_PASSWORD`

**Development Mode:**
- If SMTP credentials are not configured, verification links will be printed to the console
- You can manually copy the link to verify accounts during development

## Testing the Features

### 1. Test Registration with Email Verification
1. Register a new account
2. Check console output for verification link (if SMTP not configured)
3. Click the verification link
4. Login with verified account

### 2. Test Password Validation
1. Try to register with weak password - should show validation errors
2. Watch the password strength indicator
3. Ensure all requirements are met (8+ chars, uppercase, lowercase, number, symbol)

### 3. Test Google OAuth
1. Click "Continue with Google" button
2. Sign in with Google account
3. Should automatically create account and login

### 4. Test Profile Settings
1. Login to dashboard
2. Click "Profile" button
3. Update username, full name, phone
4. Change password (requires current password)
5. Save changes

### 5. Test Passkey Login (Requires HTTPS in production)
1. Login with regular credentials
2. Go to Profile settings
3. Register a passkey (browser will prompt for biometric/PIN)
4. Logout
5. On login page, enter email and click "Sign in with Passkey"
6. Authenticate with biometric/PIN

## API Endpoints

### New Authentication Endpoints

- `POST /auth/register` - Register with email verification
- `POST /auth/verify-email` - Verify email with token
- `POST /auth/resend-verification` - Resend verification email
- `POST /auth/google` - Google OAuth login
- `GET /auth/me` - Get current user profile
- `PUT /auth/me` - Update user profile
- `POST /auth/passkey/register-begin` - Begin passkey registration
- `POST /auth/passkey/register-complete` - Complete passkey registration
- `POST /auth/passkey/login-begin` - Begin passkey login
- `POST /auth/passkey/login-complete` - Complete passkey login

## Security Notes

1. **Email Verification**: Users must verify email before logging in
2. **Password Requirements**: Enforced on both frontend and backend
3. **OAuth Security**: Google tokens are verified server-side
4. **Passkeys**: Use WebAuthn standard with hardware-backed security
5. **HTTPS Required**: Passkeys require HTTPS in production (localhost works for development)

## Troubleshooting

### Email verification not working
- Check SMTP credentials in `.env`
- Look for verification link in console output (development mode)
- Ensure `FRONTEND_URL` is correct

### Google OAuth not working
- Verify Client ID matches in both frontend and backend
- Check authorized origins in Google Cloud Console
- Ensure Google+ API is enabled

### Passkey not working
- Passkeys require HTTPS (except localhost)
- Check browser compatibility (Chrome, Edge, Safari, Firefox)
- Ensure WebAuthn is supported on your device

### Database errors
- Run migrations: `alembic upgrade head`
- Or recreate database with new schema

## Production Deployment

1. **Use HTTPS** - Required for passkeys and secure cookies
2. **Update CORS** - Configure allowed origins in `backend/app/main.py`
3. **Set strong SECRET_KEY** - Generate with `openssl rand -hex 32`
4. **Configure real SMTP** - Use production email service
5. **Update OAuth redirect URIs** - Add production domain to Google Console
6. **Update environment variables** - Set production URLs and credentials
