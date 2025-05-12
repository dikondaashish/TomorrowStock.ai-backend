# Stock Predictor Backend

A FastAPI backend for stock price prediction.

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure environment variables in a `.env` file:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   FIREBASE_PROJECT_ID=your-firebase-project
   FIREBASE_CLIENT_EMAIL=your-client-email@example.com
   FIREBASE_PRIVATE_KEY=your-private-key-here
   API_PORT=8000
   API_HOST=0.0.0.0
   DEBUG=True
   ```
5. Run the server:
   ```
   python run.py
   ```

## Security

**IMPORTANT**: This project uses sensitive authentication credentials that should never be committed to version control.

- **Firebase credentials**: The app uses a Firebase credentials file that is stored in the `credentials/` directory, which is excluded from Git via `.gitignore`.
- **Environment variables**: Sensitive information should be stored in the `.env` file, which is also excluded from Git.
- **Private keys**: Never hardcode private keys or sensitive credentials in your application code or commit them to Git.

For production deployments, use secure environment variable services provided by your hosting platform.

## Authentication

This API uses Firebase authentication. To access protected endpoints:

1. Obtain a Firebase ID token for your user
2. Include the token in requests with the `Authorization` header:
   ```
   Authorization: Bearer <your-firebase-token>
   ```

## API Documentation

Once the server is running, you can access:
- API documentation at: http://localhost:8000/docs
- Alternative documentation at: http://localhost:8000/redoc

## Development

### Linting and Formatting

The project uses flake8, black, and isort for code quality:

```
# Run all linting and formatting tools
./scripts/lint.sh

# Or run them individually
isort .    # Sort imports
black .    # Format code
flake8 .   # Check for code quality issues
```

## Project Structure

```
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── auth.py
│   │   │   ├── health.py
│   │   │   └── prediction.py
│   │   └── api.py
│   ├── core
│   │   └── config.py
│   ├── models
│   ├── schemas
│   │   └── prediction.py
│   ├── db.py
│   ├── firebase_auth.py
│   ├── predictor.py
│   ├── sentiment.py
│   └── main.py
├── credentials       # Contains Firebase credentials (git-ignored)
├── scripts
│   └── lint.sh
├── run.py
├── main.py
├── requirements.txt
├── .flake8
├── pyproject.toml
└── .gitignore
``` 