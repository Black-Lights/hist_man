import os

# Define the project structure
project_name = "histogram_manipulation"
structure = {
    project_name: [
        "histogram_manipulation/__init__.py",
        "histogram_manipulation/equalization.py",
        "histogram_manipulation/matching.py",
        "histogram_manipulation/stretching.py",
        "histogram_manipulation/saturated_stretching.py",
        "histogram_manipulation/utils.py",
        "tests/test_equalization.py",
        "tests/test_matching.py",
        "tests/test_stretching.py",
        "tests/test_saturated_stretching.py",
        "examples/example_usage.py",
        "setup.py",
        "README.md",
        "LICENSE",
        "requirements.txt"
    ]
}

# Create directories and files
base_path = r"C:\dev\gp24\main\hist_man"  # Base path for creating the structure
for folder, files in structure.items():
    folder_path = os.path.join(base_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(base_path, file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            if file.endswith("README.md"):
                # Write documentation content into README.md
                f.write("# Histogram Manipulation Library\n\nThis is a Python library for performing various histogram manipulation techniques on images such as histogram equalization, matching, linear stretching, and saturated linear stretching.")
            elif file.endswith("setup.py"):
                # Write setup script content into setup.py
                f.write("""
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
""")
            elif file.endswith("requirements.txt"):
                # Write required dependencies into requirements.txt
                f.write("numpy\nopencv-python\nmatplotlib")

# Return the base path to allow user access to the created files
base_path
