import requests
import datetime
import json
from typing import Dict, Optional, List

# Konfigurasi API OpenWeatherMap
API_KEY = "18c3d2c7a3f97c003f68b32f8dcc3016"
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Koordinat kota-kota di Sulawesi Selatan
SULSEL_CITIES = {
    "Makassar": {"lat": -5.1477, "lon": 119.4327},
    "Parepare": {"lat": -4.0167, "lon": 119.6167},
    "Palopo": {"lat": -2.9833, "lon": 120.2000},
    "Watampone": {"lat": -4.5333, "lon": 120.3333},
    "Sengkang": {"lat": -4.1167, "lon": 120.0167}
}

def test_current_weather_api(city: str = "Makassar") -> Optional[Dict]:
    """Test fungsi untuk mengambil data cuaca terkini."""
    try:
        city_coords = SULSEL_CITIES.get(city)
        if not city_coords:
            print(f"Kota {city} tidak ditemukan dalam daftar")
            return None
            
        url = f"{BASE_URL}/weather"
        params = {
            "lat": city_coords["lat"],
            "lon": city_coords["lon"],
            "appid": API_KEY,
            "units": "metric",
            "lang": "id",
        }
        
        print(f"Mengambil data cuaca untuk {city}...")
        print(f"URL: {url}")
        print(f"Params: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"v Berhasil mengambil data cuaca!")
        print(f"Raw data: {json.dumps(data, indent=2)}")
        
        # Parse data yang diperlukan
        rainfall = 0
        if "rain" in data:
            rainfall = data["rain"].get("1h", 0)
        elif "snow" in data:
            rainfall = data["snow"].get("1h", 0)
            
        parsed_data = {
            "city": city,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.datetime.now().strftime("%H:%M"),
            "rainfall": rainfall,
            "temperature": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
        
        print(f"Parsed data: {json.dumps(parsed_data, indent=2)}")
        return parsed_data
        
    except requests.exceptions.RequestException as e:
        print(f"x Error API request: {str(e)}")
        return None
    except Exception as e:
        print(f"x Error tidak terduga: {str(e)}")
        return None

def test_forecast_api(city: str = "Makassar") -> List[Dict]:
    """Test fungsi untuk mengambil data prakiraan 5 hari."""
    try:
        city_coords = SULSEL_CITIES.get(city)
        if not city_coords:
            print(f"Kota {city} tidak ditemukan dalam daftar")
            return []
            
        url = f"{BASE_URL}/forecast"
        params = {
            "lat": city_coords["lat"],
            "lon": city_coords["lon"],
            "appid": API_KEY,
            "units": "metric",
            "lang": "id",
        }
        
        print(f"📈 Mengambil data prakiraan untuk {city}...")
        print(f"URL: {url}")
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"v Berhasil mengambil data prakiraan!")
        print(f"Total data points: {len(data['list'])}")
        
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
            
            # Agregasi curah hujan (data dalam 3 jam)
            rainfall = entry.get("rain", {}).get("3h", 0)
            daily_data[date_str]["rainfall"] += rainfall
            
            # Kumpulkan temperatur dan kelembaban
            daily_data[date_str]["temperatures"].append(entry["main"]["temp"])
            daily_data[date_str]["humidities"].append(entry["main"]["humidity"])
            
            # Simpan deskripsi cuaca (gunakan yang terdekat dengan tengah hari)
            if 10 <= dt.hour <= 14:
                daily_data[date_str]["descriptions"].append(entry["weather"][0]["description"])
        
        # Format data harian
        forecast_data = []
        for date, values in daily_data.items():
            forecast_data.append({
                "city": city,
                "date": date,
                "rainfall": round(values["rainfall"], 1),
                "temperature": round(sum(values["temperatures"]) / len(values["temperatures"]), 1) if values["temperatures"] else 28.0,
                "humidity": round(sum(values["humidities"]) / len(values["humidities"]), 1) if values["humidities"] else 75.0,
                "description": values["descriptions"][0] if values["descriptions"] else "berawan",
            })
        
        forecast_data = sorted(forecast_data, key=lambda x: x["date"])
        
        print(f"Data prakiraan harian:")
        for day in forecast_data:
            print(f"  {day['date']}: {day['rainfall']}mm, {day['temperature']}°C, {day['humidity']}%")
            
        return forecast_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error API request: {str(e)}")
        return []
    except Exception as e:
        print(f" Error tidak terduga: {str(e)}")
        return []

if __name__ == "__main__":
    print("Testing OpenWeatherMap API...")
    print("=" * 50)
    
    # Test current weather
    current_data = test_current_weather_api("Makassar")
    
    print("\n" + "=" * 50)
    
    # Test forecast data
    forecast_data = test_forecast_api("Makassar")
    print(f"\n Summary:")
    print(f"Current weather: {'v' if current_data else 'x'}")
    print(f"Forecast data: {'v' if forecast_data else 'x'} ({len(forecast_data)} days)")