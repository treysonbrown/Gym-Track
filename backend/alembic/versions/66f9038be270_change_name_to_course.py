"""Change name to Course

Revision ID: 66f9038be270
Revises: f9e68f3c034e
Create Date: 2025-08-22 09:02:12.016839

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '66f9038be270'
down_revision: str | Sequence[str] | None  = 'f9e68f3c034e'
branch_labels: str | Sequence[str] | None = None
depends_on:    str | Sequence[str] | None = None


def upgrade():
    op.rename_table('class', 'course')

def downgrade():
    op.rename_table('course', 'class')
