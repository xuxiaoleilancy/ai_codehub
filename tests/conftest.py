import pytest
import torch
import logging
import sys
import platform
import os
import subprocess
from pathlib import Path

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def get_gpu_info():
    """Get detailed GPU information"""
    gpu_info = {}
    try:
        # Try to get nvidia-smi info
        result = subprocess.run(['nvidia-smi', '--query-gpu=gpu_name,memory.total,memory.free,memory.used,driver_version', '--format=csv,noheader,nounits'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            info = result.stdout.strip().split(',')
            gpu_info['nvidia_smi'] = {
                'gpu_name': info[0].strip(),
                'total_memory': int(info[1]),
                'free_memory': int(info[2]),
                'used_memory': int(info[3]),
                'driver_version': info[4].strip()
            }
    except Exception as e:
        logger.warning(f"Failed to get nvidia-smi info: {e}")
    
    # Get PyTorch GPU info
    if torch.cuda.is_available():
        gpu_info['pytorch'] = {
            'cuda_version': torch.version.cuda,
            'cudnn_version': torch.backends.cudnn.version(),
            'device_count': torch.cuda.device_count(),
            'current_device': torch.cuda.current_device(),
            'device_name': torch.cuda.get_device_name(),
            'compute_capability': torch.cuda.get_device_capability()
        }
    
    return gpu_info

def pytest_configure(config):
    """
    Called before test collection, perform initial checks
    """
    logger.info("Running initial environment checks...")
    
    # Check Python version
    py_version = sys.version_info
    logger.info(f"Python version: {sys.version}")
    if py_version < (3, 8):
        logger.warning("Python version below 3.8 may not be fully supported")
    
    # Check system information
    logger.info(f"Operating System: {platform.system()} {platform.version()}")
    logger.info(f"Machine: {platform.machine()}")
    
    # Check GPU information
    gpu_info = get_gpu_info()
    if gpu_info.get('nvidia_smi'):
        logger.info("\nNVIDIA GPU Information:")
        for key, value in gpu_info['nvidia_smi'].items():
            logger.info(f"{key}: {value}")
    
    if gpu_info.get('pytorch'):
        logger.info("\nPyTorch GPU Information:")
        for key, value in gpu_info['pytorch'].items():
            logger.info(f"{key}: {value}")
    else:
        logger.warning("CUDA not available - running on CPU only")

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    # Create temporary test directory
    test_dir = Path("test_tmp")
    test_dir.mkdir(exist_ok=True)
    
    # Set environment variables for testing
    os.environ["AI_CODEHUB_ENV"] = "test"
    os.environ["AI_CODEHUB_TEST_DIR"] = str(test_dir)
    
    # Get GPU information
    gpu_info = get_gpu_info()
    if gpu_info.get('pytorch'):
        # Set CUDA device if multiple GPUs available
        if gpu_info['pytorch']['device_count'] > 1:
            # Use the first GPU for testing
            torch.cuda.set_device(0)
            logger.info(f"Using GPU 0: {torch.cuda.get_device_name(0)}")
    
    # Set random seed for reproducibility
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(42)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    yield
    
    # Cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Remove temporary test directory
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)

@pytest.fixture(scope="session")
def test_device():
    """Provide test device (CPU/CUDA) for tests"""
    if torch.cuda.is_available():
        # Get GPU memory info
        current_device = torch.cuda.current_device()
        total_memory = torch.cuda.get_device_properties(current_device).total_memory
        logger.info(f"Using GPU {current_device} with {total_memory / 1024**3:.2f} GB memory")
        return torch.device("cuda")
    return torch.device("cpu")

@pytest.fixture(scope="session")
def project_root():
    """Provide project root directory"""
    return Path(__file__).parent.parent 