from setuptools import setup, find_packages

setup(
    name="sbic-tracker",
    version="0.2.0",
    description="UNMAINTAINED. SBIC investment portfolio analyzer — fund-level IRR/TVPI/DPI and licensee modeling. Live SBA data loading is NOT implemented; the package returns sample data only when explicitly requested. See README.",
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
        "Development Status :: 7 - Inactive",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
)
