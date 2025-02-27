import matplotlib.pyplot as plt
from .file_handler import OpenFiles
import numpy as np
from skimage.feature import graycomatrix, graycoprops

class CONSTRASTCalculator:
    """Calculates image contrast using GLCM (Gray-Level Co-occurrence Matrix)."""

    def __init__(self, files: OpenFiles):
        if files.nir_band is None:
            raise ValueError("NIR band is required for contrast calculation.")
        self.files = files
        self.nir = files.nir_band

    def calculate(self, extra_params=None):
        """Calculate contrast using GLCM."""
        gray_image = np.uint8(self.nir / np.max(self.nir) * 255)  # Normalize to 8-bit
        glcm = graycomatrix(gray_image, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        return contrast

    def export(self, file_path: str, title: str):
        plt.figure(figsize=(10, 10))
        plt.title(title)
        plt.imshow(self.nir, cmap="gray")
        plt.axis("off")
        plt.savefig(file_path)
        plt.close()
