# -*- coding: utf-8 -*-
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="curate", # Replace with your own username
    version="0.1",
    author="Joe Pollacco",
    author_email="joseph.pollacco@pmb.ox.ac.uk",
    description="Package designed to help with analysis of data from Picasso.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FusionLocus/curate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)