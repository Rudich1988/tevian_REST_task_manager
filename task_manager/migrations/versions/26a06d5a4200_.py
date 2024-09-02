"""empty message

Revision ID: 26a06d5a4200
Revises: 6b05f071d666
Create Date: 2024-09-02 23:33:42.348162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26a06d5a4200'
down_revision: Union[str, None] = '6b05f071d666'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('unique_filename', sa.String(length=500), nullable=False))
    op.add_column('images', sa.Column('filepath', sa.String(length=500), nullable=False))
    op.create_unique_constraint(None, 'images', ['unique_filename'])
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column(
        'faces', 'bounding_box',
        existing_type=sa.JSON(),
        type_=sa.String(length=500),
        nullable=False
    )
