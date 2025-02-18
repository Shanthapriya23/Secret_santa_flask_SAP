"""updates done

Revision ID: 186599b55710
Revises: 30b468889196
Create Date: 2025-02-18 11:45:51.976127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186599b55710'
down_revision = '30b468889196'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('santa_id', sa.Integer(), nullable=False),
    sa.Column('child_id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(length=500), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['santa_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('gift_lock', schema=None) as batch_op:
        batch_op.add_column(sa.Column('revealed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gift_lock', schema=None) as batch_op:
        batch_op.drop_column('revealed')

    op.drop_table('task')
    # ### end Alembic commands ###
