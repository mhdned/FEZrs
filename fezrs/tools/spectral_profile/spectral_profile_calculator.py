# Import packages and libraries
import numpy as np
from uuid import uuid4
from pathlib import Path
from skimage import exposure
import matplotlib.pyplot as plt


# Import module and files
from fezrs.base import BaseTool
from fezrs.utils.type_handler import BandPathType


class SpectralProfileCalculator(BaseTool):

    def __init__(
        self,
        red_path: BandPathType,
        green_path: BandPathType,
        blue_path: BandPathType,
        nir_path: BandPathType,
        swir1_path: BandPathType,
        swir2_path: BandPathType,
    ):
        super().__init__(
            red_path=red_path,
            green_path=green_path,
            blue_path=blue_path,
            nir_path=nir_path,
            swir1_path=swir1_path,
            swir2_path=swir2_path,
        )

    def _validate(self):
        pass

    def process(self):
        image_columns = {
            key: value
            for key, value in self.files_handler.bands.items()
            if value is not None
        }
        image_columns_filtered = []
        image_columns_list_of_bands = list(image_columns.keys())

        for key, value in image_columns.items():
            image_columns_filtered.append(value)

        # Ensure imgcol[4] is within bounds and valid
        if len(image_columns_filtered) > 4 and isinstance(
            image_columns_filtered[4], np.ndarray
        ):
            self._output = exposure.adjust_log(image_columns_filtered[4])
        else:
            raise ValueError("Invalid image data at index 4.")

        self.xaxis = []
        self.yaxis = []

        # Prepare x and y axis data for plotting
        for i, img in enumerate(image_columns_filtered):
            self.xaxis.append(f"{image_columns_list_of_bands[i]}")
            self.yaxis.append(np.mean(img))

    def _customize_export_file(self, ax):
        pass

    def histogram_export(
        self,
        output_path: BandPathType,
        title: str | None = None,
        figsize: tuple = (10, 10),
        filename_prefix: str = "Histogram_Spectral_Profile_Tool_output",
        dpi: int = 500,
        bbox_inches: str = "tight",
        grid: bool = True,
        # show_axis: bool = False,
        # colormap: str = None,
        # show_colorbar: bool = False,
    ):
        self._validate()
        self.process()

        plt.figure(figsize=figsize)
        plt.plot(self.xaxis, self.yaxis)

        if title:
            plt.title(f"{title}-FEZrs")

        plt.xlabel("Bands")
        plt.ylabel("Intensity")
        plt.grid(grid)

        filename = f"{output_path}/{filename_prefix}_{uuid4().hex}.png"
        plt.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)

        plt.close()

        return self

    def execute(
        self,
        output_path,
        title=None,
        figsize=(10, 10),
        show_axis=True,
        colormap="gray",
        show_colorbar=False,
        filename_prefix="Tool_output",
        dpi=1000,
        bbox_inches="tight",
        grid=True,
    ):
        return super().execute(
            output_path,
            title,
            figsize,
            show_axis,
            colormap,
            show_colorbar,
            filename_prefix,
            dpi,
            bbox_inches,
            grid,
        )


# NOTE - These block code for test the tools, delete before publish product
if __name__ == "__main__":
    red_path = Path.cwd() / "data/Red.tif"
    green_path = Path.cwd() / "data/Green.tif"
    blue_path = Path.cwd() / "data/Blue.tif"
    nir_path = Path.cwd() / "data/NIR.tif"
    swir1_path = Path.cwd() / "data/SWIR1.tif"
    swir2_path = Path.cwd() / "data/SWIR2.tif"

    calculator = SpectralProfileCalculator(
        red_path=red_path,
        green_path=green_path,
        blue_path=blue_path,
        nir_path=nir_path,
        swir1_path=swir1_path,
        swir2_path=swir2_path,
    ).execute("./")
