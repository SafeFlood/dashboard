import reflex as rx

from ..components import map_container, tile_layer


def south_sulawesi_map_display() -> rx.Component:
    """Render the map display with a tile layer."""
    max_bounds = [[-1.396842, 118.991911], [-7.941256, 122.786092]]
    raster_map_url = rx.color_mode_cond(
        "https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png",
        "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
    )
    return map_container(
            tile_layer(
                url=raster_map_url,
                attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
            ),
            center=[-4.056912, 119.910098],
            max_bounds=max_bounds,
            zoom=6.3,
            scroll_wheel_zoom=True,
            height="100%",
            width="100%",
            border_radius="1em",
        )
