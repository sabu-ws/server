"""empty message

Revision ID: 078ebf820ab2
Revises: d1adc1c50b43
Create Date: 2024-03-21 12:32:12.050981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '078ebf820ab2'
down_revision = 'd1adc1c50b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('codeep', schema=None) as batch_op:
        batch_op.drop_constraint('codeep_code_key', type_='unique')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('users_cookie_key', type_='unique')
        batch_op.drop_column('cookie')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cookie', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.create_unique_constraint('users_cookie_key', ['cookie'])

    with op.batch_alter_table('codeep', schema=None) as batch_op:
        batch_op.create_unique_constraint('codeep_code_key', ['code'])

    # ### end Alembic commands ###
