"""seed categories"""

import sys
from pathlib import Path
from alembic import op
import sqlalchemy as sa


# --- ДОБАВЛЯЕМ ПУТИ ---
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "parser"))

# Теперь можно импортировать metadata и SUBCATEGORIES
from project.infrastructure.persistence.db import metadata
from project.config import SUBCATEGORIES

target_metadata = metadata


def upgrade():
    conn = op.get_bind()

    # Вставляем категории, избегая дублей
    for slug in SUBCATEGORIES:
        conn.execute(
            sa.text("""
                INSERT INTO categories (slug)
                VALUES (:slug)
                ON CONFLICT (slug) DO NOTHING
            """),
            {"slug": slug},
        )


def downgrade():
    conn = op.get_bind()

    # Удаляем только те категории, которые были добавлены этим seed
    conn.execute(
        sa.text("""
            DELETE FROM categories
            WHERE slug = ANY(:slugs)
        """),
        {"slugs": SUBCATEGORIES},
    )
