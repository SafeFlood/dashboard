import reflex as rx
from config import SULSEL_CITIES
from ..backend.weather_state import WeatherState

def weathers_cards(
    title: str, 
    value: rx.Var, 
    unit: str, 
    subtitle: str = "Pengukuran periode terakhir",
    icon: str = None
) -> rx.Component:
    """Card Statistik Cuaca."""
    
    return rx.el.div(
        # Header dengan icon dan title
        rx.el.div(
            rx.cond(
                icon is not None,
                rx.el.span(
                    icon,
                    class_name="text-base mr-2",
                ),
                rx.el.div(),
            ),
            rx.el.h3(
                title,
                class_name="text-sm font-medium text-gray-500",
            ),
            class_name="flex items-center mb-3",
        ),
        
        # Value section
        rx.el.div(
            rx.el.span(
                value,
                class_name="text-3xl font-bold text-gray-900",
                style={"font-family": "system-ui, -apple-system, sans-serif"},
            ),
            rx.el.span(
                unit,
                class_name="text-lg text-gray-700 ml-1",
            ),
            class_name="flex items-baseline mb-2",
        ),
        
        # Subtitle
        rx.el.p(
            subtitle,
            class_name="text-xs text-gray-400",
        ),
        
        class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm",
    )


def weather_stats_cards() -> rx.Component:
    """Kumpulan card statistik cuaca untuk dashboard."""

    return rx.el.div(
         weathers_cards(
            "Rata-rata Temperatur",
            WeatherState.avg_temperature,
            "°C",
            "Temperatur rata-rata dari seluruh data",
            "🌡️",
        ),
        weathers_cards(
            "Rata-rata Kelembapan",
            WeatherState.avg_humidity,
            "%",
            "Kelembapan rata-rata dari seluruh data",
            "💧",
        ),
        weathers_cards(
            "Total Curah Hujan",
            WeatherState.total_rainfall,
            "mm",
            "Penjumlahan seluruh data curah hujan",
            "🌧️",
        ),
        weathers_cards(
            "Curah Hujan Maksimal",
            WeatherState.max_daily_rainfall,
            "mm/hari",
            "Curah hujan harian maksimum yang tercatat",
            "⛈️",
        ),
        weathers_cards(
            "Hari Berpotensi Hujan",
            WeatherState.rainy_days,
            "hari",
            "Hari dengan curah hujan > 0 mm",
            "📅",
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6",
    )

def city_selector() -> rx.Component:
    """Selector untuk memilih kota."""

    return rx.hstack(
        rx.text("Pilih Kota:", font_weight="medium", color="#2c3e50"),
        rx.select(
            list(SULSEL_CITIES.keys()),
            value=WeatherState.selected_city,
            on_change=WeatherState.change_city,
            size="3",
            width="200px",
        ),
        align="center",
        spacing="3",
    )


def current_weather_info() -> rx.Component:
    """Informasi cuaca terkini."""

    return rx.callout.root(
        rx.callout.icon(
            rx.text("🌤️", font_size="xl", as_="span"),
        ),
        rx.callout.text(
            rx.text(
                f"{WeatherState.current_weather.get('city', 'Makassar')} - {WeatherState.current_weather.get('description', 'berawan')}",
                font_weight="bold",
                font_size="lg",
                text_transform="capitalize",
                as_="span",
                display="block",
                margin_bottom="1",
            ),
            rx.text(
                f"Temperatur: {WeatherState.current_weather.get('temperature', 28)}°C | "
                f"Kelembapan: {WeatherState.current_weather.get('humidity', 75)}% | "
                f"Terakhir diperbarui: {WeatherState.last_updated}",
                font_size="sm",
                as_="span",
                display="block",
            ),
        ),
        color_scheme="blue",
        variant="soft",
        size="2",
        width="100%",
    )

def refresh_button() -> rx.Component:
    """Tombol refresh data."""
    
    return rx.button(
        rx.cond(
            WeatherState.is_loading,
            rx.hstack(
                rx.spinner(size="1"),
                rx.text("Memuat..."),
                spacing="2",
            ),
            rx.hstack(
                rx.icon("rotate_cw", size=16),
                rx.text("Refresh"),
                spacing="2",
            ),
        ),
        on_click=WeatherState.refresh_data,
        disabled=WeatherState.is_loading,
        size="3",
        color_scheme="blue",
    )


def rainfall_chart() -> rx.Component:
    """Chart untuk curah hujan."""
    
    return rx.recharts.area_chart(
        rx.recharts.area(
            data_key="rainfall",
            type="natural",
            stroke="url(#colorRainfallStroke)",
            fill="url(#colorRainfall)",
            stroke_width=3,
            dot=False,
            active_dot={
                "r": 6,
                "fill": "#1e40af",
                "stroke": "white",
                "strokeWidth": 3,
                "filter": "drop-shadow(0 2px 4px rgba(0,0,0,0.1))",
            },
        ),
        rx.recharts.x_axis(
            data_key="date",
            tick_line=False,
            axis_line=False,
            tick_margin=10,
            tick_count=10,
            interval="preserveStartEnd",
            tick_size=5,
            height=40,
            custom_attrs={
                "fontSize": "12px", 
                "fill": "#64748b",
            },
            min_tick_gap=16,
        ),
        rx.recharts.y_axis(
            label={"value": "Curah Hujan (mm)", "angle": -90, "position": "insideLeft", "dy": 50}

        ),
        rx.recharts.cartesian_grid(
            stroke_dasharray="2 4",
            vertical=False,
            horizontal=True,
            stroke="#e5e7eb",
            stroke_width=1,
        ),
        rx.recharts.graphing_tooltip(
            content_style={
                **TOOLTIP_PROPS["content_style"],
                "background": "rgba(255, 255, 255, 0.95)",
                "backdrop_filter": "blur(8px)",
                "border": "1px solid #e2e8f0",
                "border_radius": "8px",
                "box_shadow": "0 10px 25px rgba(0, 0, 0, 0.1)",
            },
            item_style=TOOLTIP_PROPS["item_style"],
            label_style=TOOLTIP_PROPS["label_style"],
            cursor={
                "stroke": "#cbd5e1",
                "strokeWidth": 1,
                "strokeDasharray": "4 4",
            },
        ),
        
        # Styling Gradients
        rx.el.defs(
            # Gradient untuk fill area
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="0%",
                    stop_color="#3b82f6",
                    stop_opacity=0.6,
                ),
                rx.el.stop(
                    offset="50%",
                    stop_color="#60a5fa",
                    stop_opacity=0.3,
                ),
                rx.el.stop(
                    offset="100%",
                    stop_color="#93c5fd",
                    stop_opacity=0.05,
                ),
                id="colorRainfall",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
            # Gradient untuk stroke line
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="0%",
                    stop_color="#1e40af",
                    stop_opacity=1,
                ),
                rx.el.stop(
                    offset="50%",
                    stop_color="#3b82f6",
                    stop_opacity=0.9,
                ),
                rx.el.stop(
                    offset="100%",
                    stop_color="#60a5fa",
                    stop_opacity=0.8,
                ),
                id="colorRainfallStroke",
                x1="0",
                y1="0",
                x2="1",
                y2="0",
            ),
        ),
        rx.recharts.tooltip(),
        data=WeatherState.chart_data_rainfall,
        width="100%",
        height=400,
        margin={
                "top": 20,
                "right": 20,
                "left": 20,
                "bottom": 5,
        },

    )


def temperature_humidity_charts() -> rx.Component:
    """Charts untuk temperatur dan kelembaban dalam dua kolom terpisah."""
    
    # Chart untuk Temperatur (kolom kiri)
    temperature_chart = rx.recharts.area_chart(
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3",
            vertical=False,
            stroke="#e5e7eb",
        ),
        rx.recharts.graphing_tooltip(
            content_style=TOOLTIP_PROPS["content_style"],
            item_style=TOOLTIP_PROPS["item_style"],
            label_style=TOOLTIP_PROPS["label_style"],
            cursor={
                "stroke": "#d1d5db",
                "strokeWidth": 1,
            },
        ),
        rx.recharts.x_axis(
            data_key="date",
            tick_line=False,
            axis_line=False,
            tick_margin=10,
            tick_count=10,
            interval="preserveStartEnd",
            tick_size=5,
            height=40,
            custom_attrs={"fontSize": "12px"},
            min_tick_gap=16,
        ),
        rx.recharts.y_axis(
            label={"value": "Temperatur (°C)", "angle": -90, "position": "insideLeft", "dy": 50}
        ),
        rx.recharts.area(
            data_key="temperature",
            type_="natural",
            stroke="#e74c3c",
            fill="url(#colorTemp)",
            stroke_width=2,
            dot=False,
            active_dot={
                "r": 4,
                "fill": "#e74c3c",
                "stroke": "white",
                "strokeWidth": 2,
            },
        ),
        rx.el.defs(
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="5%",
                    stop_color="#e74c3c",
                    stop_opacity=0.3,
                ),
                rx.el.stop(
                    offset="95%",
                    stop_color="#e74c3c",
                    stop_opacity=0,
                ),
                id="colorTemp",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
        ),
        data=WeatherState.chart_data_temp_humidity,
        height=300,
        margin={
            "top": 10,
            "right": 20,
            "left": 20,
            "bottom": 0,
        },
    )
    
    # Chart untuk Humidity (kolom kanan)
    humidity_chart = rx.recharts.area_chart(
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3",
            vertical=False,
            stroke="#e5e7eb",
        ),
        rx.recharts.graphing_tooltip(
            content_style=TOOLTIP_PROPS["content_style"],
            item_style=TOOLTIP_PROPS["item_style"],
            label_style=TOOLTIP_PROPS["label_style"],
            cursor={
                "stroke": "#d1d5db",
                "strokeWidth": 1,
            },
        ),
        rx.recharts.x_axis(
            data_key="date",
            tick_line=False,
            axis_line=False,
            tick_margin=10,
            tick_count=10,
            interval="preserveStartEnd",
            tick_size=5,
            height=40,
            custom_attrs={"fontSize": "12px"},
            min_tick_gap=16,
        ),
        rx.recharts.y_axis(
            label={"value": "Kelembapan (%)", "angle": -90, "position": "insideLeft", "dy": 50}
        ),
        rx.recharts.area(
            data_key="humidity",
            type_="natural",
            stroke="#2ecc71",
            fill="url(#colorHum)",
            stroke_width=2,
            dot=False,
            active_dot={
                "r": 4,
                "fill": "#2ecc71",
                "stroke": "white",
                "strokeWidth": 2,
            },
        ),
        rx.el.defs(
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="5%",
                    stop_color="#2ecc71",
                    stop_opacity=0.3,
                ),
                rx.el.stop(
                    offset="95%",
                    stop_color="#2ecc71",
                    stop_opacity=0,
                ),
                id="colorHum",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
        ),
        data=WeatherState.chart_data_temp_humidity,
        height=300,
        margin={
            "top": 10,
            "right": 20,
            "left": 20,
            "bottom": 0,
        },
    )
    
    # Layout dua kolom
    return rx.hstack(
        rx.vstack(
            rx.heading("Temperatur", size="4", margin_bottom="10px"),
            temperature_chart,
            width="50%",
            spacing="2",
        ),
        rx.vstack(
            rx.heading("Kelembapan", size="4", margin_bottom="10px"),
            humidity_chart,
            width="50%",
            spacing="2",
        ),
        width="100%",
        spacing="4",
    )

# Tooltip properties untuk charts
TOOLTIP_PROPS = {
    "separator": ": ",
    "cursor": False,
    "is_animation_active": False,
    "label_style": {"fontWeight": "500"},
    "item_style": {
        "color": "currentColor",
        "display": "flex",
        "paddingBottom": "0px",
        "justifyContent": "flex-start",
        "textTransform": "capitalize",
    },
    "content_style": {
        "borderRadius": "5px",
        "boxShadow": "0px 2px 6px 0px rgba(0, 0, 0, 0.1)",
        "fontSize": "0.75rem",
        "lineHeight": "1rem",
        "fontWeight": "500",
        "minWidth": "8rem",
        "width": "auto",
        "padding": "0.375rem 0.625rem",
        "backgroundColor": "white",
        "border": "1px solid #e2e8f0",
    },
}