from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='amoveo-explorer',
    version='1.0',
    packages=find_packages(),
    long_description="",
    install_requires=[
        'asyncpg==0.18.1',
        'requests==2.20.0',
        'aiohttp==3.7.4',
        'psycopg2-binary==2.7.5',
    ]
)
