from setuptools import setup, find_packages

setup(
    name='Designite-Util',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'DesigniteUtil = src.main:entry_point',
        ],
    },
    install_requires=[
        'typer'
    ],
    author="Tushar Sharma, Indranil Palit"
)