# Import packages and libraries
import numpy as np
from pathlib import Path
from typing import Union, Literal, TypedDict, Optional

# Definitions types
BandPathType = Union[str, Path]
BandNameType = Literal["tif", "red", "nir", "blue", "swir1", "swir2", "green"]


class BandTypes(TypedDict, total=False):
    tif: Optional[np.ndarray]
    red: Optional[np.ndarray]
    nir: Optional[np.ndarray]
    blue: Optional[np.ndarray]
    swir1: Optional[np.ndarray]
    swir2: Optional[np.ndarray]
    green: Optional[np.ndarray]


class BandPathsType(TypedDict, total=False):
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

BandNamePCAType = Literal["red", "nir", "blue", "swir1", "swir2", "green"]
