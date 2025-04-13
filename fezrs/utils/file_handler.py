import os
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from typing import Optional, Dict, List

from fezrs.utils.type_handler import BandPathType, BandNameType, BandTypes


def _load_image(path: Optional[BandPathType]) -> Optional[np.ndarray]:
    """
    Loads an image from the specified file path if it exists.

    Args:
        path (Optional[str]): The file path to the image. If None, the function returns None.

    Returns:
        Optional[np.ndarray]: The loaded image as a NumPy array with float type, or None if the path is None.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
    """
    """Loads an image from the given path if it exists."""

    # TODO - Add a check for file type, files must be in (*.tiff | *.tif) format

    if path and os.path.exists(path):
        return io.imread(path).astype(float)
    elif path is None:
        return None
    else:
        raise FileNotFoundError(f"File {path} not found")


def _normalize(image: Optional[np.ndarray]) -> Optional[np.ndarray]:
    """
    Normalize a given image array to the range [0, 1].
    Parameters:
        image (Optional[np.ndarray]): The input image as a NumPy array.
            If None, the function returns None.
    Returns:
        Optional[np.ndarray]: The normalized image array with values scaled
            to the range [0, 1], or None if the input is None.
    Raises:
        TypeError: If the input is not a NumPy array.
    """

    if image is None:
        return None

    if not isinstance(image, np.ndarray):
        raise TypeError(f"Expected numpy.ndarray, but got {type(image)}")

    return (image - np.min(image)) / (np.max(image) - np.min(image))


def _metadata_image(path: str) -> Dict[str, np.ndarray]:
    """
    Extracts metadata for a given image file.

    This function reads an image from the specified file path using both Matplotlib
    and scikit-image libraries. It returns a dictionary containing the image data
    from both libraries, as well as the image's height and width.

    Args:
        path (str): The file path to the image.

    Returns:
        Dict[str, np.ndarray]: A dictionary containing:
            - "image_plt": The image data read using Matplotlib.
            - "image_skimage": The image data read using scikit-image.
            - "height": The height of the image (number of rows).
            - "width": The width of the image (number of columns).
    """
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
    FileHandler is a utility class for managing and processing geospatial image files.
    It provides functionality to load, normalize, and retrieve metadata for various image bands.
    Attributes:
        band_paths (Dict[str, Optional[BandPathType]]):
            A dictionary mapping band names (e.g., "red", "nir") to their respective file paths.
        bands (Dict[str, Any]):
            A dictionary mapping band names to their loaded image data.
    """

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
        """
        Retrieve normalized versions of the requested image bands.

        Args:
            requested_bands (Optional[List[BandNameType]]): A list of band names to normalize.
                If None, all available bands will be normalized.

        Returns:
            Dict[str, Optional[np.ndarray]]: A dictionary mapping band names to their normalized image data.
                Bands with no data will be excluded from the result.
        """
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
        """
        Retrieve metadata for the requested image bands.

        Args:
            requested_bands (Optional[List[BandNameType]]): A list of band names to retrieve metadata for.
                If None, metadata for all available bands will be retrieved.

        Returns:
            Dict[str, Dict]: A dictionary mapping band names to their metadata.
                Metadata includes image data and dimensions (height and width).
        """
        if requested_bands is None:
            requested_bands = self.bands.keys()

        metadata = {}
        for band in requested_bands:
            path = self.band_paths.get(band)
            if path and os.path.exists(path):
                metadata[band] = _metadata_image(path)

        return metadata

    def get_images_collection(self) -> any:
        """
        Retrieve a collection of all available image bands.

        Returns:
            skimage.io.ImageCollection: A collection of images loaded from the available band file paths.
        """
        image_columns = {
            key: value for key, value in self.band_paths.items() if value is not None
        }
        return io.imread_collection(list(image_columns.values()))
