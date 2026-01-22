# 1. Базовый образ
FROM python:3.12-slim

# 2. Устанавливаем git и bash
RUN apt-get update && apt-get install -y git bash && rm -rf /var/lib/apt/lists/*

# 3. Создаем рабочую директорию для проекта
WORKDIR /app

# 4. Копируем скрипт запуска
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# 5. Запуск по умолчанию
CMD ["./entrypoint.sh"]
