from pathlib import Path

import cv2
from matplotlib import pyplot as plt

from app.openrs.base import Base
from app.openrs.file_handler import OpenFiles


class GAUSSIANCalculator(Base):
    def __init__(self, files):
        # Check requirment bands
        if files.tif_file is None:
            raise Exception("Message")

        super().__init__(files)
        # Normalize the bands
        self.normalized_bands = files.get_normalize_bands()

        self.image = files.tif_file_metadata["image"]

    def calculate(self, extra_params):
        gaussian = cv2.GaussianBlur(self.image, (13, 13), 0)
        self.gaussian = gaussian

        return gaussian

    def export(self, file_path, title):
        plt.figure(figsize=(10, 10))
        plt.imshow(self.gaussian, cmap="gray")
        plt.title(title)
        plt.axis("off")
        plt.savefig(file_path)
        plt.close()


if __name__ == "__main__":
    tif_file = Path.cwd() / "app/openrs/data/pan_img.tif"
    calculator = GAUSSIANCalculator(OpenFiles(tif_file=tif_file))
    gaussian_image = calculator.calculate()
    plt.figure(figsize=(10, 10))
    plt.imshow(gaussian_image, cmap="gray")
    plt.title("Guassian Filter")
    plt.axis("off")
    plt.show()
