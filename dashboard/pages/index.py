"""Main Landing Page Dashboard Curah Hujan Sulawesi Selatan."""

import reflex as rx
from .dashboard import dashboard
from ..backend.weather_state import WeatherState
from ..templates import template

@template(route="/", title="Overview", on_load=WeatherState.load_weather_data)

def index() -> rx.Component:
    return rx.vstack(
        dashboard(),
        width="100%",
        align="center",
        padding="4",
    )
