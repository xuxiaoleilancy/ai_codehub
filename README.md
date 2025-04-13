# AI CodeHub

AI CodeHub is a comprehensive platform for managing, sharing, and collaborating on AI-related code and projects. This framework provides a structured environment for AI development, experimentation, and deployment.

## Project Structure

```
ai_codehub/
├── src/                    # Source code directory
│   ├── core/              # Core functionality
│   ├── models/            # AI model implementations
│   ├── utils/             # Utility functions
│   └── api/               # API endpoints
├── tests/                 # Test files
│   ├── conftest.py        # Test configuration
│   ├── test_model_manager.py  # Model manager tests
│   ├── test_environment.py    # Environment tests
│   └── test_gpu_environment.py # GPU environment tests
├── docs/                  # Documentation
├── examples/              # Example implementations
├── requirements.txt       # Python dependencies
└── config/               # Configuration files
```

## Features

- Model Management: Organize and version control AI models
- Experiment Tracking: Log and monitor experiments
- Code Sharing: Share and collaborate on AI projects
- API Integration: Easy integration with various AI services
- Documentation: Comprehensive documentation and examples
- GPU Support: Automatic GPU detection and utilization
- Testing: Comprehensive test suite with pytest

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the development server: `python src/main.py`

## GPU Support

The framework provides comprehensive GPU support and environment detection:

### GPU Requirements
- NVIDIA GPU with CUDA support
- NVIDIA drivers installed
- CUDA toolkit installed
- cuDNN installed
- PyTorch with CUDA support

### GPU Environment Detection
The framework automatically detects and tests:
- GPU availability and count
- GPU memory and compute capability
- CUDA version compatibility
- Driver version
- Performance benchmarks

## Testing

The project uses pytest for testing. To run the tests:

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-xdist

# Run all tests
pytest tests/

# Run tests with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_model_manager.py

# Run GPU environment tests
pytest tests/test_gpu_environment.py -v

# Run tests in parallel
pytest -n auto tests/
```

### Test Coverage

#### Environment Tests
- Python version compatibility
- Package dependencies
- System resources
- File system permissions
- Environment variables

#### GPU Tests
- GPU availability and count
- GPU memory information
- Compute capability
- CUDA toolkit version
- Performance benchmarks
- Basic operations
- Memory management

#### Model Tests
- Model saving and loading
- Metadata management
- Error handling
- Model listing

## Test Report Generation

The framework automatically generates comprehensive test reports in both JSON and HTML formats. Reports are stored in the `reports` directory with the following structure:

```
reports/
├── environment/          # Environment test reports
├── gpu/                 # GPU test reports
└── test_summary_*.html  # HTML summary reports
```

### Report Types

1. **Environment Reports** (`reports/environment/`)
   - System information
   - Python version
   - Package dependencies
   - System resources
   - Environment variables
   - Test results

2. **GPU Reports** (`reports/gpu/`)
   - GPU availability
   - CUDA version
   - GPU count and memory
   - Compute capability
   - Performance benchmarks
   - Test results

3. **HTML Summary Reports** (`reports/test_summary_*.html`)
   - Combined view of all test results
   - System and GPU information
   - Performance metrics
   - Links to detailed JSON reports
   - Available in both English and Chinese

### Generating Reports

Reports are automatically generated when running tests. To generate reports manually:

```bash
# Generate all reports
python -m pytest tests/ -v

# Generate reports for specific test file
python -m pytest tests/test_environment.py -v
python -m pytest tests/test_gpu_environment.py -v
```

### Report Features

- **Timestamps**: Each report includes generation timestamp
- **Bilingual Support**: Reports available in English and Chinese
- **Detailed Information**: Comprehensive system and test data
- **Performance Metrics**: GPU performance benchmarks
- **Easy Navigation**: HTML reports with links to detailed JSON data
- **Absolute Paths**: All report links use absolute paths for easy access

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
- CUDA support (optional, for GPU acceleration)
  - NVIDIA GPU with CUDA support
  - NVIDIA drivers
  - CUDA toolkit
  - cuDNN

## License

MIT License
