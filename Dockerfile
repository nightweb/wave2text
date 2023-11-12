# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование содержимого локальной папки в контейнер
COPY . .

# Открытие порта 5000 для доступа к серверу
EXPOSE 5000

# Запуск приложения
CMD ["python", "./app.py"]
