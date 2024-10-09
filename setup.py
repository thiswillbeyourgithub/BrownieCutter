
from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="BrownieCutter",
    version="0.1.11",
    description="Quick script to create new python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thiswillbeyourgithub/BrownieCutter",
    packages=find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    keywords=["cookiecutter", "pypi", "install", "package", "python", "minimal", "minimalist", "tool"],
    python_requires=">=3.11",

    entry_points={
        'console_scripts': [
            'BrownieCutter=BrownieCutter.__init__:cli_launcher',
        ],
    },

    install_requires=[
        "fire >= 0.6.0",
        "beartype >= 0.19.0",
    ],

)
