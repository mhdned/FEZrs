from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from fastapi import HTTPException, status
from .file_handler import OpenFiles

class KMEANSCalculator:
    """K-Means clustering for remote sensing analysis."""

    def __init__(self, files: OpenFiles):
        if files.nir_band is None:
            raise ValueError("NIR band is required for KMeans clustering.")
        self.files = files
        self.nir_band_metadata = files.nir_metadata
        self.nir = files.nir_band
        self.kmeans = None

    def calculate(self, extra_params: dict):
        if not isinstance(extra_params, dict) or "n_clusters" not in extra_params or "random_state" not in extra_params:
            raise HTTPException(
                detail="Provide 'n_clusters' and 'random_state' as parameters.",
                status_code=status.HTTP_412_PRECONDITION_FAILED,
            )

        n_clusters = extra_params["n_clusters"]
        random_state = extra_params["random_state"]

        image_reshape = self.nir.reshape(
            self.nir_band_metadata["width"] * self.nir_band_metadata["height"], 1
        )

        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
        kmeans.fit(image_reshape)

        clusterd_image = kmeans.cluster_centers_[kmeans.labels_].reshape(
            self.nir_band_metadata["height"], self.nir_band_metadata["width"]
        )

        self.kmeans = clusterd_image
        return self.kmeans

    def export(self, file_path: str, title: str):
        plt.figure(figsize=(10, 10))
        plt.title(title)
        plt.imshow(self.kmeans, cmap="viridis")
        plt.axis("off")
        plt.savefig(file_path)
        plt.close()
