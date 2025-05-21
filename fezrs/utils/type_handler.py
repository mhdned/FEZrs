# Import packages and libraries
import numpy as np
from pathlib import Path
from typing import Union, Literal, TypedDict, Optional

# Definitions types
BandPathType = Union[str, Path]
"""Type alias for a file path to a band, as a string or pathlib.Path."""

BandNameType = Literal["tif", "red", "nir", "blue", "swir1", "swir2", "green"]
"""Type alias for supported band names."""


class BandTypes(TypedDict, total=False):
    """
    TypedDict for storing arrays of different bands.

    Keys are band names, values are optional numpy arrays representing band data.
    """

    tif: Optional[np.ndarray]
    red: Optional[np.ndarray]
    nir: Optional[np.ndarray]
    blue: Optional[np.ndarray]
    swir1: Optional[np.ndarray]
    swir2: Optional[np.ndarray]
    green: Optional[np.ndarray]


class BandPathsType(TypedDict, total=False):
    """
    TypedDict for storing file paths to different bands.

    Keys are band path names, values are file paths as strings or Path objects.
    """

    red_path: BandPathType
    green_path: BandPathType
    blue_path: BandPathType
    nir_path: BandPathType
    swir1_path: BandPathType
    swir2_path: BandPathType
    tif_path: BandPathType


PropertyGLCMType = Literal[
    "contrast",
    "ASM",
    "dissimilarity",
    "homogeneity",
]
"""Type alias for supported GLCM property names."""

BandNamePCAType = Literal["red", "nir", "blue", "swir1", "swir2", "green"]
"""Type alias for band names used in PCA."""
