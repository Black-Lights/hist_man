from setuptools import setup, find_packages

setup(
    name='histogram_manipulation',              # Name of your package
    version='1.0.0',                            # Updated version
    packages=find_packages(),                   # Automatically find all packages
    install_requires=[
        'affine>=2.4.0',
        'anyio>=4.6.2',
        'argon2-cffi>=23.1.0',
        'attrs>=24.2.0',
        'beautifulsoup4>=4.12.3',
        'cffi>=1.17.1',
        'charset-normalizer>=3.4.0',
        'click>=8.1.7',
        'cycler>=0.12.1',
        'fonttools>=4.55.0',
        'idna>=3.10',
        'imageio>=2.36.0',
        'Jinja2>=3.1.4',
        'kiwisolver>=1.4.7',
        'matplotlib>=3.9.2',
        'numpy>=2.1.3',
        'opencv-python>=4.10.0',
        'opencv-python-headless>=4.10.0.84',
        'pandas>=2.2.3',
        'Pillow>=11.0.0',
        'PyQt5>=5.15.11',
        'PyYAML>=6.0.2',
        'rasterio>=1.4.2',
        'requests>=2.32.3',
        'scikit-image>=0.24.0',
        'scipy>=1.14.1',
        'soupsieve>=2.6',
        'tifffile>=2024.9.20',
        'urllib3>=2.2.3',
    ],
    author='Mohammad Ammar Mughees, Seyederfan Eshghollahi',  # List both authors here
    author_email='mohammadammar.mughees@mail.polimi.it, erfaneshghelahi@gmail.com',  # Separate multiple emails with a comma
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