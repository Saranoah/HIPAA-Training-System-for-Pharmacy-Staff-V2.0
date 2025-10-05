from setuptools import setup

setup(
    name="hipaa-training-system",
    version="2.0.0",
    description="Comprehensive HIPAA training for pharmacy staff",
    author="Your Name",
    py_modules=["hipaa_training_v2"],
    entry_points={
        'console_scripts': [
            'hipaa-train=hipaa_training_v2:main',
        ],
    },
    python_requires=">=3.6",
)
