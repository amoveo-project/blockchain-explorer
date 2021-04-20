from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='amoveo-explorer',
    version='1.0',
    packages=find_packages(),
    long_description="",
    install_requires=[
        'asyncpg==0.21.0',
        'requests==2.20.0',
        'aiohttp==3.4.4',
        'psycopg2-binary==2.7.5',
    ]
)
