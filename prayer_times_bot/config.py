"""
Configuration file for Prayer Times Telegram Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables!")

# AlAdhan API Configuration
ALADHAN_API_URL = os.getenv("ALADHAN_API_URL", "https://api.aladhan.com/v1")
CALCULATION_METHOD = 3  # Muslim World League (Fajr: 18°, Isha: 17°)

# Polish Cities (Name: (latitude, longitude))
POLISH_CITIES = {
    "Warszawa": (52.2297, 21.0122),
    "Kraków": (50.0647, 19.9450),
    "Wrocław": (51.1079, 17.0385),
    "Poznań": (52.4064, 16.9252),
    "Gdańsk": (54.3520, 18.6466),
    "Łódź": (51.7592, 19.4560),
    "Białystok": (53.1325, 23.1688),
    "Lublin": (51.2465, 22.5684),
    "Szczecin": (53.4285, 14.5528),
    "Katowice": (50.2649, 19.0238),
}

# Timezone
POLAND_TIMEZONE = "Europe/Warsaw"

# Message formatting
# Note: Telegram clients control font rendering, but we can use monospace formatting
USE_MONOSPACE = True  # Use monospace blocks for aligned prayer times
