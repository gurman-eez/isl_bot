"""
Start command handler
Handles /start command and welcome message
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import logging

from keyboards.main_keyboards import (
    get_main_menu_keyboard,
    get_cities_keyboard,
)
from services.formatter import formatter

logger = logging.getLogger(__name__)

# Create router for start-related handlers
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handle /start command

    Args:
        message: Telegram message object
    """
    logger.info(f"User {message.from_user.id} started the bot")

    # Send welcome message
    welcome_text = formatter.format_welcome_message()

    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Handle /help command

    Args:
        message: Telegram message object
    """
    help_text = """🕌 <b>Помощь</b>

<b>Доступные команды:</b>

/start - Начать работу с ботом
/today - Время намаза на сегодня
/week - Расписание на неделю
/cities - Выбрать город из списка
/help - Показать эту справку

<b>Как использовать бот:</b>

1️⃣ <b>Поделиться местоположением:</b>
   Нажмите кнопку "📍 Поделиться местоположением" для получения точного времени намаза для вашего местоположения.

2️⃣ <b>Выбрать город:</b>
   Нажмите "🏙️ Выбрать город" для выбора из списка польских городов.

3️⃣ <b>Просмотр расписания:</b>
   Используйте кнопки "📅 На сегодня" и "📆 На неделю" для просмотра расписания.

<b>О расчётах:</b>
Бот использует метод <b>Всемирной Мусульманской Лиги</b>:
• Угол Фаджр: 18°
• Угол Иша: 17°

Расчёты соответствуют islamicfinder.org

<i>⚠️ Примечание: Время рассчитано автоматически. Для точности рекомендуем проверить в местной мечети.</i>"""

    await message.answer(
        help_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🏙️ Выбрать город")
async def select_city_button(message: Message):
    """
    Handle city selection button

    Args:
        message: Telegram message object
    """
    city_prompt = formatter.format_city_selection_prompt()

    await message.answer(
        city_prompt,
        reply_markup=get_cities_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """
    Handle back to menu callback

    Args:
        callback: Telegram callback query
    """
    welcome_text = formatter.format_welcome_message()

    await callback.message.edit_text(
        welcome_text,
        parse_mode="HTML"
    )

    # Send new message with main menu keyboard
    await callback.message.answer(
        "Выберите действие:",
        reply_markup=get_main_menu_keyboard()
    )

    await callback.answer()
