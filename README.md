# AI CodeHub

AI CodeHub is a comprehensive platform for AI code generation and project management, built with FastAPI and React.

## Features

- Support for multiple AI models (GPT-4, Claude, Gemini, etc.)
- Code generation and project management
- User authentication and authorization
- Multi-language support (English/Chinese)
- Responsive design with mobile support
- Real-time navigation bar state management
- Secure logout functionality

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- SQLite Database

### Frontend
- React
- Tailwind CSS
- i18next Internationalization
- Axios HTTP Client
- Event delegation for dynamic elements
- Local storage for state management

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run backend service:
```bash
uvicorn src.main:app --reload
```

### Frontend Setup
1. Install dependencies:
```bash
cd static
npm install
```

2. Run development server:
```bash
npm run dev
```

## Testing

The project uses pytest for both unit tests and API tests.

### Running Tests
```bash
pytest
```

### Test Coverage
- User authentication (registration, login, token validation)
- API endpoint access control
- Database operations
- Error handling
- Navigation bar state management
- Logout functionality

### Test Database
Tests use an in-memory SQLite database, which is automatically created and cleaned up before and after each test case.

## API Documentation

After starting the service, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
ai_codehub/
├── src/
│   ├── main.py              # Application entry point
│   ├── database/            # Database configuration and models
│   ├── api/                 # API routes
│   │   ├── routers/        # API route handlers
│   │   │   ├── auth.py     # Authentication routes
│   │   │   ├── model_router.py  # Model management routes
│   │   │   └── project_router.py # Project management routes
│   ├── core/                # Core configuration and utilities
│   └── services/            # Business logic
├── static/                  # Frontend code
│   ├── components/          # React components
│   │   └── navbar.html     # Navigation bar component
│   ├── js/                 # JavaScript files
│   │   ├── common.js       # Common utilities
│   │   ├── locales.js      # Internationalization
│   │   └── i18n.js         # i18n configuration
│   ├── index.html          # Main page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── models.html         # Models page
│   ├── projects.html       # Projects page
│   └── profile.html        # User profile page
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Recent Updates

### v0.1.0
- Added secure logout functionality
- Improved navigation bar state management
- Enhanced user authentication flow
- Fixed API endpoint validation
- Added profile page
- Improved error handling
- Enhanced internationalization support

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
