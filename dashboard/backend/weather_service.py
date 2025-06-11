import datetime
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from config import API_KEY, BASE_URL, REQUEST_TIMEOUT, DEFAULT_TEMPERATURE, DEFAULT_HUMIDITY, DEFAULT_DESCRIPTION


@dataclass
class WeatherData:
    """Data class untuk menyimpan informasi cuaca."""
    date: str
    city: str
    rainfall: float
    temperature: float
    humidity: float
    description: str = ""


class WeatherService:
    """Service class untuk mengambil data cuaca dari OpenWeatherMap API."""
    
    @staticmethod
    def fetch_current_weather(city: str, lat: float, lon: float) -> Optional[Dict]:
        """Mengambil data cuaca terkini dari OpenWeatherMap API."""
        try:
            url = f"{BASE_URL}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "lang": "id",
            }
            
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Mengambil curah hujan dari data
            rainfall = 0
            if "rain" in data:
                rainfall = data["rain"].get("1h", 0)
            elif "snow" in data:
                rainfall = data["snow"].get("1h", 0)
                
            return {
                "city": city,
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.datetime.now().strftime("%H:%M"),
                "rainfall": rainfall,
                "temperature": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
                
        except Exception as e:
            print(f"Error fetching current weather: {str(e)}")
            return None

    @staticmethod
    def fetch_forecast_data(city: str, lat: float, lon: float) -> List[Dict]:
        """Mengambil data prakiraan 5 hari dari OpenWeatherMap API dan mengagregasinya per hari."""
        try:
            url = f"{BASE_URL}/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "lang": "id",
            }
            
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            # Kelompokkan data per hari
            daily_data = {}
            for entry in data["list"]:
                dt = datetime.datetime.fromtimestamp(entry["dt"])
                date_str = dt.strftime("%Y-%m-%d")
                
                if date_str not in daily_data:
                    daily_data[date_str] = {
                        "rainfall": 0,
                        "temperatures": [],
                        "humidities": [],
                        "descriptions": [],
                    }
                
                # Agregasi curah hujan
                rainfall = entry.get("rain", {}).get("3h", 0)
                daily_data[date_str]["rainfall"] += rainfall
                
                # Kumpulkan temperatur dan kelembapan
                daily_data[date_str]["temperatures"].append(entry["main"]["temp"])
                daily_data[date_str]["humidities"].append(entry["main"]["humidity"])
                
                # Simpan deskripsi cuaca (gunakan yang terdekat dengan tengah hari)
                if 10 <= dt.hour <= 14:
                    daily_data[date_str]["descriptions"].append(entry["weather"][0]["description"])
            
            # Format data harian
            historical_data = []
            for date, values in daily_data.items():
                historical_data.append({
                    "city": city,
                    "date": date,
                    "rainfall": round(values["rainfall"], 1),
                    "temperature": round(sum(values["temperatures"]) / len(values["temperatures"]), 1) if values["temperatures"] else DEFAULT_TEMPERATURE,
                    "humidity": round(sum(values["humidities"]) / len(values["humidities"]), 1) if values["humidities"] else DEFAULT_HUMIDITY,
                    "description": values["descriptions"][0] if values["descriptions"] else DEFAULT_DESCRIPTION,
                })
            
            return sorted(historical_data, key=lambda x: x["date"])
                
        except Exception as e:
            print(f"Error fetching forecast data: {str(e)}")
            return []

    @staticmethod
    def get_default_current_weather(city: str) -> Dict:
        """Mengembalikan data cuaca default jika API gagal."""
        return {
            "city": city,
            "temperature": DEFAULT_TEMPERATURE,
            "humidity": DEFAULT_HUMIDITY,
            "description": DEFAULT_DESCRIPTION,
            "rainfall": 0,
        }