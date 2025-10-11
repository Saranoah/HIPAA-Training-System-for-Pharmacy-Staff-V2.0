from setuptools import setup, find_packages

setup(
    name="hipaa-training-system",
    version="3.0.0",
    author="Israa Ali",
    author_email="israaali2019@yahoo.com",
    description="HIPAA Training System for Pharmacy Staff — secure, interactive, and production-ready.",
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
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
        "flake8>=6.0.0",
        "bandit>=1.7.5",
    ],
    python_requires=">=3.8",
)

