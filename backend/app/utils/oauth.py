from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException
import os
import httpx

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

oauth = OAuth()

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

async def verify_google_token(token: str) -> dict:
    """Verify Google ID token and return user info"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            )
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid Google token")

            user_info = response.json()

            # Verify the token is for our app
            if GOOGLE_CLIENT_ID and user_info.get('aud') != GOOGLE_CLIENT_ID:
                raise HTTPException(status_code=400, detail="Token not for this application")

            return {
                'google_id': user_info.get('sub'),
                'email': user_info.get('email'),
                'email_verified': user_info.get('email_verified', False),
                'name': user_info.get('name'),
                'picture': user_info.get('picture')
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Error verifying Google token: {str(e)}")
