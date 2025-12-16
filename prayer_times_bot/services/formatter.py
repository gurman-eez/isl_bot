"""
Message Formatter Service
Formats prayer times and other messages in Russian with monospace styling
"""
from datetime import datetime
from typing import Dict, Optional, List
import pytz

from config import POLAND_TIMEZONE


class MessageFormatter:
    """Formats bot messages in Russian with mobile-first design"""

    # Russian prayer names
    PRAYER_NAMES = {
        "Fajr": "Фаджр",
        "Sunrise": "Восход",
        "Dhuhr": "Зухр",
        "Asr": "Аср",
        "Maghrib": "Магриб",
        "Isha": "Иша",
        "Midnight": "Полночь",
    }

    # Emojis for prayers
    PRAYER_EMOJIS = {
        "Fajr": "🌅",
        "Sunrise": "☀️",
        "Dhuhr": "🌞",
        "Asr": "🌤",
        "Maghrib": "🌆",
        "Isha": "🌙",
    }

    @staticmethod
    def format_daily_times(
        timings: Dict[str, str],
        city: Optional[str] = None,
        date: Optional[datetime] = None
    ) -> str:
        """
        Format daily prayer times in Russian with monospace alignment

        Args:
            timings: Prayer times dictionary from AlAdhan API
            city: City name (optional)
            date: Date object (default: today)

        Returns:
            Formatted message string with HTML markup
        """
        if date is None:
            date = datetime.now(pytz.timezone(POLAND_TIMEZONE))

        # Header
        location_line = f"📍 <b>{city}</b>\n" if city else ""
        date_str = date.strftime("%d.%m.%Y")
        weekday = MessageFormatter._get_russian_weekday(date)

        header = f"""🕌 <b>Время намаза</b>
{location_line}📅 {weekday}, {date_str}

"""

        # Prayer times - using monospace for alignment
        # Format: emoji Prayer......: HH:MM
        prayer_lines = []
        prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]

        for prayer in prayers:
            if prayer in timings:
                emoji = MessageFormatter.PRAYER_EMOJIS.get(prayer, "🕌")
                name = MessageFormatter.PRAYER_NAMES.get(prayer, prayer)
                time = timings[prayer]

                # Create aligned formatting with monospace
                # Use dots for visual alignment (mimics JetBrains Mono spacing)
                padding = "." * (12 - len(name))
                prayer_lines.append(f"{emoji} <code>{name}{padding}: {time}</code>")

        times_block = "\n".join(prayer_lines)

        # Footer
        footer = f"\n\n<i>📖 Метод: Всемирная Мусульманская Лига</i>\n<i>   (Фаджр: 18°, Иша: 17°)</i>"

        return header + times_block + footer

    @staticmethod
    def format_weekly_times(
        calendar_data: List[Dict],
        city: Optional[str] = None
    ) -> str:
        """
        Format weekly prayer times (7 days) in compact format

        Args:
            calendar_data: List of daily prayer times from AlAdhan API
            city: City name (optional)

        Returns:
            Formatted message string with HTML markup
        """
        location_line = f"📍 <b>{city}</b>\n" if city else ""
        header = f"""🕌 <b>Время намаза на неделю</b>
{location_line}
"""

        # Format each day compactly
        lines = []
        for day_data in calendar_data[:7]:  # First 7 days
            date_obj = datetime.fromtimestamp(int(day_data["date"]["timestamp"]))
            date_str = date_obj.strftime("%d.%m")
            weekday_short = MessageFormatter._get_russian_weekday_short(date_obj)

            timings = day_data["timings"]
            fajr = timings["Fajr"]
            maghrib = timings["Maghrib"]

            # Compact format: Date Weekday Fajr-Maghrib
            lines.append(f"<code>{date_str} {weekday_short} │ {fajr} - {maghrib}</code>")

        times_block = "\n".join(lines)

        footer = "\n\n<i>Показаны Фаджр и Магриб</i>\n<i>Для полного расписания используйте /today</i>"

        return header + times_block + footer

    @staticmethod
    def format_welcome_message() -> str:
        """Welcome message in Russian"""
        return """🕌 <b>Ас-саляму алейкум!</b>

Добро пожаловать в бот времени намаза 🌙

Этот бот предоставляет точное время намаза на основе:
• <b>Метод:</b> Всемирная Мусульманская Лига
• <b>Фаджр:</b> 18° (угол)
• <b>Иша:</b> 17° (угол)

<b>Как использовать:</b>
1. Поделитесь своим местоположением 📍
2. Или выберите город из списка 🏙️

<i>Расчёты соответствуют islamicfinder.org</i>

<b>Команды:</b>
/start - Начать работу
/today - Время на сегодня
/week - Расписание на неделю
/cities - Выбрать город"""

    @staticmethod
    def format_error_message(error_type: str = "general") -> str:
        """Format error messages in Russian"""
        errors = {
            "general": "❌ Произошла ошибка. Пожалуйста, попробуйте снова.",
            "network": "❌ Ошибка сети. Проверьте подключение к интернету.",
            "location": "❌ Не удалось определить местоположение. Попробуйте снова.",
            "api": "❌ Ошибка получения данных. Попробуйте позже.",
        }
        return errors.get(error_type, errors["general"])

    @staticmethod
    def format_city_selection_prompt() -> str:
        """Prompt for city selection"""
        return """🏙️ <b>Выберите город:</b>

Выберите город из списка ниже или поделитесь своим местоположением для точного расчёта."""

    @staticmethod
    def _get_russian_weekday(date: datetime) -> str:
        """Get Russian weekday name"""
        weekdays = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье",
        }
        return weekdays[date.weekday()]

    @staticmethod
    def _get_russian_weekday_short(date: datetime) -> str:
        """Get Russian weekday short name"""
        weekdays = {
            0: "Пн",
            1: "Вт",
            2: "Ср",
            3: "Чт",
            4: "Пт",
            5: "Сб",
            6: "Вс",
        }
        return weekdays[date.weekday()]


# Global formatter instance
formatter = MessageFormatter()
