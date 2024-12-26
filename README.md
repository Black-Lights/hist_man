# Geospatial Raster Processing Library

## Overview

This library provides geospatial image processing utilities for enhancing and analyzing raster datasets. It includes the following modules:

1. **Histogram Stretching**: A module to enhance the contrast of raster images by applying percentile-based stretching.
2. **Histogram Matching**: A module to adjust the pixel intensity distribution of a raster image to match a reference histogram.

These tools are designed for geospatial applications, enabling preprocessing steps commonly used in remote sensing and GIS workflows.

---

## Features

### Histogram Stretching
- Enhances the contrast of images by clipping and rescaling pixel intensity values between specified lower and upper percentiles.
- Outputs a visually improved raster image with stretched pixel values.
- Supports multi-band raster datasets.

### Histogram Matching
- Adjusts the histogram of an input image to match the histogram of a reference image.
- Useful for normalizing image datasets for analysis or visualization.
- Compatible with single-band and multi-band raster datasets.

---

## Installation

```bash
git clone https://github.com/Black-Lights/hist_man.git
cd histogram_manipulation
pip install -r requirements.txt
```


## Usage
### Histogram Stretching 

```python
from histogram_manipulation import HistogramStretching

# Initialize the class with input and output paths
stretching = HistogramStretching(input_path="input.tif", output_path="stretched_output.tif")

# Apply contrast stretching
stretching.contrast_stretch(lower_percentile=2, upper_percentile=98)

# Save the stretched image
stretching.save_stretched_image()

# Plot original vs. stretched images in RGB channel 
stretcher.plot_rgb()
# Plot original vs. stretched images in single channel
stretcher.plot_singleband()
```

### Histogram Matching

```python
from histogram_manipulation import HistogramMatcher

# Initialize the class with input and reference images
matcher = HistogramMatching(reference_path="reference.tif", output_path="matched_output.tif")

# Apply histogram matching
matcher.match_histograms()

# Save the matched image
matcher.save_matched_image()

# Plot the bands of secondary, reference, and matched images
matcher.plot_bands(matcher.secondary, "Secondary")
matcher.plot_bands(matcher.reference, "Reference")

with rio.open(matcher.matched_path) as matched_src:
    matched_data = matched_src.read()
matcher.plot_bands(matched_data, "Matched")

matcher.plot_histograms()
```
