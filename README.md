# **FEZrs**

[![DOI](https://zenodo.org/badge/710286874.svg)](https://doi.org/10.5281/zenodo.14938038) ![Downloads](https://static.pepy.tech/badge/FEZrs) ![PyPI](https://img.shields.io/pypi/v/FEZrs?color=blue&label=PyPI&logo=pypi) [![Conda](https://img.shields.io/conda/vn/conda-forge/fezrs)](https://anaconda.org/conda-forge/fezrs) ![License](https://img.shields.io/pypi/l/FEZrs) ![PyPI - Downloads](https://img.shields.io/pypi/dm/FEZrs) ![GitHub last commit](https://img.shields.io/github/last-commit/FEZtool-team/fezrs) ![GitHub stars](https://img.shields.io/github/stars/FEZtool-team/FEZrs?style=social)

**FEZrs** is an advanced Python library developed by [**FEZtool**](https://feztool.com/) for remote sensing applications. It provides a set of powerful tools for image processing, feature extraction, and analysis of geospatial data.

## **Features**

✅ Apply various image filtering techniques (Gaussian, Laplacian, Sobel, Median, Mean)  
✅ Contrast enhancement and edge detection  
✅ Support for geospatial raster data (TIFF)  
✅ Designed for remote sensing and satellite imagery analysis  
✅ Easy integration with FastAPI for web-based processing

## **Installation**

To install FEZrs and its dependencies, use:

```sh
pip install fezrs
```

## **Usage**

Example of applying a Gaussian filter to an image:

```python
from fezrs import EqualizeRGBCalculator

equalize = EqualizeRGBCalculator(
    blue_path="path/to/your/image_band.tif",
    green_path="path/to/your/image_band.tif",
    red_path="path/to/your/image_band.tif",
)

equalize.chart_export(output_path="./your/export/path")
equalize.execute(output_path="./your/export/path")
```

## **Modules**

- `KMeansCalculator`
- `GuassianCalculator`
- `LaplacianCalculator`
- `MeanCalculator`
- `MedianCalculator`
- `SobelCalculator`
- `GLCMCalculator`
- `HSVCalculator`
- `IRHSVCalculator`
- `AdaptiveCalculator`
- `AdaptiveRGBCalculator`
- `EqualizeCalculator`
- `EqualizeRGBCalculator`
- `FloatCalculator`
- `GammaCalculator`
- `GammaRGBCalculator`
- `LogAdjustCalculator`
- `OriginalCalculator`
- `OriginalRGBCalculator`
- `SigmoidAdjustCalculator`
- `PCACalculator`
- `AFVICalculator`
- `BICalculator`
- `NDVICalculator`
- `NDWICalculator`
- `SAVICalculator`
- `UICalculator`
- `SpectralProfileCalculator`

## **Contributing**

We welcome contributions! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

## **Acknowledgment**

Special thanks to [**Chakad Cafe**](https://www.chakadcoffee.com/) for the coffee that kept us fueled during development! ☕

## **License**

This project is licensed under the **Apache-2.0 license**.
