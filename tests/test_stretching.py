
from histogram_manipulation import HistogramStretching

# first test multi band
input_path = "./histogram_stretching_data/sample.tiff"
output_path = "./histogram_stretching_data/stretched_sample.tiff"

stretcher = HistogramStretching(input_path, output_path)

# Perform contrast stretching
stretcher.contrast_stretch()

# Save the stretched image
stretcher.save_stretched_image()

# Plot the contrast-stretched RGB image
# you can change the default order of bands
stretcher.plot_rgb(default_bands=(1, 2, 3))

# Plot the Histograms
stretcher.plot_histograms()


# second test multi band
input_path = "./histogram_stretching_data/multiband_milan_S2.tif"
output_path = "./histogram_stretching_data/stretched_multiband_milan_S2.tif"
# Initialize the HistogramStretching class
stretcher = HistogramStretching(input_path, output_path)

# Perform contrast stretching
stretcher.contrast_stretch()

# Save the stretched image
stretcher.save_stretched_image()

# Plot the contrast-stretched RGB image
stretcher.plot_rgb(default_bands=(3, 2, 1))

# Plot the Histograms
stretcher.plot_histograms()


# first test single band
input_path = "./histogram_stretching_data/single_band_dtm_4326.tif"
output_path = "./histogram_stretching_data/singleband_stretched_output.tif"

stretcher = HistogramStretching(input_path, output_path)
# Perform contrast stretching
stretcher.contrast_stretch()

# Save the stretched image
stretcher.save_stretched_image()

# Plot the contrast-stretched RGB image
stretcher.plot_singleband()

# Plot the Histograms
stretcher.plot_histograms()