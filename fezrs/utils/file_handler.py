# Import packages and libraries
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from typing import Optional, Dict


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
    """
    ## FileHandler (class)
    Handles loading, normalizing, and retrieving metadata for image bands.
    """

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
        """
        ## __init__ (method)
        Initializes FileHandler with optional paths for different bands.
        """
        self.band_paths = {
            "tif": tif_path,
            "red": red_path,
            "nir": nir_path,
            "blue": blue_path,
            "swir1": swir1_path,
            "swir2": swir2_path,
            "green": green_path,
        }

        self.bands = {key: _load_image(path) for key, path in self.band_paths.items()}

    def get_normalize_bands(self) -> Dict[str, Optional[np.ndarray]]:
        """
        ## get_normalize_bands (method)
        Returns a dictionary of normalized bands.
        """
        return {band: _normalize(image) for band, image in self.bands.items()}

    def get_metadata_bands(self, requested_bands: Optional[list] = None) -> Dict[str, Dict]:
        """
        ## get_metadata_bands (method)
        Returns metadata only for the requested bands.
        
        ### Args:
            requested_bands (list, optional): List of band names to retrieve metadata for.
            If None, returns metadata for all available bands.

        ### Returns:
            dict: Metadata for requested bands.
        """
        if requested_bands is None:
            requested_bands = self.bands.keys() 

        metadata = {}
        for band in requested_bands:
            path = self.band_paths.get(band)
            if path and os.path.exists(path):
                metadata[band] = _metadata_image(path)

        return metadata
