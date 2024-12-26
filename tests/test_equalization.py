import unittest
import numpy as np
import cv2
from histogram_manipulation import HistogramEqualization  # Replace with the correct import path


class TestHistogramEqualization(unittest.TestCase):
    def setUp(self):
        """
        Setup the necessary preconditions for each test.
        You can create a simple test image for all tests here.
        """
        # Create a simple 5x5 grayscale image for testing
        # This image is manually designed so we can calculate expected results
        self.image_path = 'test_image.jpg'
        self.test_image = np.array([[0, 50, 100, 150, 200],
                                    [0, 50, 100, 150, 200],
                                    [0, 50, 100, 150, 200],
                                    [0, 50, 100, 150, 200],
                                    [0, 50, 100, 150, 200]], dtype=np.uint8)

        # Save the test image for loading in the class
        cv2.imwrite(self.image_path, self.test_image)

        # Initialize HistogramEqualization object with the test image
        self.hist_eq = HistogramEqualization(self.image_path)

    def tearDown(self):
        """
        Clean up after each test (delete the test image file if needed).
        """
        import os
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

    def test_load_image(self):
        """
        Test if the image is loaded correctly as grayscale.
        """
        self.assertEqual(self.hist_eq.image.shape, (5, 5), "Image not loaded correctly as grayscale.")

    def test_compute_histogram(self):
        """
        Test if the histogram computation returns the expected result.
        """
        # Expected histogram based on the simple test image
        expected_histogram = np.array(
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        computed_histogram = self.hist_eq.compute_histogram()
        np.testing.assert_array_equal(computed_histogram, expected_histogram, "Histogram is not computed correctly.")

    def test_compute_cdf(self):
        """
        Test if the CDF is computed correctly based on the histogram.
        """
        computed_cdf = self.hist_eq.compute_cdf()

        # Manually compute the CDF based on the image histogram
        expected_cdf = np.cumsum(self.hist_eq.compute_histogram())
        expected_cdf_normalized = (expected_cdf - expected_cdf.min()) * 255 / (expected_cdf.max() - expected_cdf.min())
        expected_cdf_normalized = expected_cdf_normalized.astype(np.uint8)

        np.testing.assert_array_equal(computed_cdf, expected_cdf_normalized, "CDF is not computed correctly.")

    def test_equalize(self):
        """
        Test if the histogram equalization function works as expected.
        """
        equalized_image = self.hist_eq.equalize()

        # Ensure the result is a valid image
        self.assertEqual(equalized_image.shape, self.test_image.shape,
                         "Equalized image does not have the correct shape.")
        self.assertTrue(np.amin(equalized_image) >= 0 and np.amax(equalized_image) <= 255,
                        "Equalized image pixel values are out of range.")

    def test_display_images(self):
        """
        Test if display_images runs without error (it shows the images).
        """
        try:
            self.hist_eq.display_images()
            displayed = True  # If no error, consider the display successful
        except Exception as e:
            displayed = False
            print(f"Error displaying images: {e}")

        self.assertTrue(displayed, "Displaying images failed.")

    def test_plot_histograms(self):
        """
        Test if plot_histograms runs without error (it plots the histograms).
        """
        try:
            self.hist_eq.plot_histograms()
            plotted = True  # If no error, consider the plot successful
        except Exception as e:
            plotted = False
            print(f"Error plotting histograms: {e}")

        self.assertTrue(plotted, "Plotting histograms failed.")


if __name__ == "__main__":
    unittest.main()
