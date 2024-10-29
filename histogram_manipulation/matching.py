# matching.py

import rasterio as rio
from skimage.exposure import match_histograms
from rasterio.plot import show
from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np

class HistogramMatcher:
    def __init__(self, secondary_path, reference_path):
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

    def match_histogram(self):
        print(f"Secondary raster band count: {self.secondary.shape[0]}")
        print(f"Reference raster band count: {self.reference.shape[0]}")
        """Perform histogram matching band-by-band."""
        for band in range(self.secondary.shape[0]):
            # Match histogram and save each band separately
            matched_band = match_histograms(self.secondary[band], self.reference[band], channel_axis=-1)
            file_path = f"./histogram_matching_data/fire_rgb_nir_match_{band + 1}.tif"
            self.file_list.append(file_path)

            # Write matched band
            with rio.open(file_path, 'w', **self.metadata_secondary) as dst_band:
                dst_band.write(matched_band.astype(self.metadata_secondary['dtype']), 1)

        # Combine matched bands into a single multiband file
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

    def plot_histograms(self):
        """Plot histograms and CDFs of the secondary, reference, and matched images."""
        with rio.open(self.matched_path) as src:
            matched = src.read()

        fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(10, 10))
        images = [self.secondary, self.reference, matched]
        titles = ["Secondary", "Reference", "Matched"]

        for i, img in enumerate(images):
            for c, c_color in enumerate(('red', 'green', 'blue', 'nir')):
                img_hist, bins = exposure.histogram(img[c], source_range='dtype')
                axes[c, i].plot(bins, img_hist / img_hist.max())
                img_cdf, bins = exposure.cumulative_distribution(img[c])
                axes[c, i].plot(bins, img_cdf)
                axes[c, i].set_xlim([0, 40000])
                axes[c, 0].set_ylabel(c_color)

        for i, title in enumerate(titles):
            axes[0, i].set_title(title)

        plt.tight_layout()
        plt.show()
