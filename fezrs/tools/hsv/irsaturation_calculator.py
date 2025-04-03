# Import packages and libraries
import numpy as np
from skimage.color import rgb2hsv
from uuid import uuid4
from pathlib import Path
from matplotlib import pyplot as plt

# Import module and files
from fezrs.base import BaseTool
from fezrs.utils.type_handler import PathLike

class IRSATURATIONCalculator(BaseTool):
    def __init__(self, red_path: PathLike, swir1_path: PathLike, swir2_path: PathLike):
        
        super().__init__(red_path=red_path, swir1_path=swir1_path, swir2_path=swir2_path)
        self.normalized_bands = self.files_handler.get_normalize_bands()
        
        self.__irsaturation_output: np.ndarray | None = None
        
    def validate(self):
        pass
    
    def calculate(self):
        red, swir1, swir2 = (self.normalized_bands[band] for band in ("red", "swir1", "swir2"))
        self.__irsaturation_output = rgb2hsv(np.dstack((swir2, swir1, red)))
        self.__irsaturation_output = self.__irsaturation_output[:,:,1]
        return self.__irsaturation_output
    
    def export_file(self,
            output_path: PathLike,
            title: str | None = None,
            figsize: tuple = (10, 5), 
            show_axis: bool = True, 
            colormap: str = None, 
            show_colorbar: bool = True,
            filename_prefix: str = "IRSATURATION_output",
            dpi: int = 500,
            grid: bool = False
        ):
        if self.__irsaturation_output is None:
            raise ValueError("IRSATURATION data not computed. Run `calculate()` before exporting.")
        
        # Ensure output path exists
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # if colormap and colormap not in cm.cmap_d:
        #     raise ValueError(f"Invalid colormap: {colormap}")
        
        # Configure and save the figure
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(self.__irsaturation_output, cmap=colormap)
        
        plt.grid(grid)
        
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
    red_path = Path.cwd() / "data/Red.tif"
    swir1_path = Path.cwd() / "data/SWIR1.tif"
    swir2_path = Path.cwd() / "data/SWIR2.tif"
    
    calculator = IRSATURATIONCalculator(red_path=red_path, swir1_path=swir1_path, swir2_path=swir2_path)
    calculator.run(output_path="./")