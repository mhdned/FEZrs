import numpy as np
from pathlib import Path
from typing import Union, TypedDict, Optional

# Definition types
PathLike = Union[str, Path]
class BandsParams(TypedDict, total=False):
    tif: Optional[np.ndarray]
    red: Optional[np.ndarray]
    nir: Optional[np.ndarray]
    blue: Optional[np.ndarray]
    swir1: Optional[np.ndarray]
    swir2: Optional[np.ndarray]
    green: Optional[np.ndarray]
