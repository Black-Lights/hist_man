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
# ----------------------------------------------------------------
# import pytest
# from histogram_manipulation import HistogramMatcher
# import rasterio as rio
#
#
# def test_valid_file_format():
#     # Test with valid GeoTIFF files
#     secondary_path = "./histogram_matching_data/post_fire.tif"
#     reference_path = "./histogram_matching_data/pre_fire.tif"
#
#     matcher = HistogramMatcher(secondary_path, reference_path)
#     assert matcher.secondary is not None
#     assert matcher.reference is not None
#
#
# def test_invalid_file_format():
#     # Test with an invalid file format (e.g., a PNG file)
#     invalid_file = "./histogram_matching_data/invalid.png"
#     valid_file = "./histogram_matching_data/pre_fire.tif"
#
#     with pytest.raises(ValueError, match="The secondary file '.*' is not a GeoTIFF."):
#         HistogramMatcher(invalid_file, valid_file)
#
#
# def test_nonexistent_file():
#     # Test with a nonexistent file
#     nonexistent_file = "./histogram_matching_data/nonexistent_file.tif"
#     valid_file = "./histogram_matching_data/pre_fire.tif"
#
#     with pytest.raises(ValueError, match="The secondary file '.*' is not readable or does not exist."):
#         HistogramMatcher(nonexistent_file, valid_file)
