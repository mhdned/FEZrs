from typing import Optional
import os
from skimage import io

import numpy as np

def _load_image(path: Optional[str]) -> Optional[np.ndarray]:
        if path and os.path.exists(path):
            return io.imread(path).astype(float)
        elif path is None:
            return None
        else:
            raise FileNotFoundError(f"File {path} not found")

def _normalize(image: np.ndarray) -> np.ndarray | None:
    if image is None:
        return None
    return (image - np.min(image)) / (np.max(image) - np.min(image))


class FileHandler:
    def __init__(
        self,
        tif_path: Optional[str] = None,
        red_path: Optional[str] = None,
        nir_path: Optional[str] = None,
        blue_path: Optional[str] = None,
        swir1_path: Optional[str] = None,
        swir2_path: Optional[str] = None,
        green_path: Optional[str] = None,
    ):
        self.tif_file = _load_image(tif_path)
        self.nir_band = _load_image(nir_path)
        self.red_band = _load_image(red_path)
        self.blue_band = _load_image(blue_path)
        self.swir1_band = _load_image(swir1_path)
        self.swir2_band = _load_image(swir2_path)
        self.green_band = _load_image(green_path)

    
    
    
    def get_normalize_bands(self) -> dict[str, np.ndarray]:
        return {
            "tif": _normalize(self.tif_file),
            "red": _normalize(self.red_band),
            "nir": _normalize(self.nir_band),
            "blue": _normalize(self.blue_band),
            "swir1": _normalize(self.swir1_band),
            "swir2": _normalize(self.swir2_band),
            "green": _normalize(self.green_band),
        }