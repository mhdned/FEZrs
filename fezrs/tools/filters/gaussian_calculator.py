# Import packages and libraries
import numpy as np
from uuid import uuid4
from pathlib import Path
from cv2 import GaussianBlur
from matplotlib import pyplot as plt

# Import module and files
from fezrs.base import BaseTool
from fezrs.utils.type_handler import PathLike

class GAUSSIANCalculator(BaseTool):
    """
    ## GAUSSIANCalculator (class)
    Applies a Gaussian blur filter to an image.

    ### Description:
    This tool takes a single-band (grayscale) image and applies a Gaussian blur
    to smooth out noise and enhance certain image features.
    """
    
    def __init__(self, tif_path: PathLike, ksize: tuple[int, int] = (13, 13), sigmaX: float = 0, sigmaY: float | None = None):
        """
        ## __init__ (method)
        Initializes the GAUSSIANCalculator class.
        
        ### Args:
            tif_path (str or Path): File path to the Tif image.
            ksize (tuple[int, int], optional): Kernel size for Gaussian blur. Must be odd and positive. Default is (13, 13).
            sigmaX (float, optional): Standard deviation in X direction. Default is 0.
            sigmaY (float | None, optional): Standard deviation in Y direction. If None, it defaults to sigmaX.

            
        ### Attributes:
            tif_file_metadata (dict): A dictionary containing metadata about the TIF image, including:
            - **image_plt (np.ndarray):** The image loaded using Matplotlib's `plt.imread()`.
            - **image_skimage (np.ndarray):** The image loaded using `skimage.io.imread()`.
            - **height (int):** The height (number of rows) of the image.
            - **width (int):** The width (number of columns) of the image.
        __gaussian_output (numpy.ndarray or None): Stores the GAUSSIAN filter after processing. Initially set to None.
        """
        
        
        super().__init__(tif_path=tif_path)
        self.tif_file_metadata = self.files_handler.get_metadata_bands(["tif"])["tif"]
        self.ksize = ksize
        self.sigmaX = sigmaX
        self.sigmaY = sigmaY
        self.__gaussian_output: np.ndarray | None = None
        
    def validate(self):
        """
        ## validate (method)
        Validates the input parameters before applying the Gaussian filter.
        """
        # Validate kernel size
        if (
            not isinstance(self.ksize, tuple) or
            len(self.ksize) != 2 or
            not all(isinstance(i, int) and i > 0 and i % 2 == 1 for i in self.ksize)
        ):
            raise ValueError("Kernel size must be a tuple of two odd, positive integers, e.g., (3, 3).")
        
        # Validate sigmaX
        if not isinstance(self.sigmaX, (int, float)) or self.sigmaX < 0:
            raise ValueError("sigmaX must be a non-negative number.")
        
        # Validate sigmaY
        if self.sigmaY is not None and (not isinstance(self.sigmaY, (int, float)) or self.sigmaY < 0):
            raise ValueError("sigmaY must be a non-negative number or None.")
    
    def calculate(self):
        """
        ## calculate (method)
        
        ### Returns:
        
        """
        self.__gaussian_output = GaussianBlur(
            self.tif_file_metadata["image_plt"],
            self.ksize,
            self.sigmaX,
            self.sigmaY if self.sigmaY is not None else self.sigmaX
        )
    
    def export_file(self, 
            output_path: PathLike,
            title: str | None = None,
            figsize: tuple = (10, 10), 
            show_axis: bool = False, 
            colormap: str = "gray", 
            show_colorbar: bool = False, 
            filename_prefix: str = "GAUSSIAN_output",
            dpi: int = 500
        ):
        """
        ## export_file (method)
        Exports the GAUSSIAN filter image as a PNG file with customizable visualization options.
        ### Args:
        output_path (str or Path): Directory where the file will be saved.
            figsize (tuple, optional): Figure size in inches. Defaults to (10, 10).
            show_axis (bool, optional): Whether to display axes. Defaults to False.
            colormap (str, optional): Colormap to apply to the image. Defaults to None.
            show_colorbar (bool, optional): Whether to include a colorbar. Defaults to False.
            filename_prefix (str, optional): Prefix for the output filename. Defaults to "GAUSSIAN_output".
            dpi (int, optional): Resolution of the saved image. Defaults to 500.
        """
        
        #NOTE - Check if GAUSSIAN is processed and store in output property 
        if self.__gaussian_output is None:
            raise ValueError("GAUSSIAN data not computed. Run `calculate()` before exporting.")
        
        # Ensure output path exists
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # if colormap and colormap not in cm.cmap_d:
        #     raise ValueError(f"Invalid colormap: {colormap}")
        
        # Configure and save the figure
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(self.__gaussian_output, cmap=colormap)
        
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
    tif_path = Path.cwd() / "data/TIF_FILE.tif"
    
    calculator = GAUSSIANCalculator(tif_path=tif_path,ksize=(7,7))
    calculator.run(output_path="./", title="Hello")