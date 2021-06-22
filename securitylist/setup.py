#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="securitylist-dwf",
    version="0.0.1",
    author="Josh Bressers",
    author_email="josh@bress.net",
    description="A script for manaing the data in the DWF securitylist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/distributedweaknessfiling/dwf-request/securitylist",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
