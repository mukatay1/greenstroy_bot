"""Описание изменений

Revision ID: 4dabd8bea9ee
Revises: af13f948f9b6
Create Date: 2024-08-25 12:09:48.776305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dabd8bea9ee'
down_revision: Union[str, None] = 'af13f948f9b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
