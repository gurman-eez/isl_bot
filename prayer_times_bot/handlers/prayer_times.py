"""
Prayer Times Handler
Handles location processing and prayer times display
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from datetime import datetime
import logging
import pytz

from config import POLISH_CITIES, POLAND_TIMEZONE
from services.aladhan_api import api, AlAdhanAPIError
from services.formatter import formatter
from keyboards.main_keyboards import (
    get_main_menu_keyboard,
    get_cities_keyboard,
)

logger = logging.getLogger(__name__)

# Create router for prayer times handlers
router = Router()


@router.message(F.location)
async def handle_location(message: Message):
    """
    Handle location sharing from user

    Args:
        message: Telegram message with location
    """
    latitude = message.location.latitude
    longitude = message.location.longitude

    logger.info(f"User {message.from_user.id} shared location: {latitude}, {longitude}")

    # Send "processing" message
    processing_msg = await message.answer("⏳ Получаю время намаза...")

    try:
        # Get prayer times from API
        timings = await api.get_timings_by_coordinates(latitude, longitude)

        # Format and send response
        response = formatter.format_daily_times(timings)

        await processing_msg.edit_text(
            response,
            parse_mode="HTML"
        )

        # Send menu keyboard
        await message.answer(
            "Что ещё вы хотите узнать?",
            reply_markup=get_main_menu_keyboard()
        )

    except AlAdhanAPIError as e:
        logger.error(f"API error for user {message.from_user.id}: {e}")
        error_msg = formatter.format_error_message("api")
        await processing_msg.edit_text(error_msg)

    except Exception as e:
        logger.error(f"Unexpected error for user {message.from_user.id}: {e}")
        error_msg = formatter.format_error_message("general")
        await processing_msg.edit_text(error_msg)


@router.callback_query(F.data.startswith("city:"))
async def handle_city_selection(callback: CallbackQuery):
    """
    Handle city selection from inline keyboard

    Args:
        callback: Telegram callback query
    """
    city_name = callback.data.split(":", 1)[1]

    logger.info(f"User {callback.from_user.id} selected city: {city_name}")

    if city_name not in POLISH_CITIES:
        await callback.answer("❌ Город не найден", show_alert=True)
        return

    # Get coordinates
    latitude, longitude = POLISH_CITIES[city_name]

    # Update message to show processing
    await callback.message.edit_text("⏳ Получаю время намаза...")

    try:
        # Get prayer times from API
        timings = await api.get_timings_by_coordinates(latitude, longitude)

        # Format and send response
        response = formatter.format_daily_times(timings, city=city_name)

        await callback.message.edit_text(
            response,
            parse_mode="HTML"
        )

        # Send menu keyboard in new message
        await callback.message.answer(
            "Что ещё вы хотите узнать?",
            reply_markup=get_main_menu_keyboard()
        )

        await callback.answer()

    except AlAdhanAPIError as e:
        logger.error(f"API error for user {callback.from_user.id}: {e}")
        error_msg = formatter.format_error_message("api")
        await callback.message.edit_text(error_msg)
        await callback.answer()

    except Exception as e:
        logger.error(f"Unexpected error for user {callback.from_user.id}: {e}")
        error_msg = formatter.format_error_message("general")
        await callback.message.edit_text(error_msg)
        await callback.answer()


@router.message(Command("today"))
@router.message(F.text == "📅 На сегодня")
async def cmd_today(message: Message):
    """
    Handle /today command or button

    Args:
        message: Telegram message object
    """
    # Show city selection
    city_prompt = "📅 <b>Время намаза на сегодня</b>\n\nВыберите город или поделитесь местоположением:"

    await message.answer(
        city_prompt,
        reply_markup=get_cities_keyboard(),
        parse_mode="HTML"
    )


@router.message(Command("week"))
@router.message(F.text == "📆 На неделю")
async def cmd_week(message: Message):
    """
    Handle /week command or button - show weekly prayer times

    Args:
        message: Telegram message object
    """
    # For now, show city selection (in future, could remember last location)
    city_prompt = "📆 <b>Расписание на неделю</b>\n\nВыберите город:"

    await message.answer(
        city_prompt,
        reply_markup=get_cities_keyboard(),
        parse_mode="HTML"
    )


@router.message(Command("cities"))
async def cmd_cities(message: Message):
    """
    Handle /cities command - show city selection

    Args:
        message: Telegram message object
    """
    city_prompt = formatter.format_city_selection_prompt()

    await message.answer(
        city_prompt,
        reply_markup=get_cities_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "time:today")
async def show_today_times(callback: CallbackQuery):
    """
    Handle today's times callback

    Args:
        callback: Telegram callback query
    """
    await callback.message.edit_text(
        "📅 Выберите город для просмотра времени на сегодня:",
        reply_markup=get_cities_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "time:week")
async def show_week_times(callback: CallbackQuery):
    """
    Handle weekly times callback

    Args:
        callback: Telegram callback query
    """
    await callback.message.edit_text(
        "📆 Выберите город для просмотра расписания на неделю:",
        reply_markup=get_cities_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "time:month")
async def show_month_times(callback: CallbackQuery):
    """
    Handle monthly times callback (future feature)

    Args:
        callback: Telegram callback query
    """
    await callback.answer(
        "📖 Функция 'На месяц' будет добавлена в следующей версии",
        show_alert=True
    )
