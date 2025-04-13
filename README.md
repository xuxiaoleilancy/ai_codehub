# AI CodeHub

A platform for managing and sharing AI-related code and projects.

## Features

- Model Management
  - Upload and manage AI models
  - Version control for models
  - Model metadata management
  - GPU support for model operations

- User Authentication
  - User registration and login
  - Token-based authentication
  - User profile management
  - Role-based access control

- Modern Web Interface
  - Responsive design
  - User-friendly forms
  - Real-time feedback
  - Clean and modern UI

## Project Structure

```
ai_codehub/
├── config/             # Configuration files
├── docs/              # Documentation
├── examples/          # Example code and usage
├── reports/           # Test and environment reports
├── scripts/           # Utility scripts
├── src/               # Source code
│   ├── api/           # API endpoints
│   ├── core/          # Core functionality
│   ├── database/      # Database models and schemas
│   └── models/        # Model management
├── static/            # Frontend assets
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript files
│   └── index.html    # Main HTML page
├── tests/             # Test files
└── requirements.txt   # Python dependencies
```

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai_codehub.git
cd ai_codehub
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python -m uvicorn src.main:app --reload
```

4. Open your browser and visit:
```
http://localhost:8000
```

## Authentication

The platform uses JWT (JSON Web Tokens) for authentication. To use the API:

1. Register a new user:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "user", "email": "user@example.com", "password": "password"}'
```

2. Login to get access token:
```bash
curl -X POST "http://localhost:8000/api/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user&password=password"
```

3. Use the token in subsequent requests:
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
     -H "Authorization: Bearer your_access_token"
```

## GPU Support

The platform automatically detects and utilizes available GPU resources for model operations. To check GPU status:

1. Run the environment tests:
```bash
python -m pytest tests/test_environment.py -v
```

2. Check the generated reports in the `reports/` directory

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Test reports will be generated in the `reports/` directory, including:
- Environment test results
- GPU detection results
- Test coverage reports

## Requirements

- Python 3.8 or higher
- FastAPI
- SQLAlchemy
- PyTorch (for GPU support)
- Modern web browser

## License

This project is licensed under the MIT License - see the LICENSE file for details.
