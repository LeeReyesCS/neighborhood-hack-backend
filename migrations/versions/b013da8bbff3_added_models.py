"""added models

Revision ID: b013da8bbff3
Revises: 
Create Date: 2023-05-19 20:34:10.856491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b013da8bbff3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('neighbor',
    sa.Column('neighbor_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('zipcode', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('looking_to_trade', sa.Boolean(), nullable=True),
    sa.Column('services', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('skills', sa.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('neighbor_id')
    )
    op.create_table('board',
    sa.Column('board_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('board_title', sa.String(), nullable=True),
    sa.Column('looking_for', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('neighbor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['neighbor_id'], ['neighbor.neighbor_id'], ),
    sa.PrimaryKeyConstraint('board_id')
    )
    op.create_table('comment',
    sa.Column('comment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment_text', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('neighbor_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.board_id'], ),
    sa.ForeignKeyConstraint(['neighbor_id'], ['neighbor.neighbor_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('board')
    op.drop_table('neighbor')
    # ### end Alembic commands ###
