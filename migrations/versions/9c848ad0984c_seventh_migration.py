"""Seventh migration.

Revision ID: 9c848ad0984c
Revises: a52d9d8bd2fd
Create Date: 2020-07-08 22:17:08.037330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c848ad0984c'
down_revision = 'a52d9d8bd2fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dorm',
    sa.Column('dorm_id', sa.Integer(), nullable=False),
    sa.Column('dorm_gender', sa.String(length=6), nullable=True),
    sa.Column('dormage_group', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('dorm_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dorm')
    # ### end Alembic commands ###