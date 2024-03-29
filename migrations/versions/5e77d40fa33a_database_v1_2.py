"""Database v1.2

Revision ID: 5e77d40fa33a
Revises: 510966343696
Create Date: 2023-05-18 22:19:57.525197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e77d40fa33a'
down_revision = '510966343696'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('mode_length_sec', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mode_id', sa.Integer(), nullable=False),
    sa.Column('played_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('game_length_sec', sa.Integer(), nullable=False),
    sa.Column('player_1_id', sa.Integer(), nullable=False),
    sa.Column('player_2_id', sa.Integer(), nullable=False),
    sa.Column('player_1_nickname', sa.String(length=50), nullable=False),
    sa.Column('player_2_nickname', sa.String(length=50), nullable=False),
    sa.Column('rate_change_player_1', sa.Integer(), nullable=False),
    sa.Column('rate_change_player_2', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mode_id'], ['mode.id'], ),
    sa.ForeignKeyConstraint(['player_1_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['player_2_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('match')
    op.drop_table('mode')
    # ### end Alembic commands ###
