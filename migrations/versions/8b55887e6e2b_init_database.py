"""init-database

Revision ID: 8b55887e6e2b
Revises: 
Create Date: 2021-06-08 00:25:17.446767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b55887e6e2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ArtistSound',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('song', sa.String(length=100), nullable=False),
    sa.Column('sound', sa.String(length=100), nullable=False),
    sa.Column('lyric', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['OrgArtist.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('PlayListLike',
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['playlist_id'], ['PlayList.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('playlist_id', 'user_id')
    )
    op.create_table('PlayListSong',
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['playlist_id'], ['PlayList.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['song_id'], ['Song.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('playlist_id', 'song_id')
    )
    op.create_table('RemakeArtistSong',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('org_song_id', sa.Integer(), nullable=True),
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['org_song_id'], ['OrgSong.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['song_id'], ['Song.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('RemakeUserSong',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('org_song_id', sa.Integer(), nullable=True),
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['org_song_id'], ['OrgSong.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['song_id'], ['Song.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('RemakeUserSong')
    op.drop_table('RemakeArtistSong')
    op.drop_table('PlayListSong')
    op.drop_table('PlayListLike')
    op.drop_table('ArtistSound')
    # ### end Alembic commands ###
