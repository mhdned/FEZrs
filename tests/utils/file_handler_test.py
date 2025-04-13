import pytest
from unittest import mock
import numpy as np

from fezrs.utils.file_handler import _load_image


def test_load_image_none_path():
    assert _load_image(None) is None


@mock.patch("fezrs.utils.file_handler.os.path.exists", return_value=True)
@mock.patch(
    "fezrs.utils.file_handler.io.imread", return_value=np.array([[1, 2], [3, 4]])
)
def test_load_image_valid_path(mock_imread, mock_exists):
    result = _load_image("image.tif")
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, np.array([[1, 2], [3, 4]], dtype=float))


@mock.patch("fezrs.utils.file_handler.os.path.exists", return_value=False)
def test_load_image_file_not_found(mock_exists):
    with pytest.raises(FileNotFoundError):
        _load_image("nonexistent.jpg")
