"""
Histogram Equalization for Grayscale Images
-------------------------------------------

This module provides a HistogramEqualization class for performing histogram equalization on grayscale images.
The class includes methods to load images, compute histograms, perform equalization, save the equalized image, and visualize results.

Dependencies:
- cv2: For image reading and processing.
- numpy: For numerical operations.
- matplotlib.pyplot: For visualization.
- rasterio: (Optional) For handling geospatial raster images.

Classes:
--------
HistogramEqualization:
    A class for histogram equalization of grayscale images.

    Methods:
    --------
    __init__(self, image_path):
        Initializes the class with the path to a grayscale image and validates the input.

    load_image(self):
        Loads the grayscale image from the specified path.

    compute_histogram(self):
        Computes the histogram of the loaded image.

    compute_cdf(self):
        Computes the cumulative distribution function (CDF) of the image histogram.

    equalize(self):
        Performs histogram equalization on the loaded image.

    save_equalized_image(self, output_path):
        Saves the equalized image to the specified output path.

    display_images(self):
        Displays the original and equalized images side by side.

    plot_histograms(self):
        Plots histograms for the original and equalized images.
"""


import cv2
import numpy as np
import matplotlib.pyplot as plt
import rasterio


class HistogramEqualization:
    """
    A class for performing histogram equalization on grayscale images.

    Attributes:
    -----------
    image_path : str
        Path to the grayscale image.
    image : numpy.ndarray
        Loaded grayscale image.
    equalized_image : numpy.ndarray
        Image after histogram equalization.
    histogram : numpy.ndarray
        Histogram of the original image.
    cdf : numpy.ndarray
        Cumulative distribution function (CDF) of the histogram.

    Methods:
    --------
    load_image(self):
        Loads the image and ensures it is grayscale.

    compute_histogram(self):
        Computes the histogram of the grayscale image.

    compute_cdf(self):
        Computes the cumulative distribution function (CDF) of the histogram.

    equalize(self):
        Performs histogram equalization on the image.

    save_equalized_image(self, output_path):
        Saves the equalized image to the specified output path.

    display_images(self):
        Displays the original and equalized images.

    plot_histograms(self):
        Plots histograms of the original and equalized images.
    """

    def __init__(self, image_path):
        """
        Initialize the class with the image path.

        Parameters:
        -----------
        image_path : str
            Path to the image file.
        """
        self.image_path = image_path
        self.image = None
        self.equalized_image = None
        self.histogram = None
        self.cdf = None
        self.load_image()

    def load_image(self):
        """
        Load the image and ensure it is grayscale.

        Raises:
        -------
        FileNotFoundError:
            If the image cannot be found.
        ValueError:
            If the image is not grayscale.
        """
        self.image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            raise FileNotFoundError(f"Unable to load the image at path: {self.image_path}")
        if self.image.ndim != 2:
            raise ValueError("The image must be grayscale.")

    def compute_histogram(self):
        """
        Compute the histogram of the grayscale image.

        Returns:
        --------
        numpy.ndarray:
            The histogram array with 256 bins.
        """
        self.histogram = cv2.calcHist([self.image], [0], None, [256], [0, 256]).flatten()
        return self.histogram

    def compute_cdf(self):
        """
        Compute the cumulative distribution function (CDF) of the histogram.

        Returns:
        --------
        numpy.ndarray:
            The normalized CDF.
        """
        if self.histogram is None:
            self.compute_histogram()

        cdf = np.cumsum(self.histogram)
        cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        self.cdf = cdf_normalized.astype(np.uint8)
        return self.cdf

    def equalize(self):
        """
        Perform histogram equalization on the image.

        Returns:
        --------
        numpy.ndarray:
            The histogram-equalized image.
        """
        if self.cdf is None:
            self.compute_cdf()

        self.equalized_image = self.cdf[self.image]
        return self.equalized_image

    def save_equalized_image(self, output_path):
        """
        Saves the equalized image to the specified output path.

        Args:
            output_path (str): The path where the equalized image will be saved.
        """
        # Save the equalized image
        with rasterio.open(self.input_path) as src:
            meta = src.meta

        meta.update(dtype=rasterio.float32, count=1)

        with rasterio.open(output_path, 'w', **meta) as dst:
            dst.write(self.equalized_image.astype(rasterio.float32), 1)

        print(f"Equalized image saved at {output_path}")

    def display_images(self):
        """
        Display the original and equalized images side by side.
        """
        if self.equalized_image is None:
            self.equalize()

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.imshow(self.image, cmap="gray")
        plt.title("Original Image")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(self.equalized_image, cmap="gray")
        plt.title("Equalized Image")
        plt.axis("off")

        plt.tight_layout()
        plt.show()

    def plot_histograms(self):
        """
        Plot the histograms of the original and equalized images.
        """
        if self.equalized_image is None:
            self.equalize()

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.hist(self.image.ravel(), bins=256, range=[0, 256], color="blue", alpha=0.7)
        plt.title("Original Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")

        plt.subplot(1, 2, 2)
        plt.hist(self.equalized_image.ravel(), bins=256, range=[0, 256], color="green", alpha=0.7)
        plt.title("Equalized Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()
