"""Third migration.

Revision ID: 64b65fc12719
Revises: 2544931f2e51
Create Date: 2020-07-08 19:37:57.213110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64b65fc12719'
down_revision = '2544931f2e51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parent', sa.Column('skills', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('parent', 'skills')
    # ### end Alembic commands ###