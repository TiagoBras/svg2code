#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import os

def version():
    with open(os.path.abspath('VERSION')) as f:
        return f.read().strip()

    raise IOError("Error: 'VERSION' file not found.")

VERSION = version()

setup(
    name='svg2code',
    version=VERSION,
    description='SVG2Code - Code Generator',
    long_description=open(os.path.abspath('README.md')).read(),
    author='Tiago Bras',
    author_email='tiagodsbras@gmail.com',
    license='MIT',
    url='https://github.com/TiagoBras/svg2code',
    packages=find_packages(exclude=[]),
    entry_points={
        'console_scripts': [
            'svg2code = svg2code.cli:main'
        ]
    },
    install_requires=['Jinja2>=2.9.5'],
    setup_requires=[],
    tests_require=[]
)
