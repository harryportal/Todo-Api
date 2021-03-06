"""empty message

Revision ID: 38d81a0f42db
Revises: be012d5699d0
Create Date: 2022-04-15 20:28:54.058249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38d81a0f42db'
down_revision = 'be012d5699d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Todo', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Todo', 'completed')
    # ### end Alembic commands ###
