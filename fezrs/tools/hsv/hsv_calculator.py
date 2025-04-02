# Import packages and libraries
import numpy as np
from uuid import uuid4
from pathlib import Path
from skimage.color import rgb2hsv
from matplotlib import pyplot as plt

# Import module and files
from fezrs.base import BaseTool
from fezrs.utils.type_handler import PathLike

# Calculator class
class HSVCalculator(BaseTool):
    """
    ## HSVCalculator (class)
    This class processes multispectral remote sensing images by normalizing the input bands
    and converting them into the HSV (Hue, Saturation, Value) color space.
    """
    def __init__(self, nir_path: PathLike, blue_path: PathLike, green_path: PathLike):
        """
        ## __init__ (method)
        Initializes the HSVCalculator with paths to Near-Infrared (NIR), Blue, and Green band images.
        
        ### Description:
        This class processes multispectral remote sensing images by normalizing the input bands
        and converting them into the HSV (Hue, Saturation, Value) color space.

        ### Args:
            nir_path (str or Path): File path to the Near-Infrared (NIR) band image.
            blue_path (str or Path): File path to the Blue band image.
            green_path (str or Path): File path to the Green band image.

        ### Attributes:
            normalized_bands (dict): A dictionary containing normalized versions of the NIR, Blue, and Green bands.
            __hsv_output (numpy.ndarray or None): Stores the HSV image after processing. Initially set to None.
        """
        super().__init__(nir_path=nir_path, blue_path=blue_path, green_path=green_path)
        self.normalized_bands = self.files_handler.get_normalize_bands()
        
        # Stores the processed HSV image
        self.__hsv_output: np.ndarray | None = None

    #TODO - Implement validation method
    def validate(self):
        """
        ## validate (method)
        Placeholder for validation logic (to be implemented in the future).
        """
        pass

    #TODO - Add comment and split sections from eachother
    def calculate(self) -> np.ndarray:
        """
        ## calculate (method)
        Computes the HSV representation of the input multispectral image.

        ### Returns:
            np.ndarray: The computed HSV image.
        """
        
        # Fetch normalized bands
        nir, blue, green = (self.normalized_bands[band] for band in ("nir", "blue", "green"))

        # Combine bands into an RGB-like array (NIR, Green, Blue order) and convert to HSV
        self.__hsv_output = rgb2hsv(np.dstack((nir, green, blue)))
        return self.__hsv_output

    def export_file(self, 
            output_path: PathLike,
            title: str | None = None,
            figsize: tuple = (10, 5), 
            show_axis: bool = True, 
            colormap: str = None, 
            show_colorbar: bool = True, 
            filename_prefix: str = "HSV_output",
            dpi: int = 500
        ):
        """
        ## export_file (method)
        Exports the HSV image as a PNG file with customizable visualization options.

        ### Args:
            output_path (str or Path): Directory where the file will be saved.
            figsize (tuple, optional): Figure size in inches. Defaults to (10, 5).
            show_axis (bool, optional): Whether to display axes. Defaults to True.
            colormap (str, optional): Colormap to apply to the image. Defaults to None.
            show_colorbar (bool, optional): Whether to include a colorbar. Defaults to True.
            filename_prefix (str, optional): Prefix for the output filename. Defaults to "HSV_output".
            dpi (int, optional): Resolution of the saved image. Defaults to 500.
        """
        
        #NOTE - Check if HSV is processed and store in output property 
        if self.__hsv_output is None:
            raise ValueError("HSV data not computed. Run `calculate()` before exporting.")
        
        # Ensure output path exists
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # if colormap and colormap not in cm.cmap_d:
        #     raise ValueError(f"Invalid colormap: {colormap}")
        
        # Configure and save the figure
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(self.__hsv_output, cmap=colormap)
        
        if not show_axis:
            ax.axis("off")
        
        if show_colorbar:
            fig.colorbar(im, ax=ax)
            
        if title:
            plt.title(f"{title}-FEZrs")

        filename = f"{output_path}/{filename_prefix}_{uuid4().hex}.png"
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        
        #FIX Should return the location or output file
        return filename


#NOTE - These block code for test the tools, delete before publish product
if __name__ == "__main__":
    nir_path = Path.cwd() / "data/NIR.tif"
    blue_path = Path.cwd() / "data/Blue.tif"
    green_path = Path.cwd() / "data/Green.tif"
    
    calculator = HSVCalculator(blue_path=blue_path, green_path=green_path, nir_path=nir_path)
    
