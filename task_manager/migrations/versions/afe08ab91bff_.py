"""empty message

Revision ID: afe08ab91bff
Revises: b7440b08a2e9
Create Date: 2024-09-28 02:20:39.882699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afe08ab91bff'
down_revision: Union[str, None] = 'b7440b08a2e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_faces_image_id'), 'faces', ['image_id'], unique=False)
    op.create_index(op.f('ix_images_task_id'), 'images', ['task_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_images_task_id'), table_name='images')
    op.drop_index(op.f('ix_faces_image_id'), table_name='faces')
    # ### end Alembic commands ###
