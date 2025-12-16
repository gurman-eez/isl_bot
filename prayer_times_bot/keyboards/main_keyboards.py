"""
Telegram Keyboard Layouts
Mobile-first design with Russian labels
"""
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from typing import List

from config import POLISH_CITIES


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Main menu keyboard with location sharing and city selection

    Returns:
        ReplyKeyboardMarkup for mobile-first interface
    """
    keyboard = [
        [
            KeyboardButton(
                text="📍 Поделиться местоположением",
                request_location=True
            )
        ],
        [
            KeyboardButton(text="🏙️ Выбрать город")
        ],
        [
            KeyboardButton(text="📅 На сегодня"),
            KeyboardButton(text="📆 На неделю")
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие..."
    )


def get_location_request_keyboard() -> ReplyKeyboardMarkup:
    """
    Simple keyboard requesting location

    Returns:
        ReplyKeyboardMarkup with location button
    """
    keyboard = [
        [
            KeyboardButton(
                text="📍 Отправить местоположение",
                request_location=True
            )
        ],
        [
            KeyboardButton(text="🏙️ Выбрать город вместо этого")
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Поделитесь местоположением..."
    )


def get_cities_keyboard() -> InlineKeyboardMarkup:
    """
    Inline keyboard with Polish cities

    Returns:
        InlineKeyboardMarkup with city buttons
    """
    # Sort cities alphabetically
    sorted_cities = sorted(POLISH_CITIES.keys())

    # Create buttons in rows of 2
    buttons = []
    row = []
    for i, city in enumerate(sorted_cities):
        row.append(
            InlineKeyboardButton(
                text=f"📍 {city}",
                callback_data=f"city:{city}"
            )
        )

        # Create row of 2 buttons
        if len(row) == 2 or i == len(sorted_cities) - 1:
            buttons.append(row)
            row = []

    # Add back button
    buttons.append([
        InlineKeyboardButton(
            text="◀️ Назад в меню",
            callback_data="back_to_menu"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Simple back to menu button

    Returns:
        InlineKeyboardMarkup with back button
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="◀️ Вернуться в меню",
                callback_data="back_to_menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_time_options_keyboard() -> InlineKeyboardMarkup:
    """
    Keyboard for selecting time range (today/week/month)

    Returns:
        InlineKeyboardMarkup with time options
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="📅 На сегодня",
                callback_data="time:today"
            ),
            InlineKeyboardButton(
                text="📆 На неделю",
                callback_data="time:week"
            )
        ],
        [
            InlineKeyboardButton(
                text="📖 На месяц",
                callback_data="time:month"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Назад",
                callback_data="back_to_menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
