#!/usr/bin/env python3

from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='myfpl',
    version='1.0',
    description='A useful module',
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='trozler',
    author_email='tony.rosler246@gmail.com',
    url="https://github.com/trozler/myfpl",
    packages=['myfpl'],
    keywords=['fpl', 'fantasy premier league',
              'cli', 'command line'],
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["myfpl=myfpl.__main__:main"]}
)
