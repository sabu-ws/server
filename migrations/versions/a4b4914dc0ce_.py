"""empty message

Revision ID: a4b4914dc0ce
Revises: 149a8a81f9ab
Create Date: 2024-05-06 14:12:26.924036

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a4b4914dc0ce'
down_revision = '149a8a81f9ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('USBlog', schema=None) as batch_op:
        pass
        #batch_op.add_column(sa.Column('date_ht', sa.DateTime(timezone=True), nullable=False))
        #batch_op.drop_constraint('USBlog_id_key', type_='unique')
        #batch_op.drop_column('id')
        #batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('USBlog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"USBlog_id_seq"\'::regclass)'), autoincrement=True, nullable=False))
        batch_op.create_unique_constraint('USBlog_id_key', ['id'])
        batch_op.drop_column('date_ht')

    # ### end Alembic commands ###
