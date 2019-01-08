# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='src',
    version='0.0.1',
    description='Q learning in maze environment',
    long_description=readme,
    author='Sebastian Eger',
    author_email='eger.sebsatian@gmx.de',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

