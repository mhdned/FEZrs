# Import packages and libraries
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from typing import Optional, Dict, List

# Import module and files
from fezrs.utils.type_handler import BandPathType, BandNameType, BandTypes


# Helper functions
def _load_image(path: Optional[str]) -> Optional[np.ndarray]:
    """Loads an image from the given path if it exists."""
    if path and os.path.exists(path):
        return io.imread(path).astype(float)
    elif path is None:
        return None
    else:
        raise FileNotFoundError(f"File {path} not found")


def _normalize(image: Optional[np.ndarray]) -> Optional[np.ndarray]:
    """Normalizes an image between 0 and 1."""
    if image is None:
        return None
    return (image - np.min(image)) / (np.max(image) - np.min(image))


def _metadata_image(path: str) -> Dict[str, np.ndarray]:
    """Extracts metadata for a given image path."""
    image_plt = plt.imread(path)
    image_skimage = io.imread(path)
    return {
        "image_plt": image_plt,
        "image_skimage": image_skimage,
        "height": image_plt.shape[0],
        "width": image_plt.shape[1],
    }


class FileHandler:
    def __init__(
        self,
        red_path: Optional[BandPathType] = None,
        green_path: Optional[BandPathType] = None,
        blue_path: Optional[BandPathType] = None,
        nir_path: Optional[BandPathType] = None,
        swir1_path: Optional[BandPathType] = None,
        swir2_path: Optional[BandPathType] = None,
        tif_path: Optional[BandPathType] = None,
    ):
        self.band_paths: BandTypes = {
            "tif": tif_path,
            "red": red_path,
            "nir": nir_path,
            "blue": blue_path,
            "swir1": swir1_path,
            "swir2": swir2_path,
            "green": green_path,
        }

        self.bands: BandTypes = {
            key: _load_image(path) for key, path in self.band_paths.items()
        }

    def get_normalized_bands(
        self, requested_bands: Optional[List[BandNameType]] = None
    ):
        if requested_bands is None:
            requested_bands = list(self.bands.keys())

        return {
            band: _normalize(self.bands[band])
            for band in requested_bands
            if self.bands.get(band) is not None
        }

    def get_metadata_bands(
        self, requested_bands: Optional[list[BandNameType]] = None
    ) -> Dict[str, Dict]:
        if requested_bands is None:
            requested_bands = self.bands.keys()

        metadata = {}
        for band in requested_bands:
            path = self.band_paths.get(band)
            if path and os.path.exists(path):
                metadata[band] = _metadata_image(path)

        return metadata

    def get_images_collection(self) -> any:
        image_columns = {
            key: value for key, value in self.band_paths.items() if value is not None
        }
        return io.imread_collection(list(image_columns.values()))
