"""empty message

Revision ID: d1c03030a811
Revises: c0b394533c82
Create Date: 2023-05-01 13:06:56.325365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1c03030a811'
down_revision = 'c0b394533c82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('puns_categories',
    sa.Column('pun_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['pun_id'], ['puns.id'], ),
    sa.PrimaryKeyConstraint('pun_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('puns_categories')
    # ### end Alembic commands ###
