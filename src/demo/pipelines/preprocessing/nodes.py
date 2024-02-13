import logging
from typing import Any, Dict

import matplotlib.pyplot as plt
import pandas as pd
from h3ronpy.pandas.raster import (
    nearest_h3_resolution,
    raster_to_dataframe,
    raster_to_geodataframe,
)
from rasterio.enums import Resampling
from xarray import DataArray

log = logging.getLogger(__name__)


def _parse_resampling(resampling: str) -> Resampling:
    """Parses the resampling method."""
    if (res := Resampling.__members__.get(resampling)) is not None:
        return res
    else:
        raise ValueError(f"Invalid resampling method: {resampling}")


def resample(
        raster: DataArray,
        parameters: Dict[str, Any],
) -> DataArray:
    """Resamples the raster to the target resolution.
    NOTE: expect square pixels.

    Args:
        parameters: Parameters including the target resolution and the resampling method.
        raster: Tuple of (data, metadata).
    Returns:
        Tuple of (data, metadata) of the resampled raster.
    """
    log.debug(f"{parameters=}")
    curr_pixel_size = raster.rio.transform().a

    new_width = int(raster.rio.width * curr_pixel_size / parameters["pixel_size"])
    new_height = int(raster.rio.height * curr_pixel_size / parameters["pixel_size"])
    return raster.rio.reproject(
        raster.rio.crs,
        shape=(new_height, new_width),
        resampling=_parse_resampling(parameters["method"]),
    )


def clip_to_boundary(raster: DataArray, boundary_params: Dict[str, float]) -> DataArray:
    """Clip the raster to the boundary area.
    Args:
        raster: Tuple of (data, metadata).
        boundary_params: Dict of boundary parameters. Minx, miny, maxx, maxy.
    Returns:
        Raster with the boundary area clipped.
    """
    log.debug(f"Clipping to {boundary_params=}")
    return raster.rio.clip_box(**boundary_params)


def to_h3(raster: DataArray, with_geometry: bool = False) -> pd.DataFrame:
    """Convert a raster to h3 hexagons
    Args:
        raster: raster data.
        with_geometry: If True, returns a GeoDataFrame, else a DataFrame.
    Returns:
        DataFrame of h3 hexagons with the sampled values.
    """
    if len(raster.shape) > 2:  # raster has multiple bands # noqa: PLR2004
        data = raster.to_numpy()[0]
    else:
        data = raster.to_numpy()
    h3_resolution = nearest_h3_resolution(raster.rio.shape, raster.rio.transform())

    to_h3_df = raster_to_geodataframe if with_geometry else raster_to_dataframe
    df = to_h3_df(
        data,
        raster.rio.transform(),
        h3_resolution=h3_resolution,
        nodata_value=raster.rio.nodata,
        compact=False,
    )
    df["cell"] = df["cell"].apply(lambda x: hex(x)[2:])
    return df


def plot(raster: DataArray):
    """Plot the raster."""
    fig, ax = plt.subplots()
    raster.where(raster != raster.rio.nodata).plot(robust=True, cmap="viridis", ax=ax)
    return fig
