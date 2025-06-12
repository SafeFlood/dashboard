import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

# Konfigurasi API OpenWeatherMap
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Validasi API key
# if not API_KEY:
#     raise ValueError(
#         "OPENWEATHER_API_KEY tidak ditemukan! "
#         "Pastikan Anda sudah membuat file .env dan mengisi API key. "
#         "Contoh: OPENWEATHER_API_KEY=your_api_key_here"
#     )

# Hanya error jika sedang run app, bukan saat import oleh reflex export
if __name__ == "__main__" or "RUN_MAIN" in os.environ:
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY tidak ditemukan!")
    
    
BASE_URL = "http://api.openweathermap.org/data/2.5"

print("[DEBUG] OPENWEATHER_API_KEY =", API_KEY)

# Koordinat kota-kota di Sulawesi Selatan
SULSEL_CITIES: Dict[str, Dict[str, float]] = {
    # Kota
    "Makassar": {"lat": -5.1500, "lon": 119.4500},      
    "Parepare": {"lat": -4.0333, "lon": 119.6500},
    "Palopo": {"lat": -2.9925, "lon": 120.1969},

    # Kabupaten
    "Bantaeng": {"lat": -5.4833, "lon": 119.9833},
    "Barru": {"lat": -4.4333, "lon": 119.6833},
    "Bone": {"lat": -4.7000, "lon": 120.1333},
    "Bulukumba": {"lat": -5.4167, "lon": 120.2333},
    "Enrekang": {"lat": -3.5000, "lon": 119.8667},
    "Gowa": {"lat": -5.3167, "lon": 119.7500},
    "Jeneponto": {"lat": -5.6333, "lon": 119.7333},
    "Luwu": {"lat": -2.5577, "lon": 121.3242},
    "Luwu Timur": {"lat": -2.5096, "lon": 120.3978},
    "Luwu Utara": {"lat": -2.6000, "lon": 120.2500},
    "Maros": {"lat": -5.0500, "lon": 119.7167},
    "Pangkajene dan Kepulauan": {"lat": -4.7827, "lon": 119.5506},
    "Pinrang": {"lat": -3.6167, "lon": 119.6000},
    "Sidenreng Rappang": {"lat": -3.8500, "lon": 119.9667},
    "Sinjai": {"lat": -5.2167, "lon": 120.1500},
    "Soppeng": {"lat": -4.3842, "lon": 119.8900},
    "Takalar": {"lat": -5.4167, "lon": 119.5167},
    "Tana Toraja": {"lat": -3.0024, "lon": 119.7966},
    "Toraja Utara": {"lat": -2.9274, "lon": 119.7922},
    "Wajo": {"lat": -4.0000, "lon": 120.1667},
    "Selayar Islands": {"lat": -6.8167, "lon": 120.8000}
}

# Konfigurasi timeout untuk request API
REQUEST_TIMEOUT = 5

# Default values jika API gagal
DEFAULT_TEMPERATURE = 28.5
DEFAULT_HUMIDITY = 75
DEFAULT_DESCRIPTION = "berawan"