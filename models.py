from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'Artists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    albums = relationship('Album', back_populates='artist')


class Album(Base):
    __tablename__ = 'Albums'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey('Artists.id'))
    artist = relationship('Artist', back_populates='albums')
    songs = relationship('Song', back_populates='album')


class Song(Base):
    __tablename__ = 'Songs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    duration = Column(Integer)
    album_id = Column(Integer, ForeignKey('Albums.id'))
    album = relationship('Album', back_populates='songs')
