"""empty message

Revision ID: 86b1440622e2
Revises: 997359b059a1
Create Date: 2024-06-01 21:12:10.660239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86b1440622e2'
down_revision = '997359b059a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist_genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=100), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue_genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=100), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_genre')
    op.drop_table('artist_genre')
    # ### end Alembic commands ###
