from setuptools import setup, find_packages

setup(
    name="hipaa-training-system",
    version="3.0.0",
    author="Your Name",
    author_email="your@email.com",
    description="HIPAA Training System for Pharmacy Staff",
    packages=find_packages(include=["hipaa_training", "hipaa_training.*"]),
    include_package_data=True,
    install_requires=[
        "cryptography>=42.0.0",
        "pytest>=8.0.0",
        "sqlalchemy>=1.4.23",
        "python-dotenv>=0.19.0",
        "rich>=12.5.1",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
