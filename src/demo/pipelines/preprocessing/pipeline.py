"""
This is a boilerplate pipeline 'general_preprocessing'
generated using Kedro 0.19.2
"""

from kedro.pipeline import Pipeline, node, pipeline

from demo.pipelines.preprocessing.nodes import (
    clip_to_boundary,
    plot,
    resample,
    to_h3,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=resample,
            inputs=["USDA_soil_order", "params:resampling"],
            outputs="USDA_soil_order_resampled",
        ),
        node(
            func=clip_to_boundary,
            inputs=["USDA_soil_order_resampled", "params:bbox"],
            outputs="USDA_soil_order_clipped",
        ),
        node(
            func=to_h3,
            inputs=["USDA_soil_order_clipped"],
            outputs="USDA_soil_order_h3",
            name="to_h3_parquet_node",
        ),
        node(
            func=to_h3,
            inputs=["USDA_soil_order_clipped", "params:h3_with_geometry"],
            outputs="USDA_soil_order_h3_geo",
            name="to_h3_geo_node",
        ),
        node(
            func=plot,
            inputs=["USDA_soil_order_clipped"],
            outputs="usda_soils_plot",
        ),
    ])
