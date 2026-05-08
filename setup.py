from setuptools import setup, find_packages

setup(
    name="sbic-tracker",
    version="0.1.0",
    description="SBIC investment portfolio analyzer — fund-level IRR/TVPI/DPI, licensee tracking, and SBA program data analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jay Patel",
    author_email="thejaypatel1511@gmail.com",
    url="https://github.com/Jaypatel1511/sbic-tracker",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
)
