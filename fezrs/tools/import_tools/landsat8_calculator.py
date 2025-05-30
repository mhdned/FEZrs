import numpy as np
from pathlib import Path

from fezrs.base import BaseTool
from fezrs.utils.type_handler import BandPathType, Landset8ExportType


class Landsat8_Calculator(BaseTool):

    def __init__(
        self,
        red_path: BandPathType,
        green_path: BandPathType,
        blue_path: BandPathType,
        nir_path: BandPathType,
        swir1_path: BandPathType,
        swir2_path: BandPathType,
        exportType: Landset8ExportType = None,
    ):
        super().__init__(
            red_path=red_path,
            green_path=green_path,
            blue_path=blue_path,
            nir_path=nir_path,
            swir1_path=swir1_path,
            swir2_path=swir2_path,
        )

        self.exportType: Landset8ExportType = exportType

    def _validate(self):
        pass

    def process(self):
        first_band = None
        second_band = None
        third_band = None

        match (self.exportType):
            case None:
                first_band = self.files_handler.bands["red"]
                second_band = self.files_handler.bands["green"]
                third_band = self.files_handler.bands["blue"]

            case "rgb":
                bands = self.files_handler.get_normalized_bands(
                    requested_bands=["red", "green", "blue"]
                )

                first_band = bands["red"]
                second_band = bands["green"]
                third_band = bands["blue"]

            case "infrared":
                bands = self.files_handler.get_normalized_bands(
                    requested_bands=["swir2", "swir1", "nir"]
                )

                first_band = bands["swir2"]
                second_band = bands["swir1"]
                third_band = bands["nir"]

            case _:
                first_band = self.files_handler.bands["red"]
                second_band = self.files_handler.bands["green"]
                third_band = self.files_handler.bands["blue"]

        stack = np.stack([first_band, second_band, third_band], axis=2)

        self._output = stack

    def execute(
        self,
        output_path,
        title=None,
        figsize=(10, 10),
        show_axis=False,
        colormap=None,
        show_colorbar=False,
        filename_prefix="Tool_output",
        dpi=500,
        bbox_inches="tight",
        grid=False,
        nrows=None,
        ncols=None,
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
            nrows,
            ncols,
        )


# NOTE - These block code for test the tools, delete before publish product
if __name__ == "__main__":
    red_path = Path.cwd() / "data/Red.tif"
    green_path = Path.cwd() / "data/Green.tif"
    blue_path = Path.cwd() / "data/Blue.tif"
    nir_path = Path.cwd() / "data/NIR.tif"
    swir1_path = Path.cwd() / "data/SWIR1.tif"
    swir2_path = Path.cwd() / "data/SWIR2.tif"

    calculator = Landsat8_Calculator(
        red_path=red_path,
        green_path=green_path,
        blue_path=blue_path,
        nir_path=nir_path,
        swir1_path=swir1_path,
        swir2_path=swir2_path,
        exportType=None,
    ).execute("./")
