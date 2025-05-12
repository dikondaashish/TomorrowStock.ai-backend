import os
import json
import firebase_admin
from firebase_admin import auth as fb_auth, credentials
from fastapi import Depends, HTTPException, Header
import logging
from app.core.config import settings

# Initialize Firebase Admin SDK
try:
    # Secure way to handle Firebase credentials
    # In production, use environment variables as shown in the original code
    # For development, we can use a json file that's excluded from version control
    
    # Create credentials directory if it doesn't exist
    os.makedirs('credentials', exist_ok=True)
    
    # Check if credentials file exists, if not create it
    cred_file = 'credentials/firebase-credentials.json'
    if not os.path.exists(cred_file):
        with open(cred_file, 'w') as f:
            json.dump({
                "type": "service_account",
                "project_id": settings.FIREBASE_PROJECT_ID,
                "private_key_id": "2aecae3a4c25ad75aaf1dd94111423b01559f92f",
                "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
                "client_email": settings.FIREBASE_CLIENT_EMAIL,
                "client_id": "100921287202914034152",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{settings.FIREBASE_CLIENT_EMAIL.replace('@', '%40')}",
                "universe_domain": "googleapis.com"
            }, f, indent=2)
        
        # Add credentials directory to .gitignore
        gitignore_path = '.gitignore'
        with open(gitignore_path, 'a+') as f:
            f.seek(0)
            content = f.read()
            if 'credentials/' not in content:
                f.write('\n# Credentials\ncredentials/\n')
    
    # Initialize Firebase with the credentials file
    cred = credentials.Certificate(cred_file)
    firebase_admin.initialize_app(cred)
    logging.info("Firebase Admin SDK initialized successfully with credentials file")
except Exception as e:
    logging.error(f"Error initializing Firebase Admin SDK: {e}")
    # Continue without crashing - we'll handle auth failures at runtime

async def get_current_user(authorization: str = Header(...)):
    """
    Firebase authentication middleware.
    Verifies the Firebase ID token and returns user info.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials. Bearer token required."
        )
    
    token = authorization.removeprefix("Bearer ").strip()
    
    try:
        decoded = fb_auth.verify_id_token(token)
        return decoded  # contains uid, email, etc.
    except Exception as e:
        logging.error(f"Firebase authentication error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        ) 