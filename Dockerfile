FROM python:3.13.2-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Copy requirements first for layer caching optimization
COPY prayer_times_bot/requirements.txt /app/prayer_times_bot/requirements.txt
RUN pip install --no-cache-dir -r /app/prayer_times_bot/requirements.txt

# Copy application code
COPY prayer_times_bot/ /app/prayer_times_bot/

# Health check for Railway monitoring
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f "python.*bot.py" || exit 1

CMD ["python", "-u", "prayer_times_bot/bot.py"]
