"""
HistogramStretching Class
-------------------------
This class provides functionality for applying histogram stretching (contrast stretching) to GeoTIFF images.
It enhances the contrast of raster image bands and allows saving, visualizing, and analyzing the results.

Dependencies:
    - numpy (as np)
    - rasterio
    - matplotlib.pyplot (as plt)

Class Methods:
--------------
1. __init__(input_path, output_path):
    Initialize the class with the input GeoTIFF file path and the output path to save the processed image.

    Parameters:
        - input_path (str): Path to the input GeoTIFF file.
        - output_path (str): Path to save the processed image.

    Raises:
        - AssertionError: If the input file is not in GeoTIFF format or does not exist.

2. _validate_file_format(file_path, file_type):
    Internal method to validate that a file is in GeoTIFF format and is readable.

    Parameters:
        - file_path (str): Path to the file being validated.
        - file_type (str): Type of file being validated (e.g., "input" or "output").

    Raises:
        - AssertionError: If the file is not a valid GeoTIFF or cannot be read.

3. contrast_stretch(lower_percentile=2, upper_percentile=98):
    Perform contrast stretching on all bands of the input GeoTIFF.

    Parameters:
        - lower_percentile (int): Lower percentile for clipping (default: 2).
        - upper_percentile (int): Upper percentile for clipping (default: 98).

    Effects:
        - Stores the contrast-stretched image in `self.stretched_image`.

4. save_stretched_image():
    Save the contrast-stretched image to the specified output path.

    Effects:
        - Writes the stretched image to a new GeoTIFF file using the original file's metadata.

5. plot_rgb(default_bands=(3, 2, 1)):
    Plot the original and contrast-stretched RGB images side by side.

    Parameters:
        - default_bands (tuple): Default band order for RGB visualization (1-based indexing).

    Raises:
        - ValueError: If RGB band order cannot be determined from metadata and default order is invalid.

    Effects:
        - Displays a side-by-side comparison of the original and stretched images.

6. plot_singleband():
    Plot a single band of the original and contrast-stretched images.

    Effects:
        - Displays a side-by-side comparison of a selected band before and after stretching.
        - The band number can be modified within the method.

7. plot_histograms():
    Plot the histograms of the original and contrast-stretched images.

    Effects:
        - Displays the histograms of both the original and contrast-stretched images for comparison.
        - Each histogram shows pixel intensity distribution across all bands.
"""


import numpy as np
import rasterio
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt

class HistogramStretching:
    def __init__(self, input_path, output_path):
        self._validate_file_format(input_path, "input")
        self.input_path = input_path
        self.output_path = output_path
        # Open the input file using rasterio and read metadata
        with rasterio.open(self.input_path) as src:
            self.src_data = src.read()  # Reads all bands
            self.metadata = src.meta  # Metadata for saving

    def _validate_file_format(self, file_path, file_type):
        """Validate that the file is in the correct GeoTIFF format using assertions."""
        try:
            with rio.open(file_path) as src:
                # Assert that the file is a GeoTIFF
                assert src.driver == "GTiff", f" The {file_type} file '{file_path}' is not a GeoTIFF."
        except rio.errors.RasterioIOError:
            assert False, f"The {file_type} file '{file_path}' is not readable or does not exist."

    def contrast_stretch(self, lower_percentile=2, upper_percentile=98):
        # Apply contrast stretching to each band in the raster
        stretched_bands = []
        for band in self.src_data:
            # Calculate percentiles
            p2 = np.percentile(band, lower_percentile)
            p98 = np.percentile(band, upper_percentile)

            # Stretch and normalize values
            band_stretched = np.clip(band, p2, p98)
            band_stretched = (band_stretched - p2) / (p98 - p2)
            stretched_bands.append(band_stretched)

        # Stack stretched bands along the last axis
        self.stretched_image = np.stack(stretched_bands, axis=0)

    def save_stretched_image(self):
        # Save the contrast-stretched image to the specified output path
        with rasterio.open(self.output_path, 'w', **self.metadata) as dst:
            for i in range(1, self.stretched_image.shape[0] + 1):
                dst.write(self.stretched_image[i - 1], i)

    def plot_rgb(self, default_bands=(3, 2, 1)):
        """
        Plot the original and contrast-stretched images side by side using the correct RGB band order.
        Dynamically determines the RGB band order from metadata if available; otherwise, falls back to a default order.

        :param default_bands: Default band order for RGB (1-based indexing) if metadata is unavailable.
        """
        # Attempt to extract band descriptions from metadata
        try:
            with rasterio.open(self.input_path) as src:
                band_descriptions = src.descriptions
        except Exception as e:
            print(f"Warning: Could not read band descriptions from metadata: {e}")
            band_descriptions = None

        # Dynamically determine the band order for RGB
        band_map = {"red": None, "green": None, "blue": None}
        if band_descriptions:
            for idx, description in enumerate(band_descriptions):
                if description is not None:
                    description_lower = description.lower()
                    if "red" in description_lower:
                        band_map["red"] = idx + 1  # 1-based index
                    elif "green" in description_lower:
                        band_map["green"] = idx + 1
                    elif "blue" in description_lower:
                        band_map["blue"] = idx + 1

        # Fallback to default order if RGB bands are not determined
        if None in band_map.values():
            print("Warning: Could not determine RGB band order from metadata. Using default band order.")
            bands = default_bands
        else:
            bands = (band_map["red"], band_map["green"], band_map["blue"])

        # Prepare original image (RGB)
        original_rgb = np.stack([self.src_data[bands[0] - 1],
                                 self.src_data[bands[1] - 1],
                                 self.src_data[bands[2] - 1]], axis=-1)

        # Normalize the original image to [0, 1] if necessary
        if original_rgb.max() > 1:
            original_rgb = (original_rgb - original_rgb.min()) / (original_rgb.max() - original_rgb.min())

        # Prepare contrast-stretched image (RGB)
        stretched_rgb = np.stack([self.stretched_image[bands[0] - 1],
                                  self.stretched_image[bands[1] - 1],
                                  self.stretched_image[bands[2] - 1]], axis=-1)

        # Plot original and stretched images
        plt.figure(figsize=(12, 6))

        # Original image
        plt.subplot(1, 2, 1)
        plt.imshow(original_rgb)
        plt.title("Original Image (RGB)")
        plt.axis('off')  # Hide axes

        # Stretched image
        plt.subplot(1, 2, 2)
        plt.imshow(stretched_rgb)
        plt.title("Contrast-Stretched Image (RGB)")
        plt.axis('off')  # Hide axes

        plt.tight_layout()
        plt.show()

    def plot_singleband(self):
        # Plot a single band of the contrast-stretched image
        band_number = 1  # Replace with the desired band number
        band_image = self.stretched_image[band_number - 1]

        original_rgb = self.src_data[band_number - 1]

        # Plot original and stretched images
        plt.figure(figsize=(12, 6))

        # Original image
        plt.subplot(1, 2, 1)
        plt.imshow(original_rgb,cmap='gray')
        plt.title(f"original image Band {band_number}")
        plt.axis('off')  # Hide axes

        # Stretched image
        plt.subplot(1, 2, 2)
        plt.imshow(band_image, cmap='gray')
        plt.title(f"Contrast-Stretched Band {band_number}")
        plt.axis('off')  # Hide axes
        plt.tight_layout()
        plt.show()

    def plot_histograms(self):
        """
        Plot the histograms of the original and contrast-stretched images for all bands.
        """
        plt.figure(figsize=(12, 6))

        # Loop through each band and plot histograms
        for i, (band_data, band_stretched) in enumerate(zip(self.src_data, self.stretched_image)):
            # Plot original histogram
            plt.subplot(2, len(self.src_data), i + 1)
            plt.hist(band_data.ravel(), bins=256, range=[0, 256], color="blue", alpha=0.7)
            plt.title(f"Original Histogram (Band {i + 1})")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")

            # Plot stretched histogram
            plt.subplot(2, len(self.src_data), len(self.src_data) + i + 1)
            plt.hist(band_stretched.ravel(), bins=256, range=[0, 1], color="green", alpha=0.7)
            plt.title(f"Stretched Histogram (Band {i + 1})")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

