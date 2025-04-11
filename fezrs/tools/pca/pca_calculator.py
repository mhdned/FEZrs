# Import packages and libraries
import numpy as np
from uuid import uuid4
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as skpc

# Import module and files
from fezrs.base import BaseTool
from fezrs.utils.type_handler import BandPathType


class PCACalculator(BaseTool):

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

        self.metadata_bands = self.files_handler.get_metadata_bands(
            requested_bands=[
                "nir",
                "blue",
                "green",
                "red",
                "swir1",
                "swir2",
            ]
        )

        self.image_shape = (
            self.metadata_bands["red"]["width"],
            self.metadata_bands["red"]["height"],
        )

    def _validate(self):
        pass

    def process(self):
        image_columns = []
        image_columns_filtered = self.files_handler.get_images_collection()
        for i in range(len(image_columns_filtered)):
            image_columns.append(image_columns_filtered[i].flatten())
        images = np.array(image_columns)
        pca = skpc(n_components=6)
        pca.fit(images)
        self._output = pca.components_[:6]
        return self._output

    def _customize_export_file(self, ax):
        pass

    def _export_file(
        self,
        output_path,
        title=None,
        figsize=(20, 30),
        show_axis=False,
        colormap="gray",
        show_colorbar=False,
        filename_prefix="Tool_output",
        dpi=1000,
        bbox_inches="tight",
        grid=False,
        nrows=6,
        ncols=2,
    ):
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        plt.title(title)
        for i, pca_component in enumerate(self._output):
            reshaped_component = pca_component.reshape(self.image_shape)
            ax[i, 0].imshow(reshaped_component, cmap=colormap)
            ax[i, 0].set_title(f"PCA Band {i + 1}")
            ax[i, 0].axis("off")
            ax[i, 1].hist(
                pca_component.ravel(),
                bins=256,
                density=True,
                histtype="bar",
                color="black",
            )
            ax[i, 1].set_title(f"Histogram of PCA Band {i + 1}")

        # Export file
        filename = f"{output_path}/{filename_prefix}_{uuid4().hex}.png"
        fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)

        # Close plt and return value
        plt.close(fig)

    def execute(
        self,
        output_path,
        title=None,
        figsize=(20, 30),
        show_axis=False,
        colormap=None,
        show_colorbar=False,
        filename_prefix="Tool_output",
        dpi=500,
        bbox_inches="tight",
        grid=True,
        nrows=6,
        ncols=2,
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

    calculator = PCACalculator(
        red_path=red_path,
        green_path=green_path,
        blue_path=blue_path,
        nir_path=nir_path,
        swir1_path=swir1_path,
        swir2_path=swir2_path,
    ).execute(output_path="./", title="PCA output")
