"""Dashboard Curah Hujan Sulawesi Selatan - Main Page."""

import datetime
import reflex as rx
from ..components.card import card
from ..templates import template
from ..backend.weather_state import WeatherState
from ..components.weather_card import (
    weather_stats_cards,
    city_selector,
    current_weather_info,
    refresh_button,
    rainfall_chart,
    temperature_humidity_charts,
)

def _time_data() -> rx.Component:
    """Component untuk menampilkan rentang waktu data."""
    now = datetime.datetime.now()
    future = now + datetime.timedelta(days=5)
    
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=15),
            content=f"{now.strftime('%b %d, %Y')} - {future.strftime('%b %d, %Y')}",
        ),
        rx.text("Prakiraan 5 hari", size="3", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )


def dashboard_header() -> rx.Component:
    """Header dashboard."""
    return rx.hstack(
        rx.hstack(
            rx.heading(
                "Dashboard Prakiraan Cuaca Sulawesi Selatan",
                size="8",
                weight="bold",
                color="#2c3e50",
            ),
            align="center",
            spacing="3",
        ),
        rx.spacer(),
        rx.hstack(
            _time_data(),
            refresh_button(),
            align="center",
            spacing="4",
        ),
        width="100%",
        align="center",
        padding_bottom="4",
    )

def weather_controls() -> rx.Component:
    """Kontrol untuk pemilihan kota dan informasi cuaca terkini."""
    return rx.vstack(
        current_weather_info(),
        city_selector(),
        spacing="4",
        width="100%",
    )

def charts_section() -> rx.Component:
    """Bagian untuk menampilkan grafik curah hujan dan temperatur/kelembapan."""
    return rx.vstack(
        card(
            rx.vstack(
                rx.heading(
                    "Prakiraan Curah Hujan Harian",
                    size="6",
                    weight="medium",
                    color="#2c3e50",
                    margin_bottom="4",
                    
                ),
                rainfall_chart(),
                spacing="4",
                width="100%",
                bg="white",
                padding="6",
                border_radius="lg",
                box_shadow="sm",
            ),
        ),
        card(
            rx.vstack(
                rx.heading(
                    "Prakiraan Temperatur dan Kelembapan",
                    size="6",
                    weight="medium",
                    color="#2c3e50",
                ),
                temperature_humidity_charts(),
                spacing="4",
                width="100%",
            ),
        ),
        spacing="6",
        width="100%",
    )


def footer_info() -> rx.Component:
    """Footer dengan informasi sumber data."""
    return rx.box(
        rx.text(
            "Data cuaca dari OpenWeatherMap API | Dashboard Prakiraan Cuaca Realtime",
            font_size="sm",
            color="gray.500",
            text_align="center",
        ),
        padding_top="8",
        width="100%",
        border_top="1px solid #e2e8f0",

        
    )

def dashboard() -> rx.Component:
    """Dashboard utama aplikasi cuaca."""
    return rx.vstack(
            dashboard_header(),
            
            # Kontrol untuk pilih kota dan refresh
            weather_controls(),
            
            # Weather stats cards
            rx.cond(
            ~WeatherState.is_loading,
            weather_stats_cards(),
            ),
            
            # Menampilkan charts
            rx.cond(
                (~WeatherState.is_loading) & (WeatherState.error_message == ""),
            charts_section(),
            ),

            # Footer informasi
            footer_info(),
            max_width="100%",
            padding="6",
            spacing="6",
            bg="#f8fafc",
        )
