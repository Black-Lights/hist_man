import matplotlib

matplotlib.use('Qt5Agg')  # Use a GUI backend compatible with PyCharm
import os
from histogram_manipulation.equalization import HistogramEqualization


def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the image
    image_path = os.path.join(script_dir, '../tests/histogram_equalization_data/single_band_dtm_4326.tif')

    # Normalize the path
    image_path = os.path.normpath(image_path)

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: File does not exist at {image_path}")
        return

    # Proceed with the histogram equalization
    try:
        processor = HistogramEqualization(image_path)
        processor.equalize()
        processor.display_images()
        processor.plot_histograms()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
