from pathlib import Path

from fezrs.base import BaseTool
from fezrs.utils.type_handler import BandPathType, TimeCDType


class TimeCalculator(BaseTool):
    def __init__(
        self,
        nir_path: BandPathType,
        before_nir_path: BandPathType,
        time: TimeCDType,
    ):
        super().__init__(
            nir_path=nir_path,
            before_nir_path=before_nir_path,
        )

        self.time_bands = self.files_handler.get_metadata_bands(
            requested_bands=[
                "nir",
                "before_nir",
            ]
        )

        self.selectedTime = time

    def _validate(self):
        pass

    def process(self):
        match (self.selectedTime):
            case "after":
                self._output = self.time_bands["nir"]["image_skimage"]
            case "before":
                self._output = self.time_bands["before_nir"]["image_skimage"]
            case _:
                self._output = self.time_bands["nir"]["image_skimage"]

        return self._output

    def execute(
        self,
        output_path,
        title=None,
        figsize=(10, 10),
        show_axis=True,
        colormap="gray",
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
    nir_path = Path.cwd() / "data/Change Detection/After/B4.tif"
    swir1_path = Path.cwd() / "data/Change Detection/After/B5.tif"
    swir2_path = Path.cwd() / "data/Change Detection/After/B7.tif"

    before_nir_path = Path.cwd() / "data/Change Detection/Before/B4.tif"
    before_swir1_path = Path.cwd() / "data/Change Detection/Before/B5.tif"
    before_swir2_path = Path.cwd() / "data/Change Detection/Before/B7.tif"

    calculator = TimeCalculator(
        nir_path=nir_path,
        before_nir_path=before_nir_path,
        time="before",
    ).execute("./", title="Test CD time")
