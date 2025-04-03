# Import packages and libraries
import numpy as np
from uuid import uuid4
from pathlib import Path
import matplotlib.pyplot as plt
from skimage.color import rgb2hsv

# Import module and files
from fezrs.base import BaseTool
from fezrs.utils.type_handler import PathLike

class SATURATIONCalculator(BaseTool):
    
    def __init__(self, nir_path: PathLike, blue_path: PathLike, green_path: PathLike):
        super().__init__(nir_path=nir_path, blue_path=blue_path, green_path=green_path)
        self.normalized_bands = self.files_handler.get_normalize_bands()
        
        self.__saturation_output: np.ndarray | None = None
        
    def validate(self):
        pass
    
    def calculate(self):
        nir, blue, green = (self.normalized_bands[band] for band in ("nir", "blue", "green"))
        self.__saturation_output = rgb2hsv(np.dstack((nir, green, blue)))
        self.__saturation_output = self.__saturation_output[:,:,1]
        return self.__saturation_output
    
    def export_file(self,
            output_path: PathLike,
            title: str | None = None,
            figsize: tuple = (10, 5), 
            show_axis: bool = True, 
            colormap: str = None, 
            show_colorbar: bool = True, 
            filename_prefix: str = "SATURATION_output",
            dpi: int = 500,
            grid: bool = True
        ):
        
        if self.__saturation_output is None:
            raise ValueError("SATURATION data not computed. Run `calculate()` before exporting.")
        
        # Ensure output path exists
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # if colormap and colormap not in cm.cmap_d:
        #     raise ValueError(f"Invalid colormap: {colormap}")
        
        # Configure and save the figure
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(self.__saturation_output, cmap=colormap)
        
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
    nir_path = Path.cwd() / "data/NIR.tif"
    blue_path = Path.cwd() / "data/Blue.tif"
    green_path = Path.cwd() / "data/Green.tif"
    
    calculator = SATURATIONCalculator(blue_path=blue_path, green_path=green_path, nir_path=nir_path)
    calculator.run(output_path="./")
