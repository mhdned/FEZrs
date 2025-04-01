# Import packages and libraries
import numpy as np
from pathlib import Path
from random import random
from skimage.color import rgb2hsv
from matplotlib import pyplot as plt

# Import module and files
from fezrs.base import BaseTool

# Calculator class
class HSVCalculator(BaseTool):
    """description
    """
    def __init__(self, nir_path, blue_path, green_path):
        """description

        Args:
            nir_path (_type_): _description_
            blue_path (_type_): _description_
            green_path (_type_): _description_
        """
        super().__init__(nir_path=nir_path, blue_path=blue_path, green_path=green_path)
        self.normalized_bands = self.files_handler.get_normalize_bands()
        self.__hsv_output = None

    def validate(self):
        pass

    #TODO - Add comment and split sections from eachother
    def calculate(self):
        nir = self.normalized_bands["nir"]
        blue = self.normalized_bands["blue"]
        green = self.normalized_bands["green"]

        image_hsv = np.dstack((nir, green, blue))
        self.hsv = rgb2hsv(image_hsv)
        return self.hsv

    def export(self, output_path: str):
        #NOTE - Check if HSV is processed and store in output property 
        if self.__hsv_output is None:
            raise "HSV data not computed. Run `calculate()` before exporting."

        #TODO - Add validation for output_path parameter
        
        #TODO - Made some values dynamically and receive it as parameters from the user
        plt.figure(figsize=(10, 5))
        plt.imshow(self.__hsv_output)
        plt.axis("off")
        plt.colorbar()
        plt.savefig(output_path)
        plt.close()

#NOTE - These block code for test the tools, delete before publish product
if __name__ == "__main__":
    nir_path = Path.cwd() / "data/NIR.tif"
    blue_path = Path.cwd() / "data/Blue.tif"
    green_path = Path.cwd() / "data/Green.tif"
    
    calculator = HSVCalculator(blue_path=blue_path, green_path=green_path, nir_path=nir_path)
    hsv = calculator.calculate()
    plt.figure(figsize=(20, 10))
    plt.imshow(hsv)
    plt.colorbar()
    plt.savefig(f'./HSV_output_{int(random()*10000)}.png')
    plt.close()
