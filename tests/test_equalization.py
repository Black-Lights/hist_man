"""
Histogram Equalization Test Script
----------------------------------

This script tests the functionality of the `HistogramEqualization` class by performing histogram equalization on a single-band raster image.
The script includes:
1. File path validation.
2. Execution of the equalization process.
3. Visualization of results (equalized image and histograms).

Dependencies:
- matplotlib (Qt5Agg backend)
- histogram_manipulation.HistogramEqualization
"""

import matplotlib
import os
from histogram_manipulation.equalization import HistogramEqualization

# Use a GUI backend compatible with PyCharm
matplotlib.use("Qt5Agg")


def test_histogram_equalization(image_path):
    """
    Test histogram equalization on a single-band raster image.

    Parameters:
    -----------
    image_path : str
        Absolute path to the input raster file.
    """
    print(f"Testing histogram equalization on: {image_path}")

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: File does not exist at {image_path}")
        return

    # Perform histogram equalization
    try:
        processor = HistogramEqualization(image_path)
        processor.equalize()
        processor.display_images()
        processor.plot_histograms()
        print(f"Histogram equalization completed successfully for: {image_path}\n")
    except FileNotFoundError as e:
        print(f"File Error: {e}")
    except ValueError as e:
        print(f"Value Error: {e}")


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the test image
    image_path = os.path.join(
        script_dir, "../tests/histogram_equalization_data/single_band_dtm_4326.tif"
    )

    # Normalize the path
    image_path = os.path.normpath(image_path)

    # Run the test
    test_histogram_equalization(image_path)
