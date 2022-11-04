from distutils.core import setup
from setuptools import find_packages
import os

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''
setup(

# Project name: 
name='sbml2hyb',

# Packages to include in the distribution: 
package_dir={"":"src"},

# Packages to include in the distribution: 
packages=find_packages(where='src'),

# Project version number:
version='0.0.46',

# Long description of your library: 
long_description=long_description,
long_description_content_type='text/markdown',

# Your name: 
author='Rafael Costa',

# Your email address:
author_email='rafael.s.costa@tecnico.ulisboa.pt',

# Link to your github repository or website: 
url='https://github.com/rs-costa/sbml2hyb',

# Download Link from where the project can be downloaded from:
download_url='https://github.com/rs-costa/sbml2hyb',


# List project dependencies: 
install_requires=[
'Pillow==9.0',
'tensorflow==2.10.0',
'python-libsbml==5.19.6'
],

# https://pypi.org/classifiers/ 
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "Operating System :: OS Independent",
]
)