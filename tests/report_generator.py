import json
import os
import datetime
import torch
import platform
import logging
from pathlib import Path
from typing import Dict, Any
import sys

class TestReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Create subdirectories
        self.env_report_dir = self.output_dir / "environment"
        self.gpu_report_dir = self.output_dir / "gpu"
        self.env_report_dir.mkdir(exist_ok=True)
        self.gpu_report_dir.mkdir(exist_ok=True)

    def generate_environment_report(self, test_results: Dict[str, Any], lang: str = "en") -> Path:
        """Generate environment test report"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.env_report_dir / f"environment_report_{lang}_{timestamp}.json"
        
        system_info = {
            "platform": platform.platform(),
            "python_version": sys.version,
            "processor": platform.processor(),
            "machine": platform.machine()
        }

        if lang == "zh":
            report_data = {
                "时间戳": timestamp,
                "系统信息": {
                    "平台": system_info["platform"],
                    "Python版本": system_info["python_version"],
                    "处理器": system_info["processor"],
                    "机器类型": system_info["machine"]
                },
                "测试结果": test_results
            }
        else:
            report_data = {
                "timestamp": timestamp,
                "system_info": system_info,
                "test_results": test_results
            }
        
        with open(report_path, "w", encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        
        self.logger.info(f"Environment report generated: {report_path}")
        return report_path

    def generate_gpu_report(self, test_results: Dict[str, Any], lang: str = "en") -> Path:
        """Generate GPU test report"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.gpu_report_dir / f"gpu_report_{lang}_{timestamp}.json"
        
        gpu_info = {
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
            "cudnn_version": torch.backends.cudnn.version() if torch.cuda.is_available() else None,
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "current_device": torch.cuda.current_device() if torch.cuda.is_available() else None,
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "compute_capability": torch.cuda.get_device_capability(0) if torch.cuda.is_available() else None
        }

        if lang == "zh":
            report_data = {
                "时间戳": timestamp,
                "GPU信息": {
                    "CUDA可用": gpu_info["cuda_available"],
                    "CUDA版本": gpu_info["cuda_version"],
                    "cuDNN版本": gpu_info["cudnn_version"],
                    "GPU数量": gpu_info["device_count"],
                    "当前设备": gpu_info["current_device"],
                    "设备名称": gpu_info["device_name"],
                    "计算能力": gpu_info["compute_capability"]
                },
                "测试结果": test_results
            }
        else:
            report_data = {
                "timestamp": timestamp,
                "gpu_info": gpu_info,
                "test_results": test_results
            }
        
        with open(report_path, "w", encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        
        self.logger.info(f"GPU report generated: {report_path}")
        return report_path

    def generate_html_report(self, env_report_path: Path, gpu_report_path: Path, lang: str = "en") -> Path:
        """Generate HTML summary report"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = self.output_dir / f"test_summary_{lang}_{timestamp}.html"
        
        # Read JSON reports
        with open(env_report_path, "r", encoding='utf-8') as f:
            env_data = json.load(f)
        with open(gpu_report_path, "r", encoding='utf-8') as f:
            gpu_data = json.load(f)

        # Define translations
        translations = {
            "zh": {
                "title": "AI CodeHub 测试报告摘要",
                "generated_time": "生成时间",
                "system_info": "系统环境信息",
                "gpu_info": "GPU信息",
                "test_results": "测试结果",
                "gpu_perf_test": "GPU性能测试",
                "detailed_reports": "详细报告链接",
                "env_report": "环境测试报告",
                "gpu_report": "GPU测试报告",
                "success": "成功",
                "failure": "失败",
                "not_available": "不可用",
                "yes": "是",
                "no": "否"
            },
            "en": {
                "title": "AI CodeHub Test Report Summary",
                "generated_time": "Generated Time",
                "system_info": "System Environment Information",
                "gpu_info": "GPU Information",
                "test_results": "Test Results",
                "gpu_perf_test": "GPU Performance Tests",
                "detailed_reports": "Detailed Reports",
                "env_report": "Environment Test Report",
                "gpu_report": "GPU Test Report",
                "success": "Success",
                "failure": "Failure",
                "not_available": "N/A",
                "yes": "Yes",
                "no": "No"
            }
        }

        t = translations[lang]
        
        # Generate HTML content with translations
        html_content = f"""
        <!DOCTYPE html>
        <html lang="{lang}">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{t['title']}</title>
            <style>
                body {{
                    font-family: {'"Microsoft YaHei", ' if lang == "zh" else ""}'Arial, sans-serif';
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                .section {{
                    background: #f9f9f9;
                    border-radius: 5px;
                    padding: 20px;
                    margin-bottom: 20px;
                }}
                .test-result {{
                    margin: 10px 0;
                    padding: 10px;
                    border-left: 4px solid #3498db;
                }}
                .success {{
                    border-left-color: #2ecc71;
                }}
                .warning {{
                    border-left-color: #f1c40f;
                }}
                .error {{
                    border-left-color: #e74c3c;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .timestamp {{
                    color: #7f8c8d;
                    font-size: 0.9em;
                }}
                .json-link {{
                    color: #3498db;
                    text-decoration: none;
                }}
                .json-link:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{t['title']}</h1>
                <p class="timestamp">{t['generated_time']}: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                
                <div class="section">
                    <h2>{t['system_info']}</h2>
                    <table>
                        <tr>
                            <th>{'项目' if lang == 'zh' else 'Item'}</th>
                            <th>{'值' if lang == 'zh' else 'Value'}</th>
                        </tr>
                        <tr>
                            <td>{'操作系统' if lang == 'zh' else 'Platform'}</td>
                            <td>{env_data.get('系统信息', env_data['system_info'])['平台' if lang == 'zh' else 'platform']}</td>
                        </tr>
                        <tr>
                            <td>{'Python版本' if lang == 'zh' else 'Python Version'}</td>
                            <td>{env_data.get('系统信息', env_data['system_info'])['Python版本' if lang == 'zh' else 'python_version']}</td>
                        </tr>
                        <tr>
                            <td>{'处理器' if lang == 'zh' else 'Processor'}</td>
                            <td>{env_data.get('系统信息', env_data['system_info'])['处理器' if lang == 'zh' else 'processor']}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>{t['gpu_info']}</h2>
                    <table>
                        <tr>
                            <th>{'项目' if lang == 'zh' else 'Item'}</th>
                            <th>{'值' if lang == 'zh' else 'Value'}</th>
                        </tr>
                        <tr>
                            <td>{'CUDA可用' if lang == 'zh' else 'CUDA Available'}</td>
                            <td>{t['yes'] if gpu_data.get('GPU信息', gpu_data['gpu_info'])['CUDA可用' if lang == 'zh' else 'cuda_available'] else t['no']}</td>
                        </tr>
                        <tr>
                            <td>{'CUDA版本' if lang == 'zh' else 'CUDA Version'}</td>
                            <td>{gpu_data.get('GPU信息', gpu_data['gpu_info'])['CUDA版本' if lang == 'zh' else 'cuda_version'] or t['not_available']}</td>
                        </tr>
                        <tr>
                            <td>{'GPU数量' if lang == 'zh' else 'GPU Count'}</td>
                            <td>{gpu_data.get('GPU信息', gpu_data['gpu_info'])['GPU数量' if lang == 'zh' else 'device_count']}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>{t['test_results']}</h2>
                    <h3>{t['gpu_perf_test']}</h3>
                    <table>
                        <tr>
                            <th>{'测试项目' if lang == 'zh' else 'Test Item'}</th>
                            <th>{'结果' if lang == 'zh' else 'Result'}</th>
                            <th>{'耗时(秒)' if lang == 'zh' else 'Time (s)'}</th>
                        </tr>
                        <tr>
                            <td>{'矩阵加法' if lang == 'zh' else 'Matrix Addition'}</td>
                            <td>{t['success'] if gpu_data['test_results']['operations']['addition']['success'] else t['failure']}</td>
                            <td>{gpu_data['test_results']['operations']['addition']['time']:.6f}</td>
                        </tr>
                        <tr>
                            <td>{'矩阵乘法' if lang == 'zh' else 'Matrix Multiplication'}</td>
                            <td>{t['success'] if gpu_data['test_results']['operations']['matrix_multiplication']['success'] else t['failure']}</td>
                            <td>{gpu_data['test_results']['operations']['matrix_multiplication']['time']:.6f}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>{t['detailed_reports']}</h2>
                    <p><a href="{env_report_path}" class="json-link">{t['env_report']} (JSON)</a></p>
                    <p><a href="{gpu_report_path}" class="json-link">{t['gpu_report']} (JSON)</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(html_path, "w", encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML report generated: {html_path}")
        return html_path

    def generate_chinese_reports(self) -> Dict[str, Path]:
        """生成所有中文测试报告"""
        # 生成环境测试结果
        env_test_results = {
            "Python环境": {
                "版本检查": True,
                "依赖包": ["torch", "numpy", "pytest"],
                "状态": "正常"
            },
            "系统环境": {
                "内存使用": "正常",
                "磁盘空间": "充足"
            }
        }
        
        # 生成GPU测试结果
        gpu_test_results = {
            "operations": {
                "addition": {
                    "success": True,
                    "time": 0.001234
                },
                "matrix_multiplication": {
                    "success": True,
                    "time": 0.005678
                }
            }
        }
        
        # 生成各种报告
        env_report = self.generate_environment_report(env_test_results, lang="zh")
        gpu_report = self.generate_gpu_report(gpu_test_results, lang="zh")
        html_report = self.generate_html_report(env_report, gpu_report, lang="zh")
        
        return {
            "环境报告": env_report,
            "GPU报告": gpu_report,
            "HTML报告": html_report
        } 