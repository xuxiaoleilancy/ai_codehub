import pytest
import sys
import platform
import pkg_resources
import numpy as np
import os
import logging
from pathlib import Path
from src.report_generator import TestReportGenerator
import json

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def report_generator():
    return TestReportGenerator()

def test_python_version(report_generator):
    """Test Python version meets requirements"""
    test_results = {
        "python_version": {
            "version": sys.version,
            "meets_requirement": sys.version_info >= (3, 8),
            "required_version": "3.8+"
        }
    }
    report_generator.generate_environment_report(test_results)
    assert sys.version_info >= (3, 8), "Python version should be 3.8 or higher"

def test_required_packages(report_generator):
    """Test all required packages are installed with correct versions"""
    required_packages = {
        'torch': '2.1.1',
        'numpy': '1.24.3',
        'pandas': '2.1.3',
        'fastapi': '0.95.0',
        'pytest': '7.4.3',
        'scikit-learn': '1.3.2'
    }
    
    test_results = {"packages": {}}
    for package, min_version in required_packages.items():
        try:
            pkg_version = pkg_resources.get_distribution(package).version
            meets_requirement = pkg_resources.parse_version(pkg_version) >= pkg_resources.parse_version(min_version)
            test_results["packages"][package] = {
                "installed_version": pkg_version,
                "required_version": min_version,
                "meets_requirement": meets_requirement
            }
            assert meets_requirement, f"{package} version should be {min_version} or higher, got {pkg_version}"
        except Exception as e:
            test_results["packages"][package] = {
                "error": str(e),
                "meets_requirement": False
            }
            raise
    
    report_generator.generate_environment_report(test_results)

def test_system_info(report_generator):
    """Test and record system information"""
    test_results = {
        "system_info": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
            "machine": platform.machine()
        }
    }
    
    # Check memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        test_results["system_info"]["memory"] = {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "free": memory.free
        }
    except ImportError:
        test_results["system_info"]["memory"] = {
            "error": "psutil not installed"
        }
    
    report_generator.generate_environment_report(test_results)

def test_project_structure(report_generator):
    """Test project structure and required directories"""
    required_dirs = [
        'src',
        'src/models',
        'src/api',
        'src/core',
        'src/utils',
        'tests',
        'docs',
        'examples',
        'config'
    ]
    
    test_results = {"project_structure": {}}
    project_root = Path(__file__).parent.parent
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        test_results["project_structure"][dir_path] = {
            "exists": full_path.exists(),
            "is_directory": full_path.is_dir() if full_path.exists() else False
        }
        assert full_path.exists(), f"Required directory {dir_path} not found"
        assert full_path.is_dir(), f"{dir_path} is not a directory"
    
    report_generator.generate_environment_report(test_results)

def test_environment_variables(report_generator):
    """Test environment variables"""
    test_results = {"environment_variables": {}}
    
    # Check for optional environment variables
    env_vars = {
        'CUDA_VISIBLE_DEVICES': 'CUDA device configuration',
        'PYTHONPATH': 'Python path',
        'TORCH_HOME': 'PyTorch home directory',
        'AI_CODEHUB_ENV': 'AI CodeHub environment'
    }
    
    for var, description in env_vars.items():
        value = os.environ.get(var)
        test_results["environment_variables"][var] = {
            "value": value if value else "not set",
            "description": description
        }
    
    report_generator.generate_environment_report(test_results)

def test_generate_chinese_reports(report_generator):
    """测试生成中文测试报告"""
    reports = report_generator.generate_chinese_reports()
    
    # 验证报告文件是否生成
    assert reports["环境报告"].exists()
    assert reports["GPU报告"].exists()
    assert reports["HTML报告"].exists()
    
    # 验证报告内容
    with open(reports["环境报告"], "r", encoding="utf-8") as f:
        env_data = json.load(f)
        assert "系统信息" in env_data
        assert "Python环境" in env_data["测试结果"]
    
    with open(reports["GPU报告"], "r", encoding="utf-8") as f:
        gpu_data = json.load(f)
        assert "GPU信息" in gpu_data
        assert "CUDA可用" in gpu_data["GPU信息"]
    
    with open(reports["HTML报告"], "r", encoding="utf-8") as f:
        html_content = f.read()
        assert "AI CodeHub 测试报告摘要" in html_content
        assert "系统环境信息" in html_content
        assert "GPU信息" in html_content 