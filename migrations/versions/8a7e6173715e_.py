"""empty message

Revision ID: 8a7e6173715e
Revises: a4b4914dc0ce
Create Date: 2024-05-06 14:21:39.857958

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8a7e6173715e'
down_revision = 'a4b4914dc0ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('USBlog')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('USBlog',
    sa.Column('virus', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date_ht', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('scan_id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='USBlog_user_id_fkey'),
    sa.PrimaryKeyConstraint('date_ht', name='USBlog_pkey')
    )
    # ### end Alembic commands ###
