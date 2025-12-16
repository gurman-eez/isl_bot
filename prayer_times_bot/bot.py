"""
Prayer Times Telegram Bot
Main entry point for the bot application

A mobile-first bot for displaying Islamic prayer times in Russian
Based on Muslim World League calculation method (Fajr: 18°, Isha: 17°)
"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import start, prayer_times


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """
    Main function to start the bot with production-ready error handling
    """
    logger.info("Starting Prayer Times Bot...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Running in production mode with long-polling")

    # Initialize bot with default parse mode
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    # Initialize dispatcher
    dp = Dispatcher()

    # Register routers
    dp.include_router(start.router)
    dp.include_router(prayer_times.router)

    logger.info("Routers registered successfully")

    # Start bot with proper error handling for production
    try:
        logger.info("Bot is starting polling...")
        logger.info("Listening for updates. Press Ctrl+C to stop.")

        # Drop pending updates on startup to avoid processing old messages
        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
    except asyncio.CancelledError:
        logger.info("Bot polling cancelled, shutting down gracefully...")
    except Exception as e:
        logger.error(f"Critical error during bot execution: {e}", exc_info=True)
        raise
    finally:
        logger.info("Closing bot session...")
        await bot.session.close()
        logger.info("Bot stopped successfully")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
