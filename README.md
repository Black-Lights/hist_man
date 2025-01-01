# Geospatial Raster Processing Library

## Overview

This library provides geospatial image processing utilities for enhancing and analyzing raster datasets. It aims to provide essential functionalities for image histogram manipulation, allowing users to input multi-band images and apply various operations to enhance image contrast and distribution. It includes the following modules:

1. **Histogram Stretching**: A module to enhance the contrast of raster images by applying percentile-based stretching.
2. **Histogram Matching**: A module to adjust the pixel intensity distribution of a raster image to match a reference histogram.
3. **Histogram Equalization**: A module to improve the contrast of raster images by redistributing pixel intensity values using histogram equalization.

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

### Histogram Equalization
- Improves image contrast by redistributing pixel intensity values across the entire intensity range.
- Automatically balances the intensity distribution to enhance image details.
- Supports single-band raster datasets.

---

## Installation

```bash
pip install histogram-manipulation
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
stretching.plot_rgb()
# Plot original vs. stretched images in single channel
stretching.plot_singleband()

# Plot the Histograms
stretching.plot_histograms()
```

### Histogram Matching

```python
from histogram_manipulation import HistogramMatcher

# Initialize the class with input and reference images
matcher = HistogramMatcher(reference_path="reference.tif", output_path="matched_output.tif")

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

### Histogram Equalization

```python
from histogram_manipulation.equalization import HistogramEqualization

# Initialize the class with the input path
equalizer = HistogramEqualization(input_path="input.tif")

# Apply histogram equalization
equalizer.equalize()

# Save the equalized image
equalizer.save_equalized_image(output_path="equalized_output.tif")

# Display the original and equalized images side by side
equalizer.display_images()

# Plot histograms of the original and equalized images
equalizer.plot_histograms()
```