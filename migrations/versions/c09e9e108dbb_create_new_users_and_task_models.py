"""create new users and task models

Revision ID: c09e9e108dbb
Revises: fb97b11c619e
Create Date: 2025-01-21 15:31:55.752492

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c09e9e108dbb"
down_revision: Union[str, None] = "fb97b11c619e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "tasks_new",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("description", sa.String, nullable=False),
    )

    op.execute(
        """
    INSERT INTO tasks_new (id, description)
    SELECT id, description
    FROM tasks
    """
    )

    op.drop_table("tasks")

    op.rename_table("tasks_new", "tasks")


def downgrade():
    op.create_table(
        "tasks_old",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("description", sa.String, nullable=True),  # Sem NOT NULL
    )

    op.execute(
        """
    INSERT INTO tasks_old (id, description)
    SELECT id, description
    FROM tasks
    """
    )

    op.drop_table("tasks")

    op.rename_table("tasks_old", "tasks")
