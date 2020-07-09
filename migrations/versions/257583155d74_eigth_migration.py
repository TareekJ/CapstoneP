"""Eigth migration.

Revision ID: 257583155d74
Revises: 9c848ad0984c
Create Date: 2020-07-08 22:45:59.991007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '257583155d74'
down_revision = '9c848ad0984c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dorm', sa.Column('capacity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dorm', 'capacity')
    # ### end Alembic commands ###