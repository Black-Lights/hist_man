
from setuptools import setup, find_packages

setup(
    name='histogram_manipulation',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'matplotlib',
    ],
    author='Your Name',
    description='A library for histogram manipulation of images',
    url='https://github.com/yourusername/histogram_manipulation',
)
