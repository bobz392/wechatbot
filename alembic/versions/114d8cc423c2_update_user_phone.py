"""update user phone

Revision ID: 114d8cc423c2
Revises: e402cb191952
Create Date: 2018-08-03 15:56:28.940196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '114d8cc423c2'
down_revision = 'e402cb191952'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone_number', sa.String(length=11), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone_number')
    # ### end Alembic commands ###