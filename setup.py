from setuptools import setup, find_packages

setup(
    name="ai_codehub",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "numpy",
        "pytest",
    ],
    python_requires=">=3.8",
) 