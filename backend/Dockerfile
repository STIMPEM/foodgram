FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копирование кода проекта
COPY foodgram_backend/ .

# Копирование скрипта запуска
COPY start.sh .

# Создание директории для статических файлов
RUN mkdir -p /app/static/backend/

# Создание пользователя для безопасности и настройка прав
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app \
    && chmod +x /app/start.sh

# Устанавливаем sudo для appuser
RUN apt-get update && apt-get install -y sudo \
    && echo "appuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && rm -rf /var/lib/apt/lists/*

USER appuser

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["./start.sh"] 