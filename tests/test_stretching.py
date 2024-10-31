
from histogram_manipulation import HistogramStretching

input_path = "./histogram_stretching_data/multiband_milan_S2.tif"
output_path = "./histogram_stretching_data/stretched_output.tif"
# Initialize the HistogramStretching class
stretcher = HistogramStretching(input_path, output_path)

# Perform contrast stretching
stretcher.contrast_stretch()

# Save the stretched image
stretcher.save_stretched_image()

# Plot the contrast-stretched RGB image
stretcher.plot_rgb()

input_path = "./histogram_stretching_data/single_band_dtm_4326.tif"
output_path = "./histogram_stretching_data/singleband_stretched_output.tif"
stretcher = HistogramStretching(input_path, output_path)

# Perform contrast stretching
stretcher.contrast_stretch()

# Save the stretched image
stretcher.save_stretched_image()

# Plot the contrast-stretched RGB image
stretcher.plot_singleband()