"""empty message

Revision ID: d952e3332d45
Revises: 38d81a0f42db
Create Date: 2022-04-15 20:53:23.594085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd952e3332d45'
down_revision = '38d81a0f42db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Todo', sa.Column('task_done', sa.Boolean(), nullable=True))
    op.drop_column('Todo', 'completed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Todo', sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Todo', 'task_done')
    # ### end Alembic commands ###