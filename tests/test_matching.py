# main_script.py
import rasterio as rio
from histogram_manipulation import HistogramMatcher

# File paths
reference_path = "./histogram_matching_data/pre_fire.tif"
secondary_path = "./histogram_matching_data/post_fire.tif"

# Initialize the HistogramMatcher
matcher = HistogramMatcher(secondary_path, reference_path)


# Perform histogram matching
matcher.match_histogram()


# Plot the bands of secondary, reference, and matched images
matcher.plot_bands(matcher.secondary, "Secondary")
matcher.plot_bands(matcher.reference, "Reference")

with rio.open(matcher.matched_path) as matched_src:
    matched_data = matched_src.read()
matcher.plot_bands(matched_data, "Matched")

# Plot histograms and CDFs for secondary, reference, and matched images
matcher.plot_histograms()

#----------------------------------------------------------------
# second test

# # File paths
# reference_path = "./histogram_matching_data/sample.tiff"
# secondary_path = "./histogram_matching_data/sample2.tif"
#
# # Initialize the HistogramMatcher
# matcher = HistogramMatcher(secondary_path, reference_path)
#
#
# # Perform histogram matching
# matcher.match_histogram()
#
#
# # Plot the bands of secondary, reference, and matched images
# matcher.plot_bands(matcher.secondary, "Secondary")
# matcher.plot_bands(matcher.reference, "Reference")
#
# with rio.open(matcher.matched_path) as matched_src:
#     matched_data = matched_src.read()
# matcher.plot_bands(matched_data, "Matched")
#
# # Plot histograms and CDFs for secondary, reference, and matched images
# # you can change how much intensity values it shows on histogram the default value is 20000
# matcher.plot_histograms(xlim = 400)


