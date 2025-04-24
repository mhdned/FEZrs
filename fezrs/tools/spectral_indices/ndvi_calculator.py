# Import packages and libraries
from pathlib import Path
from matplotlib.pyplot import cm

# Import module and files
from fezrs.base import BaseTool
from fezrs.utils.type_handler import BandPathType


# Calculator class
class NDVICalculator(BaseTool):
    def __init__(
        self,
        nir_path: BandPathType,
        red_path: BandPathType,
    ):
        super().__init__(nir_path=nir_path, red_path=red_path)
        self.normalized_bands = self.files_handler.get_normalized_bands(
            requested_bands=["nir", "red"]
        )

    def _validate(self):
        pass

    def process(self):
        nir, red = (self.normalized_bands[band] for band in ("nir", "red"))

        self._output = (nir - red) / (nir + red)
        return self._output

    def execute(
        self,
        output_path,
        title=None,
        figsize=(15, 10),
        show_axis=False,
        colormap=cm.Grays,
        show_colorbar=True,
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
    nir_path = Path.cwd() / "data/NIR.tif"
    red_path = Path.cwd() / "data/Red.tif"

    calculator = NDVICalculator(nir_path=nir_path, red_path=red_path).execute(
        output_path="./", title="NDVI output"
    )
