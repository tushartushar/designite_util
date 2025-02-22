from setuptools import setup, find_packages

setup(
    name='Designite-Util',
    version='1.0.3',
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