"""seed categories

Revision ID: 3656621f69e8
Revises: 27c9def19fd2
Create Date: 2026-01-07 12:28:52.665916
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "3656621f69e8"
down_revision: Union[str, Sequence[str], None] = "27c9def19fd2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from project.config import SUBCATEGORIES


def upgrade() -> None:
    conn = op.get_bind()

    for slug in SUBCATEGORIES:
        conn.execute(
            sa.text(
                """
                INSERT INTO categories (slug)
                VALUES (:slug)
                ON CONFLICT (slug) DO NOTHING
                """
            ),
            {"slug": slug},
        )


def downgrade() -> None:
    conn = op.get_bind()

    conn.execute(
        sa.text(
            """
            DELETE FROM categories
            WHERE slug = ANY(:slugs)
            """
        ),
        {"slugs": SUBCATEGORIES},
    )
