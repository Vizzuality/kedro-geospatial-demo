import numpy as np
import pytest
import rioxarray  # noqa: F401
import xarray as xr
from rasterio.enums import Resampling

from demo.pipelines.preprocessing.nodes import _parse_resampling, resample, to_h3


@pytest.fixture
def raster() -> xr.DataArray:
    """10x10 1 degree per pixel raster"""
    data = np.ones(shape=(10, 10), dtype=np.float32)
    lat, lon = np.linspace(1, 10, num=10), np.linspace(1, 10, num=10)

    raster = xr.DataArray(data, coords={"lat": lat, "lon": lon}, dims=["lat", "lon"])
    raster = raster.rio.set_spatial_dims("lon", "lat")
    raster = raster.rio.write_crs("EPSG:4326")
    return raster


@pytest.fixture
def small_raster() -> xr.DataArray:
    """2x2 10 degrees per pixel raster"""
    data = np.ones(shape=(2, 2), dtype=np.float32)
    lat, lon = [0, 10], [0, 10]
    raster = xr.DataArray(data, coords={"lat": lat, "lon": lon}, dims=["lat", "lon"])
    raster = raster.rio.set_spatial_dims("lon", "lat")
    raster = raster.rio.write_crs("EPSG:4326")
    return raster


def test__parse_resampling():
    assert _parse_resampling("nearest") == Resampling.nearest
    assert _parse_resampling("bilinear") == Resampling.bilinear
    assert _parse_resampling("cubic") == Resampling.cubic
    with pytest.raises(ValueError):
        _parse_resampling("invalid")


def test_resample_is_correct(raster):
    parameters = {"pixel_size": 2, "method": "sum"}
    resampled = resample(raster, parameters)
    assert resampled.rio.shape == (5, 5)
    assert np.all(resampled.values == 4)  # noqa: PLR2004
    assert resampled.rio.crs == raster.rio.crs


def test_to_h3(small_raster):
    """Test that the raster is converted to h3 hexagons."""

    h3df = to_h3(small_raster)
    np.testing.assert_array_equal(h3df.columns, ["value", "cell"])
    # raster to h3 doesn't change the values
    assert all(v == 1 for v in h3df["value"])
    # cells should be at resolution 1, in hexadecimal format, the second digit is the resolution byte
    assert all(cell.startswith("81") for cell in h3df["cell"])


def test_to_h3_with_geometry(small_raster):
    """Test that the raster is converted to h3 hexagons with geometry."""
    h3df = to_h3(small_raster, with_geometry=True)
    np.testing.assert_array_equal(h3df.columns, ["value", "cell", "geometry"])
    # raster to h3 doesn't change the values
    assert all(v == 1 for v in h3df["value"])
    # cells should be at resolution 1, in hexadecimal format, the second digit is the resolution byte
    assert all(cell.startswith("81") for cell in h3df["cell"])
    # geometry should be a polygon
    assert all(geom.geom_type == "Polygon" for geom in h3df["geometry"])
