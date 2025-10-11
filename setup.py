from setuptools import setup, find_packages

setup(
    name="hipaa_training",
    version="3.0.0",
    author="Israa Ali",
    author_email="israaali2019@yahoo.com",
    description="HIPAA Training System for Pharmacy Staff (V3.0)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Saranoah/HIPAA-Training-System-for-Pharmacy-Staff-V3.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cryptography>=3.4.8",
        "sqlalchemy>=1.4.23",
        "alembic>=1.7.1",
        "python-dotenv>=0.19.0",
        "python-dateutil>=2.8.2",
        "psycopg2-binary>=2.9.3",
        "colorama>=0.4.4",
        "rich>=12.5.1",
        "speechrecognition>=3.8.1",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "hipaa-training=main:setup_production_environment",
        ],
    },
)

