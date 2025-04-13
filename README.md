# AI CodeHub

AI CodeHub is a structured platform for managing and sharing AI-related code and projects.

## Features

- User Authentication & Authorization
  - User registration and login
  - JWT token authentication
  - Role-based access control (User/Superuser)

- Project Management
  - Create and manage projects
  - Project descriptions and metadata
  - Project access control

- Model Management
  - Model upload and version control
  - Model metadata management
  - Support for multiple model types (Classification/Regression/Generative)
  - Model status tracking (Draft/Training/Ready/Error)

- GPU Support
  - CUDA device detection
  - GPU memory management
  - Model GPU acceleration

- Testing and Reporting
  - Environment testing
  - GPU detection tests
  - HTML and JSON format test reports
  - Automated testing framework

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

3. Initialize the database:
```bash
python -m src.database.init_db
```

4. Start the server:
```bash
uvicorn src.main:app --reload
```

5. Access the application:
- Open your browser and visit http://localhost:8000
- Default superuser credentials:
  - Username: admin
  - Password: admin123

## API Documentation

After starting the server, view the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Main API endpoints:
- `/api/auth/*` - Authentication related
- `/api/v1/models/*` - Model management
- `/api/projects/*` - Project management

## System Requirements

- Python 3.8 or higher
- SQLite 3
- CUDA toolkit (optional, for GPU support)
- Other dependencies in requirements.txt

## Testing

Run tests:
```bash
python -m pytest tests/ -v
```

Test reports are located in the `reports/` directory:
- `reports/environment/` - Environment test reports
- `reports/gpu/` - GPU test reports
- `reports/summary.html` - Test summary report

## Directory Structure

```
ai_codehub/
├── src/
│   ├── api/            - API routes and handlers
│   ├── core/           - Core functionality and config
│   ├── database/       - Database models and config
│   ├── models/         - Model management code
│   └── static/         - Static files
├── tests/              - Test code
├── reports/            - Test reports
├── requirements.txt    - Project dependencies
└── README.md          - Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
