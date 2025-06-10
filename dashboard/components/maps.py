import reflex as rx
class MapContainer(rx.NoSSRComponent):
    library = "react-leaflet"
    tag = "MapContainer"
    center: rx.Var[list]
    zoom: rx.Var[float]
    scroll_wheel_zoom: rx.Var[bool]
    min_zoom: rx.Var[float] = 7.5
    max_bounds: rx.Var[list] = None

    lib_dependencies: list[str] = [
        "react",
        "react-dom",
        "leaflet",
    ]

    def add_imports(self):
        return {"": ["leaflet/dist/leaflet.css"]}

class TileLayer(rx.NoSSRComponent):
    library = "react-leaflet"
    tag = "TileLayer"
    url: rx.Var[str]

class CircleMarker(rx.NoSSRComponent):
    library = "react-leaflet"
    tag = "CircleMarker"
    center: rx.Var[list]  
    radius: rx.Var[int] = 5  
    color: rx.Var[str] = "blue"
    fill_color: rx.Var[str] = "blue"
    fill_opacity: rx.Var[float] = 0.6
    weight: rx.Var[int] = 1  
    
map_container = MapContainer.create
tile_layer = TileLayer.create
circle_marker = CircleMarker.create

def map_with_circle_points():
    return map_container(
        tile_layer(
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        ),
        circle_marker(
            center=[51.505, -0.09],
            radius=10,
            color="red",
            fill_color="red",
            fill_opacity=0.6,
        ),
        center=[51.505, -0.09],
        zoom=13,
        scroll_wheel_zoom=True,
        style={"height": "400px", "width": "100%"}
    )