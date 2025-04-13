import pytest
import torch
import logging
import subprocess
import re
import time
from typing import Dict, List, Optional
from src.report_generator import TestReportGenerator

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def report_generator():
    return TestReportGenerator()

def get_nvidia_smi_info() -> Dict:
    """Get NVIDIA GPU information using nvidia-smi"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=gpu_name,memory.total,memory.free,memory.used,driver_version', '--format=csv,noheader,nounits'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            gpu_info = result.stdout.strip().split(',')
            return {
                'gpu_name': gpu_info[0].strip(),
                'total_memory': int(gpu_info[1]),
                'free_memory': int(gpu_info[2]),
                'used_memory': int(gpu_info[3]),
                'driver_version': gpu_info[4].strip()
            }
    except Exception as e:
        logger.warning(f"Failed to get nvidia-smi info: {e}")
    return {}

def get_cuda_version() -> Optional[str]:
    """Get CUDA version from nvcc"""
    try:
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_match = re.search(r'release (\d+\.\d+)', result.stdout)
            if version_match:
                return version_match.group(1)
    except Exception as e:
        logger.warning(f"Failed to get CUDA version: {e}")
    return None

def test_gpu_availability(report_generator):
    """Test basic GPU availability"""
    test_results = {
        "cuda_available": torch.cuda.is_available(),
        "pytorch_cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
        "cudnn_version": torch.backends.cudnn.version() if torch.cuda.is_available() else None
    }
    
    report_generator.generate_gpu_report(test_results)
    
    if not test_results["cuda_available"]:
        pytest.skip("CUDA not available")

def test_gpu_count(report_generator):
    """Test number of available GPUs"""
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    
    test_results = {
        "device_count": torch.cuda.device_count(),
        "devices": []
    }
    
    for i in range(torch.cuda.device_count()):
        device_info = {
            "device_id": i,
            "device_name": torch.cuda.get_device_name(i),
            "compute_capability": torch.cuda.get_device_capability(i),
            "total_memory": torch.cuda.get_device_properties(i).total_memory
        }
        test_results["devices"].append(device_info)
    
    report_generator.generate_gpu_report(test_results)
    assert test_results["device_count"] > 0, "No GPUs found"

def test_gpu_memory(report_generator):
    """Test GPU memory information"""
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    
    test_results = {"memory_info": {}}
    
    # Get PyTorch GPU memory info
    current_device = torch.cuda.current_device()
    test_results["memory_info"]["pytorch"] = {
        "total_memory": torch.cuda.get_device_properties(current_device).total_memory,
        "allocated_memory": torch.cuda.memory_allocated(current_device),
        "cached_memory": torch.cuda.memory_reserved(current_device)
    }
    
    # Get nvidia-smi info
    nvidia_info = get_nvidia_smi_info()
    if nvidia_info:
        test_results["memory_info"]["nvidia_smi"] = nvidia_info
    
    report_generator.generate_gpu_report(test_results)

def test_gpu_compute_capability():
    """Test GPU compute capability"""
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    
    current_device = torch.cuda.current_device()
    compute_capability = torch.cuda.get_device_capability(current_device)
    logger.info(f"GPU {current_device} Compute Capability: {compute_capability[0]}.{compute_capability[1]}")
    
    # Check if compute capability meets minimum requirements
    assert compute_capability >= (3, 5), "GPU compute capability below minimum requirement (3.5)"

def test_gpu_performance(report_generator):
    """Test basic GPU performance"""
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    
    test_results = {"performance": {}}
    
    # Test matrix multiplication
    sizes = [(1000, 1000), (2000, 2000)]
    for size in sizes:
        x = torch.randn(size, device='cuda')
        y = torch.randn(size, device='cuda')
        
        # Time matrix multiplication
        start_time = time.time()
        z = torch.matmul(x, y)
        torch.cuda.synchronize()
        elapsed_time = time.time() - start_time
        
        test_results["performance"][f"matmul_{size[0]}x{size[1]}"] = {
            "time": elapsed_time,
            "size": size
        }
    
    report_generator.generate_gpu_report(test_results)

def test_cuda_toolkit():
    """Test CUDA toolkit installation"""
    cuda_version = get_cuda_version()
    if cuda_version:
        logger.info(f"CUDA Toolkit Version: {cuda_version}")
        # Check if CUDA version matches PyTorch CUDA version
        if torch.cuda.is_available():
            torch_cuda_version = torch.version.cuda
            assert cuda_version.startswith(torch_cuda_version), \
                f"CUDA toolkit version ({cuda_version}) does not match PyTorch CUDA version ({torch_cuda_version})"
    else:
        logger.warning("CUDA toolkit not found or nvcc not in PATH")

def test_gpu_operations(report_generator):
    """Test various GPU operations"""
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    
    test_results = {"operations": {}}
    
    # Test tensor operations
    x = torch.randn(100, 100, device='cuda')
    y = torch.randn(100, 100, device='cuda')
    
    # Test basic operations
    start_time = time.time()
    z = x + y
    torch.cuda.synchronize()
    add_time = time.time() - start_time
    
    # Test matrix operations
    start_time = time.time()
    w = torch.matmul(x, y)
    torch.cuda.synchronize()
    matmul_time = time.time() - start_time
    
    test_results["operations"] = {
        "addition": {
            "time": add_time,
            "success": z.device.type == 'cuda'
        },
        "matrix_multiplication": {
            "time": matmul_time,
            "success": w.device.type == 'cuda'
        }
    }
    
    # Test memory management
    del x, y, z, w
    torch.cuda.empty_cache()
    allocated = torch.cuda.memory_allocated()
    test_results["operations"]["memory_management"] = {
        "allocated_after_cleanup": allocated,
        "success": allocated == 0
    }
    
    report_generator.generate_gpu_report(test_results) 