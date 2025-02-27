from pathlib import Path

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

from app.openrs.base import Base
from app.openrs.exceptions.OException import OException
from app.openrs.export import PlotExport
from app.openrs.file_handler import OpenFiles


class KMeansCalculator(Base):
    def __init__(self, files: OpenFiles):
        if files.nir_band is None:
            raise Exception("Nir band are required")
        super().__init__(files)
        self.normalized_bands = self.files.get_normalize_bands()
        self.clusterd_image = None

    def calculate(self, extra_params: dict):
        self.normalized_nir = self.files.nir_band
        row = self.normalized_nir.shape[0]
        col = self.normalized_nir.shape[1]
        X = self.normalized_nir.reshape((row * col, 1))
        kmeans = KMeans(n_clusters=4, random_state=0)
        kmeans.fit(X)
        cluster_centers = kmeans.cluster_centers_
        cluster_labels = kmeans.labels_
        self.clusterd_image = cluster_centers[cluster_labels].reshape(row, col)
        return self.clusterd_image

    def export(self, file_path: Path, title: str):
        if self.clusterd_image is None:
            raise OException("KMeans has not been calculated. Call 'calculate' first.")

        plt.figure(figsize=(15, 10))
        plt.imshow(self.clusterd_image)
        plt.title(title)
        plt.colorbar()
        plt.axis("off")
        plt.savefig(file_path)
        plt.close()


if __name__ == "__main__":
    nir_path = Path.cwd() / "app/openrs/data/NIR(1).tif"

    calculator = KMeansCalculator(OpenFiles(nir_path=nir_path))
    kmeans = calculator.calculate()
    plot_export = PlotExport()
    calculator.export("hello", title="NDVI Image")
