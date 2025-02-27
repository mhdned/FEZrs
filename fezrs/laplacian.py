from pathlib import Path

import cv2
from fastapi import HTTPException, status
from matplotlib import pyplot as plt

from app.openrs.base import Base
from app.openrs.file_handler import OpenFiles


class LAPLACIANCalculator(Base):
    def __init__(self, files):
        # Check requirment bands
        if files.tif_file is None:
            raise Exception("Message")

        super().__init__(files)
        # Normalize the bands
        self.normalized_bands = files.get_normalize_bands()

        self.image = files.tif_file_metadata["image"]

    def calculate(self, extra_params: dict) -> any:
        # Validation extra parameters
        if extra_params is None and type(extra_params) is not dict:
            raise HTTPException(
                detail="you should send value of (n_clusters and random_state), these params are required",
                status_code=status.HTTP_412_PRECONDITION_FAILED,
            )
        if extra_params.get("kernel_size") is None:
            raise HTTPException(
                detail="The kernel_size cant be empty",
                status_code=status.HTTP_412_PRECONDITION_FAILED,
            )

        if (
            type(extra_params["kernel_size"]) is not int
            and extra_params["kernel_size"] / 2 != 1
        ):
            raise HTTPException(
                detail="The kernel_size value should be number and odd",
                status_code=status.HTTP_412_PRECONDITION_FAILED,
            )

        # End validation extra parameters
        kernel_size: int = extra_params["kernel_size"]

        # This calculate may need more params for Sobel argument
        laplacian_image = cv2.Laplacian(self.image, -1, ksize=kernel_size)
        self.laplacian_image = laplacian_image
        return laplacian_image

    def export(self, file_path, title) -> None:
        plt.figure(figsize=(10, 10))
        plt.imshow(self.laplacian_image, cmap="gray")
        plt.title(title)
        plt.axis("off")
        plt.savefig(file_path)
        plt.close()


# Export (on test mode)
if __name__ == "__main__":
    tif_file = Path.cwd() / "app/openrs/data/pan_img.tif"
    calculator = LAPLACIANCalculator(OpenFiles(tif_file=tif_file))
    laplacian_image = calculator.calculate({"kernel_size": 7})
    plt.figure(figsize=(10, 10))
    plt.imshow(laplacian_image, cmap="gray")
    plt.title("Laplacian Filter")
    plt.axis("off")
    plt.show()
