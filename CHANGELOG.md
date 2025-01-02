# Changelog

---

## [1.1.1] - 2025-01-02
### Fixed
- Fixed indentation issue in the `equalization` module that caused errors in execution.

---

## [1.1.0] - 2025-01-02
### Added
- Added support for dual execution environments (regular Python scripts and Jupyter Notebooks) by checking for `__file__` in globals. 
- Improved path handling for cross-platform compatibility using `os.path.join` and `os.path.normpath`.

### Fixed
- Fixed a bug in the `save_equalized_image` function where `input_path` was used instead of `image_path`, causing errors during saving.

---

## [1.0.0] - 2025-01-01
### Changed
- Updated `README.md` to explain examples more accurately.

---

## [0.1.0] - 2025-01-01
### Added
- Initial release of the library with core functionalities:
  - Histogram equalization.
  - Histogram matching.
  - Histogram stretching.
  - Displaying images and histograms.

---