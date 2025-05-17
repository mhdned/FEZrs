from uuid import uuid4
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class HistogramExportMixin:
    def _add_watermark(self, ax):
        imagebox = OffsetImage(self._logo_watermark, zoom=1, alpha=0.3)
        ab = AnnotationBbox(
            imagebox,
            (0.95, 0.95),
            xycoords="axes fraction",
            frameon=False,
            box_alignment=(1, 1),
        )
        ax.add_artist(ab)

    def _save_histogram_figure(
        self, ax, output_path, filename_prefix, dpi, bbox_inches
    ):
        filename = f"{output_path}/{filename_prefix}_{uuid4().hex}.png"
        ax.figure.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
        plt.close(ax.figure)
        return filename
