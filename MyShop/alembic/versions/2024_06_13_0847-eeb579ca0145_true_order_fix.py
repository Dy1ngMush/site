"""true order fix

Revision ID: eeb579ca0145
Revises: 2aa3a1c6b384
Create Date: 2024-06-13 08:47:16.559344

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eeb579ca0145"
down_revision: Union[str, None] = "2aa3a1c6b384"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "true_orders", "promocode", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "true_orders", "promocode", existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###
