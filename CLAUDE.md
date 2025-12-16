# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a **Prayer Times Telegram Bot** (`prayer_times_bot/`) - a mobile-first Russian-language bot that displays Islamic prayer times based on user location or city selection in Poland.

**Key Features:**
- Location-based prayer times using AlAdhan API
- Muslim World League calculation method (Fajr: 18°, Isha: 17°)
- Russian language interface with monospace-formatted times
- Support for 10 major Polish cities
- Built with aiogram 3.x (async Telegram bot framework)

## Development Environment

- **Python Version**: 3.13.2
- **Package Manager**: pip 25.1.1
- **Virtual Environment**: `.venv/` (at project root)
- **Main Project**: `prayer_times_bot/` directory

## Common Commands

### Bot Development

```bash
# Navigate to bot directory
cd prayer_times_bot

# Install bot dependencies
pip install -r requirements.txt

# Set up environment variables (required!)
# 1. Copy .env.example to .env
# 2. Add your Telegram bot token from @BotFather
BOT_TOKEN=your_bot_token_here

# Run the bot
python bot.py

# View logs
tail -f bot.log
```

### Environment Setup
```bash
# Activate virtual environment (from project root)
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r prayer_times_bot/requirements.txt
```

### Testing Prayer Times

To verify calculations match islamicfinder.org:
1. Test with specific Polish city coordinates
2. Compare results with islamicfinder.org (Muslim World League method)
3. Times should match within ±1 minute

```bash
# Example: Manual API test
curl "https://api.aladhan.com/v1/timings/16-12-2025?latitude=52.2297&longitude=21.0122&method=3"
```

## Architecture

### Project Structure

```
prayer_times_bot/
├── bot.py                   # Entry point - initializes bot and routers
├── config.py                # Configuration (API URLs, cities, constants)
│
├── handlers/                # Message and command handlers
│   ├── start.py            # /start, /help, menu navigation
│   └── prayer_times.py     # Location handling, prayer times display
│
├── services/                # Business logic layer
│   ├── aladhan_api.py      # AlAdhan API client (async HTTP requests)
│   └── formatter.py        # Russian message formatting with monospace
│
└── keyboards/               # Telegram UI components
    └── main_keyboards.py   # Location sharing, city selection keyboards
```

### Key Architectural Patterns

1. **Handler-Service Separation**
   - Handlers (`handlers/`) receive Telegram updates and respond to users
   - Services (`services/`) contain business logic (API calls, formatting)
   - Keeps handlers thin and testable

2. **Async Throughout**
   - Uses `async/await` for all I/O operations
   - aiogram 3.x is fully asynchronous
   - aiohttp for non-blocking API calls

3. **Router-Based Organization**
   - Each handler module exports a Router
   - Routers are registered in bot.py
   - Clean separation of concerns by feature

4. **Centralized Configuration**
   - `config.py` contains all constants and settings
   - Uses python-dotenv for environment variables
   - Polish cities coordinates stored as dictionary

### Data Flow

1. **Location Flow**: User shares location → `prayer_times.py:handle_location()` → `aladhan_api.py:get_timings_by_coordinates()` → `formatter.py:format_daily_times()` → User receives formatted prayer times

2. **City Selection Flow**: User clicks city button → `prayer_times.py:handle_city_selection()` → Gets coordinates from `config.POLISH_CITIES` → Same as location flow

3. **Command Flow**: User sends /start → `start.py:cmd_start()` → `formatter.format_welcome_message()` → Display with main menu keyboard

### External Dependencies

- **AlAdhan API**: Free prayer times API (no authentication required)
  - Endpoint: https://api.aladhan.com/v1
  - Method 3 = Muslim World League (Fajr: 18°, Isha: 17°)
  - Returns JSON with prayer times in HH:MM format

- **aiogram 3.x**: Telegram Bot API framework
  - Handles long polling, message routing, keyboard rendering
  - Built-in HTML/Markdown formatting support

### Message Formatting

- Uses HTML formatting (`parse_mode="HTML"`)
- Monospace blocks (`<code>`) for prayer time alignment
- Emojis for visual guidance (🌅 Fajr, 🌙 Isha, etc.)
- JetBrains Mono style achieved with dots for visual spacing in code blocks

### Error Handling

- Custom `AlAdhanAPIError` exception for API failures
- Graceful degradation: Show error messages in Russian
- Logging to both console and `bot.log` file

## Development Guidelines

### Adding New Cities

Edit `config.py`:
```python
POLISH_CITIES = {
    "City Name": (latitude, longitude),
    # Add new cities here
}
```

### Modifying Prayer Time Display

Edit `services/formatter.py`:
- `format_daily_times()` for single-day display
- `format_weekly_times()` for week view
- Maintain monospace alignment in `<code>` blocks

### Adding New Commands

1. Create handler in appropriate file (`handlers/start.py` or `handlers/prayer_times.py`)
2. Use `@router.message(Command("commandname"))` decorator
3. No need to modify bot.py (router auto-registers)

### Testing with BotFather

1. Create test bot with @BotFather
2. Get token, add to `.env`
3. Run `python bot.py`
4. Test all commands and location sharing
5. Verify times against islamicfinder.org

## Important Notes

- **Never commit `.env` file** (contains bot token)
- **AlAdhan API** has no rate limits documented, but be respectful
- **Timezone**: All times use Europe/Warsaw (UTC+1/+2)
- **Calculation Method**: Must remain MWL (method 3) to match islamicfinder.org
- **Language**: All user-facing text must be in Russian