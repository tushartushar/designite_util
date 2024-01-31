from setuptools import setup, find_packages

setup(
    name='Designite-Util',
    version='0.1.2',
    packages=find_packages(exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'DesigniteUtil = designiteutil.main:entry_point',
        ]
    },
    install_requires=[
        'typer'
    ],
    author="Tushar Sharma, Indranil Palit"
)