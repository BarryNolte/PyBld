#################################################
#
# PyBld - setup for PyBld Tool
#
#################################################
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pybld",
    version="0.3.0",
    author="Barry Nolte",
    author_email="barry@barrynolte.com",
    description="Python based make tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pybld",
    install_requires=["sarge", "colorama", "tabulate"],
    packages=find_packages(exclude=['tests.py']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Installation/Setup",
        "Topic :: Utilities",
    ],
    entry_points={
        'console_scripts': ['pybld = pybld.pybuild:DoMain']
    },
)
