"""empty message

Revision ID: 371afe8b768e
Revises: 
Create Date: 2024-04-27 20:01:33.408256

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '371afe8b768e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usblog')
    with op.batch_alter_table('USBlog', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('scanLogPath', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scanLogPath', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('USBlog', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    op.create_table('usblog',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('virus', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('device_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='usblog_device_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='usblog_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='usblog_pkey'),
    sa.UniqueConstraint('id', name='usblog_id_key')
    )
    # ### end Alembic commands ###
