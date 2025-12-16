"""
AlAdhan API Service for fetching Islamic prayer times
API Documentation: https://aladhan.com/prayer-times-api
"""
import aiohttp
from datetime import datetime
from typing import Dict, Optional, Tuple
import logging

from config import ALADHAN_API_URL, CALCULATION_METHOD

logger = logging.getLogger(__name__)


class AlAdhanAPIError(Exception):
    """Custom exception for AlAdhan API errors"""
    pass


class AlAdhanAPI:
    """Service for interacting with AlAdhan Prayer Times API"""

    def __init__(self, api_url: str = ALADHAN_API_URL, method: int = CALCULATION_METHOD):
        """
        Initialize AlAdhan API client

        Args:
            api_url: Base URL for AlAdhan API
            method: Calculation method (3 = Muslim World League)
        """
        self.api_url = api_url
        self.method = method
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def get_timings_by_coordinates(
        self,
        latitude: float,
        longitude: float,
        date: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Get prayer timings for specific coordinates

        Args:
            latitude: Location latitude
            longitude: Location longitude
            date: Date in DD-MM-YYYY format (default: today)

        Returns:
            Dictionary with prayer times

        Raises:
            AlAdhanAPIError: If API request fails
        """
        if date is None:
            date = datetime.now().strftime("%d-%m-%Y")

        url = f"{self.api_url}/timings/{date}"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "method": self.method,
        }

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"AlAdhan API error: {response.status} - {error_text}")
                        raise AlAdhanAPIError(f"API returned status {response.status}")

                    data = await response.json()

                    if data.get("code") != 200:
                        raise AlAdhanAPIError(f"API error: {data.get('status', 'Unknown error')}")

                    return data["data"]["timings"]

        except aiohttp.ClientError as e:
            logger.error(f"Network error calling AlAdhan API: {e}")
            raise AlAdhanAPIError(f"Ошибка сети: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise AlAdhanAPIError(f"Неожиданная ошибка: {str(e)}")

    async def get_timings_by_city(
        self,
        city: str,
        country: str = "Poland",
        date: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Get prayer timings for a specific city

        Args:
            city: City name
            country: Country name (default: Poland)
            date: Date in DD-MM-YYYY format (default: today)

        Returns:
            Dictionary with prayer times

        Raises:
            AlAdhanAPIError: If API request fails
        """
        if date is None:
            date = datetime.now().strftime("%d-%m-%Y")

        url = f"{self.api_url}/timingsByCity/{date}"
        params = {
            "city": city,
            "country": country,
            "method": self.method,
        }

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"AlAdhan API error: {response.status} - {error_text}")
                        raise AlAdhanAPIError(f"API returned status {response.status}")

                    data = await response.json()

                    if data.get("code") != 200:
                        raise AlAdhanAPIError(f"API error: {data.get('status', 'Unknown error')}")

                    return data["data"]["timings"]

        except aiohttp.ClientError as e:
            logger.error(f"Network error calling AlAdhan API: {e}")
            raise AlAdhanAPIError(f"Ошибка сети: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise AlAdhanAPIError(f"Неожиданная ошибка: {str(e)}")

    async def get_monthly_calendar(
        self,
        latitude: float,
        longitude: float,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> list:
        """
        Get prayer timings for entire month

        Args:
            latitude: Location latitude
            longitude: Location longitude
            month: Month number (default: current month)
            year: Year (default: current year)

        Returns:
            List of daily prayer times

        Raises:
            AlAdhanAPIError: If API request fails
        """
        now = datetime.now()
        if month is None:
            month = now.month
        if year is None:
            year = now.year

        url = f"{self.api_url}/calendar/{year}/{month}"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "method": self.method,
        }

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"AlAdhan API error: {response.status} - {error_text}")
                        raise AlAdhanAPIError(f"API returned status {response.status}")

                    data = await response.json()

                    if data.get("code") != 200:
                        raise AlAdhanAPIError(f"API error: {data.get('status', 'Unknown error')}")

                    return data["data"]

        except aiohttp.ClientError as e:
            logger.error(f"Network error calling AlAdhan API: {e}")
            raise AlAdhanAPIError(f"Ошибка сети: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise AlAdhanAPIError(f"Неожиданная ошибка: {str(e)}")


# Global API instance
api = AlAdhanAPI()
