# histogram_manipulation/__init__.py

# Import necessary modules
from .equalization import histogram_equalization
from .matching import histogram_matching
from .stretching import linear_stretching, saturated_linear_stretching
from .utils import load_image, preprocess_image, save_image

# Specify the version of your package
__version__ = "0.1.0"