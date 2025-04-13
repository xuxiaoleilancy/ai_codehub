#!/usr/bin/env python
import os
import sys
import glob
import json
from pathlib import Path
from datetime import datetime

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.report_generator import TestReportGenerator

def get_latest_report(directory, pattern):
    """Get the latest report file from the specified directory"""
    files = glob.glob(str(Path(directory) / pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def main():
    """Generate HTML report from the latest environment and GPU test results"""
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Get the latest environment and GPU reports
    env_report = get_latest_report("reports/environment", "environment_report_*.json")
    gpu_report = get_latest_report("reports/gpu", "gpu_report_*.json")
    
    if not env_report or not gpu_report:
        print("Error: Could not find required report files.")
        print(f"Environment report found: {env_report}")
        print(f"GPU report found: {gpu_report}")
        sys.exit(1)
    
    try:
        # Create report generator instance
        report_generator = TestReportGenerator()
        
        # Generate HTML report
        html_report = report_generator.generate_html_report(
            Path(env_report),
            Path(gpu_report)
        )
        
        print("\nReport generation completed successfully!")
        print(f"Environment report: {env_report}")
        print(f"GPU report: {gpu_report}")
        print(f"HTML report: {html_report}")
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 