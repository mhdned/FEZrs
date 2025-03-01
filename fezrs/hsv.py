from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2hsv
from fezrs.openrs.base import Base
from fezrs.openrs.file_handler import OpenFiles
from fezrs.exceptions import OException


class HSVCalculator(Base):
    """
    HSV Calculator for remote sensing applications.
    
    This class computes the Hue, Saturation, and Value (HSV) from NIR, Green, and Blue bands.
    """

    def __init__(self, files: OpenFiles):
        """
        Initializes the HSVCalculator with the required bands.

        :param files: OpenFiles instance containing NIR, Green, and Blue bands.
        :raises OException: If any required band is missing.
        """
        if not all([files.nir_band, files.green_band, files.blue_band]):
            raise OException("NIR, Green, and Blue bands are required for HSV calculation.")

        super().__init__(files)
        self.normalized_bands = self.files.get_normalize_bands()
        self.hsv = None

    def calculate(self, extra_params: dict = None):
        """
        Calculates the HSV values from the input bands.

        :param extra_params: (Optional) Dictionary for future additional parameters.
        :return: Computed HSV image (numpy array).
        """
        nir = self.normalized_bands["nir"]
        green = self.normalized_bands["green"]
        blue = self.normalized_bands["blue"]

        image_hsv = np.dstack((nir, green, blue))
        self.hsv = rgb2hsv(image_hsv)
        return self.hsv

    def export(self, file_path: Path, title: str = "HSV Image"):
        """
        Exports the computed HSV image as a PNG file.

        :param file_path: Path to save the output image.
        :param title: Title of the exported image.
        :raises OException: If HSV data is not yet computed.
        """
        if self.hsv is None:
            raise OException("HSV data not computed. Run `calculate()` before exporting.")

        plt.figure(figsize=(10, 5))
        plt.title(title)
        plt.imshow(self.hsv)
        plt.axis("off")
        plt.colorbar()
        plt.savefig(file_path)
        plt.close()


# Test Execution (if run as a script)
if __name__ == "__main__":
    nir_path = Path.cwd() / "fezrs/openrs/data/NIR.tif"
    green_path = Path.cwd() / "fezrs/openrs/data/Green.tif"
    blue_path = Path.cwd() / "fezrs/openrs/data/Blue.tif"

    files = OpenFiles(nir_path=nir_path, green_path=green_path, blue_path=blue_path)
    calculator = HSVCalculator(files)

    hsv = calculator.calculate()
    
    # Display the image
    plt.figure(figsize=(10, 5))
    plt.imshow(hsv)
    plt.colorbar()
    plt.axis("off")
    plt.show()
    
    # Save the image
    output_path = Path.cwd() / "output/hsv_result.png"
    calculator.export(output_path, title="HSV Calculation Result")
