"""Ninth migration.

Revision ID: a35400fe2150
Revises: 257583155d74
Create Date: 2020-07-09 09:27:04.824113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a35400fe2150'
down_revision = '257583155d74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('c_id', sa.Integer(), nullable=False),
    sa.Column('comments_made', sa.String(length=400), nullable=True),
    sa.Column('fname', sa.String(length=25), nullable=True),
    sa.Column('lname', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('c_id')
    )
    op.add_column('child', sa.Column('comments_made', sa.String(length=400), nullable=True))
    op.add_column('dorm', sa.Column('max_capacity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dorm', 'max_capacity')
    op.drop_column('child', 'comments_made')
    op.drop_table('comment')
    # ### end Alembic commands ###
