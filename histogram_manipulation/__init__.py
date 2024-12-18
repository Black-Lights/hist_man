# __init__.py

from .matching import HistogramMatcher

from .stretching import HistogramStretching

from .equalization import HistogramEqualization

__all__ = ['HistogramMatcher', 'HistogramStretching', 'HistogramEqualization']
