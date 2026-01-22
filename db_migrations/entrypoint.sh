#!/bin/bash
set -e

# URL репозитория
REPO_URL="https://github.com/VaycheslavZhukovsky/dataHarvesterHarvester.git"
PROJECT_DIR="/app/project_repo"

# Клонируем или обновляем репозиторий
if [ -d "$PROJECT_DIR" ]; then
    echo "Обновляем репозиторий..."
    cd "$PROJECT_DIR" && git pull
else
    echo "Клонируем репозиторий..."
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

# Переходим в папку с миграциями
cd "$PROJECT_DIR/db_migrations"

# 1️⃣ Устанавливаем зависимости из requirements.txt внутри репозитория
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Устанавливаем зависимости из $PROJECT_DIR/requirements.txt..."
    pip install --no-cache-dir -r "$PROJECT_DIR/requirements.txt"
else
    echo "requirements.txt не найден!"
    exit 1
fi

# 2️⃣ Настраиваем PYTHONPATH
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# 3️⃣ Запускаем миграции
python migrations/env.py
