"""empty message

Revision ID: b685d222a839
Revises: 31bc366c09f4
Create Date: 2019-10-08 14:54:24.371135

"""

# revision identifiers, used by Alembic.
revision = 'b685d222a839'
down_revision = '31bc366c09f4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('priority', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tickets', 'priorities', ['priority'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_column('tickets', 'priority')
    # ### end Alembic commands ###
