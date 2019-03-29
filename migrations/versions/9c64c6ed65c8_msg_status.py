"""msg status

Revision ID: 9c64c6ed65c8
Revises: b09c9eff3522
Create Date: 2019-03-28 23:38:52.261636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c64c6ed65c8'
down_revision = 'b09c9eff3522'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'status')
    # ### end Alembic commands ###
