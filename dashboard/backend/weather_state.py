import datetime
import reflex as rx
from typing import List, Dict, Optional
from config import SULSEL_CITIES
from .weather_service import WeatherService


class WeatherState(rx.State):
    """State management untuk data cuaca dan dashboard."""

    # Data cuaca
    weather_data: List[Dict] = []
    current_weather: Dict = {}

    # Status aplikasi
    is_loading: bool = False
    error_message: str = ""

    # Pengaturan dashboard
    selected_city: str = "Makassar"
    last_updated: str = ""

    # Data untuk charts
    chart_dates: List[str] = []
    rainfall_values: List[float] = []
    temperature_values: List[float] = []
    humidity_values: List[float] = []

    # Statistik
    total_rainfall: float = 0
    avg_temperature: float = 0
    avg_humidity: float = 0
    max_daily_rainfall: float = 0
    rainy_days: int = 0

    def load_weather_data(self, city: str = None):
        """Memuat data cuaca untuk kota yang dipilih."""
        if city:
            self.selected_city = city
        
        self.is_loading = True
        self.error_message = ""
        
        try:
            city_coords = SULSEL_CITIES.get(self.selected_city)
            if not city_coords:
                raise ValueError(f"Kota {self.selected_city} tidak ditemukan")
            
            # Ambil data cuaca terkini
            current_data = WeatherService.fetch_current_weather(
                self.selected_city,
                city_coords["lat"],
                city_coords["lon"],
            )
            
            if current_data:
                self.current_weather = current_data
                self.last_updated = f"{current_data['date']} {current_data['time']} WIB"
            else:
                self.current_weather = WeatherService.get_default_current_weather(self.selected_city)
                self.last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M WIB")
            
            # Ambil data prakiraan 5 hari
            forecast_data = WeatherService.fetch_forecast_data(
                self.selected_city,
                city_coords["lat"],
                city_coords["lon"],
            )
            self.weather_data = forecast_data
            
            # Prepare chart data
            self.prepare_chart_data()
            
            # Calculate statistics
            self.calculate_statistics()
            
        except Exception as e:
            self.error_message = f"Gagal memuat data cuaca: {str(e)}"
            print(f"Error in load_weather_data: {str(e)}")
        
        finally:
            self.is_loading = False

    @rx.var
    def chart_data_rainfall(self) -> List[Dict]:
        """Data untuk chart curah hujan."""
        if not self.chart_dates:
            return []
        return [
            {
                "date": self.format_date_short(date),
                "rainfall": self.rainfall_values[i] if i < len(self.rainfall_values) else 0
            }
            for i, date in enumerate(self.chart_dates)
        ]

    @rx.var
    def chart_data_temp_humidity(self) -> List[Dict]:
        """Data untuk chart temperatur dan kelembapan."""
        if not self.chart_dates:
            return []
        length = min(len(self.chart_dates), len(self.temperature_values), len(self.humidity_values))
        return [
            {
                "date": self.format_date_short(self.chart_dates[i]),
                "temperature": self.temperature_values[i],
                "humidity": self.humidity_values[i],
            }
            for i in range(length)
        ]

    def prepare_chart_data(self):
        """Menyiapkan data untuk chart."""
        if not self.weather_data:
            return
        
        sorted_data = sorted(self.weather_data, key=lambda x: x["date"])
        self.chart_dates = [item["date"] for item in sorted_data]
        self.rainfall_values = [item["rainfall"] for item in sorted_data]
        self.temperature_values = [item["temperature"] for item in sorted_data]
        self.humidity_values = [item["humidity"] for item in sorted_data]

    def calculate_statistics(self):
        """Menghitung nilai statistik cuaca."""
        if not self.weather_data:
            return
        
        self.total_rainfall = round(sum(item["rainfall"] for item in self.weather_data), 1)
        self.avg_temperature = round(sum(item["temperature"] for item in self.weather_data) / len(self.weather_data), 1) if self.weather_data else 0
        self.avg_humidity = round(sum(item["humidity"] for item in self.weather_data) / len(self.weather_data), 1) if self.weather_data else 0
        self.max_daily_rainfall = round(max((item["rainfall"] for item in self.weather_data), default=0), 1)
        self.rainy_days = len([item for item in self.weather_data if item["rainfall"] > 0])

    def load_initial_data(self):
        """Load data awal saat web dibuka."""
        self.load_weather_data()

    def refresh_data(self):
        """Refresh semua data cuaca."""
        self.load_weather_data()

    def change_city(self, city: str):
        """Mengubah kota yang dipilih."""
        self.load_weather_data(city)

    def format_date_short(self, date_str: str) -> str:
        """Format tanggal menjadi MM-DD."""
        try:
            return date_str[-5:]  # Ambil 5 karakter terakhir (MM-DD)
        except:
            return date_str
    
    