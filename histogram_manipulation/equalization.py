import cv2
import numpy as np
import matplotlib.pyplot as plt
import rasterio

class HistogramEqualization:
    """
    A class for performing histogram equalization on grayscale images.
    """

    def __init__(self, image_path):
        """
        Initialize the class with the image path.

        Parameters:
        - image_path (str): Path to the image file.
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
        - FileNotFoundError: If the image cannot be found.
        - ValueError: If the image is not grayscale.
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
        - numpy.ndarray: The histogram array with 256 bins.
        """
        self.histogram = cv2.calcHist([self.image], [0], None, [256], [0, 256]).flatten()
        return self.histogram

    def compute_cdf(self):
        """
        Compute the cumulative distribution function (CDF) of the histogram.

        Returns:
        - numpy.ndarray: The normalized CDF.
        """
        if self.histogram is None:
            self.compute_histogram()

        # Compute the cumulative sum (CDF)
        cdf = np.cumsum(self.histogram)

        # Normalize the CDF to span the full range of pixel values (0 to 255)
        cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        self.cdf = cdf_normalized.astype(np.uint8)
        return self.cdf

    def equalize(self):
        """
        Perform histogram equalization on the image.

        Returns:
        - numpy.ndarray: The histogram-equalized image.
        """
        if self.cdf is None:
            self.compute_cdf()

        # Map the original pixel values to the equalized values
        self.equalized_image = self.cdf[self.image]
        return self.equalized_image

    def display_images(self):
        """
        Display the original and equalized images side by side.
        """
        if self.equalized_image is None:
            self.equalize()

        plt.figure(figsize=(12, 6))

        # Original image
        plt.subplot(1, 2, 1)
        plt.imshow(self.image, cmap="gray")
        plt.title("Original Image")
        plt.axis("off")

        # Equalized image
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

        # Original histogram
        plt.subplot(1, 2, 1)
        plt.hist(self.image.ravel(), bins=256, range=[0, 256], color="blue", alpha=0.7)
        plt.title("Original Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")

        # Equalized histogram
        plt.subplot(1, 2, 2)
        plt.hist(self.equalized_image.ravel(), bins=256, range=[0, 256], color="green", alpha=0.7)
        plt.title("Equalized Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()
