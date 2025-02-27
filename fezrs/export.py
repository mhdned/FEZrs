import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import ndarray


class BaseExport:
    def show(self, input: ndarray, title: str, cmap: cm, use_colorbar: bool = True) -> None:
        """Display the input array as an image."""
        raise NotImplementedError("Subclasses should implement this method")

    def save(self, input: ndarray, title: str, cmap: cm, use_colorbar: bool = True,
             file_path: str = "data/save.png") -> None:
        """Save the input array as an image to the specified file path."""
        raise NotImplementedError("Subclasses should implement this method")


class PlotExport(BaseExport):
    def __init__(self):
        super().__init__()

    def show(self, _input: ndarray, title: str, cmap: cm, use_colorbar: bool = True) -> None:
        """Display the input array as an image with the specified title and colormap."""

        plt.figure(figsize=(15, 10))
        plt.imshow(_input, cmap=cmap)
        plt.title(title)
        if use_colorbar:
            plt.colorbar()
        plt.axis('off')
        plt.show()

    def save(self, _input: ndarray, title: str, cmap: cm, use_colorbar: bool = True,
             file_path: str = "data/save.png") -> None:
        """Save the input array as an image with the specified title and colormap to the given file path."""
        plt.figure(figsize=(15, 10))
        plt.imshow(_input, cmap=cmap)
        plt.title(title)
        if use_colorbar:
            plt.colorbar()
        plt.axis('off')
        plt.savefig(file_path)
        plt.close()
