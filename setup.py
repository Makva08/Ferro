#!/usr/bin/env python3
"""
Created on Thu Jun  1 08:33:01 2017

@author: Jackson Anderson
"""

from distutils.core import setup

setup(
    name='Ferro',
    version='0.1dev',
    author='Jackson Anderson',
    author_email='jda4923@rit.edu',
    packages=['ferro',],
    license='',
    description='Manipulation and Modeling of Ferroelectric Test Data',
    long_description=open('README.txt').read(),
    install_requires=[
        'scipy',
        'numpy',
        'matplotlib',
        'mpldatacursor',
        'copy',
        're',
        'os',
        'csv',
    ],
)