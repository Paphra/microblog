"""user token

Revision ID: 063f0bf6c6d1
Revises: 9c64c6ed65c8
Create Date: 2019-03-31 23:03:42.883906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '063f0bf6c6d1'
down_revision = '9c64c6ed65c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    # ### end Alembic commands ###