# setup.py
from setuptools import setup, find_packages
setup(
    name="hipaa-training-system",
    version="2.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["Flask==3.0.0", "Werkzeug==3.0.1"],
)
