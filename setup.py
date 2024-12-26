from setuptools import setup, find_packages

setup(
    name='histogram_manipulation',              # Name of your package
    version='0.1.0',                            # Initial version
    packages=find_packages(),                   # Automatically find all packages
    install_requires=[
        'numpy>=1.21',                          # Specify minimum versions if needed
        'opencv-python>=4.5',
        'matplotlib>=3.0',
        'rasterio>=1.2',
        'scikit-image>=0.18',
    ],
    author='EA',                                # Author name
    author_email='your.email@example.com',      # Optional email
    description='A library for histogram manipulation of images',
    long_description=open('README.md').read(),  # Use README as the description
    long_description_content_type='text/markdown',  # Specify markdown format
    url='https://github.com/Black-Lights/hist_man.git',  # GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',                    # Specify compatible Python versions
)
