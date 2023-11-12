# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Установка рабочей директории в контейнере
WORKDIR /app

# Установка ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка Gunicorn
RUN pip install gunicorn

# Копирование содержимого локальной папки в контейнер
COPY . .

# Открытие порта 5000 для доступа к серверу
EXPOSE 5000

# Запуск приложения с помощью Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
