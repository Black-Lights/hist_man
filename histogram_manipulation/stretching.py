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

    # def plot_rgb(self, bands=(3, 2, 1)):
    #     # Select RGB bands (default: bands 3, 2, and 1) and plot the image
    #     rgb_image = np.stack([self.stretched_image[bands[0] - 1],
    #                           self.stretched_image[bands[1] - 1],
    #                           self.stretched_image[bands[2] - 1]], axis=-1)
    #
    #     plt.imshow(rgb_image)
    #     plt.title("Contrast-Stretched Raster Data (RGB)")
    #     plt.axis('off')  # Hide axes for cleaner plot
    #     plt.show()

    def plot_rgb(self, bands=(3, 2, 1)):
        """
        Plot the original and contrast-stretched images side by side.
        :param bands: Tuple of band indices for RGB plotting (default: (3, 2, 1)).
        """
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

