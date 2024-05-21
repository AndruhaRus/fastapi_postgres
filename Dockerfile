# Dockerfile

# Используем официальный образ Python
FROM python:3.9

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы проекта
COPY . .

# Указываем команду для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
