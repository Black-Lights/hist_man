"""
Histogram Matching for Geospatial Raster Data
---------------------------------------------

This module provides a `HistogramMatcher` class for performing histogram matching between a reference raster and a secondary raster.
The class includes methods to validate input files, normalize raster bands, match histograms manually, and visualize results.

Dependencies:
- `rasterio`: For reading and writing raster files.
- `skimage.exposure`: For histogram analysis.
- `matplotlib.pyplot`: For plotting.
- `numpy`: For numerical operations.

Classes:
--------
HistogramMatcher:
    A class for histogram matching between a secondary raster and a reference raster.

    Methods:
    --------
    __init__(self, secondary_path, reference_path):
        Initializes the class with paths to the secondary and reference rasters, and validates their formats.

    _validate_file_format(self, file_path, file_type):
        Ensures that the input files are GeoTIFFs and can be opened.

    _calculate_cdf(self, hist):
        Computes the cumulative distribution function (CDF) from a histogram.

    _match_histogram_manual(self, source, reference):
        Manually matches the histogram of a source raster band to a reference raster band.

    match_histogram(self):
        Matches histograms of all bands in the secondary raster to the corresponding bands in the reference raster.

    combine_bands(self):
        Combines individually matched bands into a single multiband raster.

    plot_bands(self, image, title):
        Visualizes individual raster bands with normalized intensity.

    plot_histograms(self):
        Plots histograms and CDFs for secondary, reference, and matched rasters.
"""


# matching.py
from skimage import exposure
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np

class HistogramMatcher:
    def __init__(self, secondary_path, reference_path):
        # Validate file formats
        self._validate_file_format(secondary_path, "secondary")
        self._validate_file_format(reference_path, "reference")

        # Load the reference and secondary images
        with rio.open(reference_path) as ref:
            self.reference = ref.read()
            self.metadata_reference = ref.profile.copy()
            self.metadata_reference.update(compress='deflate')

        with rio.open(secondary_path) as sec:
            self.secondary = sec.read()
            self.metadata_secondary = sec.profile.copy()
            self.metadata_secondary.update(compress='deflate')

        self.file_list = []  # To store paths of individual band files

    def _validate_file_format(self, file_path, file_type):
        """Validate that the file is in the correct GeoTIFF format using assertions."""
        try:
            with rio.open(file_path) as src:
                # Assert that the file is a GeoTIFF
                assert src.driver == "GTiff", f" The {file_type} file '{file_path}' is not a GeoTIFF."
        except rio.errors.RasterioIOError:
            assert False, f"The {file_type} file '{file_path}' is not readable or does not exist."

    def _calculate_cdf(self, hist):
        """Calculate the cumulative distribution function from a histogram."""
        cdf = hist.cumsum()
        if cdf[-1] == 0:
            return np.zeros_like(cdf)  # Return an array of zeros to avoid division by zero
        cdf_normalized = cdf / cdf[-1]  # Normalize to range [0, 1]
        return cdf_normalized

    def _match_histogram_manual(self, source, reference):
        """Perform manual histogram matching between source and reference arrays."""
        # Calculate histograms for both source and reference
        hist_source, bins_source = np.histogram(source.flatten(), bins=256, range=[0, 1], density=True)
        hist_ref, bins_ref = np.histogram(reference.flatten(), bins=256, range=[0, 1], density=True)

        # Compute the CDF for source and reference
        cdf_source = self._calculate_cdf(hist_source)
        cdf_ref = self._calculate_cdf(hist_ref)

        # Create a lookup table to match source values to reference values
        lookup_table = np.interp(cdf_source, cdf_ref, bins_ref[:-1])

        # Map the source array using the lookup table
        source_matched = np.interp(source.flatten(), bins_source[:-1], lookup_table)
        return source_matched.reshape(source.shape)

    def match_histogram(self):
        print(f"Secondary raster band count: {self.secondary.shape[0]}")
        print(f"Reference raster band count: {self.reference.shape[0]}")

        for band in range(self.secondary.shape[0]):
            print(f"Processing band {band + 1}")
            # Normalize input bands to the range [0, 1] for histogram calculations
            source_norm = (self.secondary[band] - self.secondary[band].min()) / (self.secondary[band].max() - self.secondary[band].min())
            reference_norm = (self.reference[band] - self.reference[band].min()) / (self.reference[band].max() - self.reference[band].min())

            # Match histogram of the current band
            matched_band = self._match_histogram_manual(source_norm, reference_norm)

            # Denormalize the matched band back to the original range
            matched_band = matched_band * (self.secondary[band].max() - self.secondary[band].min()) + self.secondary[band].min()

            file_path = f"./histogram_matching_data/fire_rgb_nir_match_{band + 1}.tif"
            self.file_list.append(file_path)

            # Write matched band
            with rio.open(file_path, 'w', **self.metadata_secondary) as dst_band:
                dst_band.write(matched_band.astype(self.metadata_secondary['dtype']), 1)

        self.combine_bands()

    def combine_bands(self):
        """Combine matched bands into a single multiband raster."""
        with rio.open(self.file_list[0]) as src:
            meta = src.meta.copy()
        meta.update(count=len(self.file_list))

        self.matched_path = "./histogram_matching_data/fire_rgb_nir_match.tif"
        with rio.open(self.matched_path, 'w', **meta) as dst:
            for band_id, band_path in enumerate(self.file_list, start=1):
                with rio.open(band_path) as src_band:
                    dst.write(src_band.read(1), band_id)

    def plot_bands(self, image, title):
        """Plot bands with normalized intensity."""
        fig, axarr = plt.subplots(1, image.shape[0], figsize=(20, 5))
        for i in range(image.shape[0]):
            band_norm = (image[i] - image[i].min()) / (image[i].max() - image[i].min())
            axarr[i].imshow(band_norm, cmap='gray')
            axarr[i].set_title(f'{title} - Band {i+1}')
            axarr[i].axis('off')
        plt.show()



    def plot_histograms(self, xlim=20000):
        """
        Plot histograms and CDFs of the secondary, reference, and matched images.
        Handles cases where fewer than four bands are present.

        Parameters:
        - xlim: int, optional, default=20000
            The x-axis limit for the plots.
        """
        with rio.open(self.matched_path) as src:
            matched = src.read()

        # Determine the number of bands dynamically
        num_bands = min(self.secondary.shape[0], 4)  # Use up to 4 bands, if available
        band_colors = ['red', 'green', 'blue', 'nir'][:num_bands]

        fig, axes = plt.subplots(nrows=num_bands, ncols=3, figsize=(10, num_bands * 2.5))
        images = [self.secondary, self.reference, matched]
        titles = ["Secondary", "Reference", "Matched"]

        for i, img in enumerate(images):
            for c in range(num_bands):  # Loop over the available bands
                img_hist, bins = exposure.histogram(img[c], source_range='dtype')
                axes[c, i].plot(bins, img_hist / img_hist.max(), label="Histogram")
                img_cdf, bins = exposure.cumulative_distribution(img[c])
                axes[c, i].plot(bins, img_cdf, label="CDF")
                axes[c, i].set_xlim([0, xlim])
                axes[c, i].set_ylabel(band_colors[c])
                axes[c, i].legend(loc="upper left")

        for i, title in enumerate(titles):
            axes[0, i].set_title(title)

        plt.tight_layout()
        plt.show()