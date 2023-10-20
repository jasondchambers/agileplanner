""" Setup script for agileplanner package."""
# pylint: disable=deprecated-module
from distutils.command.clean import clean
import os
from shutil import rmtree
from setuptools import setup, find_packages

class CleanCommand(clean):
    """Custom implementation of ``clean`` setuptools command."""
    CLEAN_FILES = 'dist ./app/agileplanner.egg-info'.split(' ')

    def run(self):
        """After calling the super class implementation, this function removes
        the dist directory and egg-info file if they exists."""
        super().run()
        for item_to_clean in self.CLEAN_FILES:
            print(f'Cleaning {item_to_clean}')
            if os.path.exists(item_to_clean):
                rmtree(item_to_clean)

with open("docs/README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="agileplanner",
    version="0.0.3",
    description="Agile planning tools for capacity calculation and basic scheduling of epics.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jasondchambers/agileplanner",
    author="Jason Chambers",
    author_email="jason.d.chambers@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Scheduling"
    ],
    install_requires=["pandas >= 2.1.1", "pyYAML >= 6.0.1"],
    extras_require={
        "dev": ["twine>=4.0.2"]
    },
    python_requires=">=3.10",
    cmdclass={
        'clean': CleanCommand,
    },
)
