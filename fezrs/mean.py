from pathlib import Path

import cv2
from matplotlib import pyplot as plt

from app.openrs.base import Base
from app.openrs.file_handler import OpenFiles


class MEANCalculator(Base):
    """
    MEAN calculator class
    """

    def __init__(self, files: OpenFiles):
        # Check requirment bands
        if files.tif_file is None:
            raise Exception("Message")
        super().__init__(files)
        # Normalize the bands
        self.normalized_bands = files.get_normalize_bands()

        self.image = files.tif_file_metadata["image"]

    def calculate(self, extra_params: dict):
        self.mean_image = cv2.blur(self.image, (9, 9))

        return self.mean_image

    def export(self, file_path: Path, title: str):
        plt.figure(figsize=(10, 10))
        plt.imshow(self.mean_image, cmap="gray")
        plt.title(title)
        plt.axis("off")
        plt.savefig(file_path)
        plt.close()


# Export (on test mode)
if __name__ == "__main__":
    tif_file = Path.cwd() / "app/openrs/data/pan_img.tif"
    calculator = MEANCalculator(OpenFiles(tif_file=tif_file))
    mean_filter = calculator.calculate(None)
    plt.figure(figsize=(10, 10))
    plt.imshow(mean_filter, cmap="gray")
    plt.title("Mean Filter")
    plt.axis("off")
    plt.show()
