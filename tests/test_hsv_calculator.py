import pytest
import numpy as np
from pathlib import Path
from fezrs.tools.hsv.hsv_calculator import HSVCalculator

# Define test data paths
TEST_DATA_DIR = Path(__file__).parent / "sample-data"
NIR_PATH = TEST_DATA_DIR / "NIR.tif"
BLUE_PATH = TEST_DATA_DIR / "Blue.tif"
GREEN_PATH = TEST_DATA_DIR / "Green.tif"

@pytest.fixture
def hsv_calculator():
    """Fixture to initialize HSVCalculator"""
    return HSVCalculator(nir_path=NIR_PATH, blue_path=BLUE_PATH, green_path=GREEN_PATH)

def test_calculate(hsv_calculator):
    """Test if HSV calculation runs without errors"""
    hsv_result = hsv_calculator.calculate()
    assert isinstance(hsv_result, np.ndarray), "Output should be a NumPy array"

def test_export(hsv_calculator, tmp_path: Path | str = "./tests"):
    """Test export functionality"""
    output_file = f"{tmp_path}/output"
    hsv_calculator.calculate()
    result = hsv_calculator.export_file(output_path=output_file)
    assert Path(result).exists(), "Exported file should exist"
