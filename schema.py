import graphene
import sqlite3


# Define your GraphQL types
class ArtistType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class AlbumType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    artist = graphene.Field(ArtistType)


class TrackType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    album = graphene.Field(AlbumType)


# Define your queries
class Query(graphene.ObjectType):
    artists = graphene.List(ArtistType)
    albums = graphene.List(AlbumType)
    tracks = graphene.List(TrackType)

    def resolve_artists(self, info):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM artists')
        artists = cursor.fetchall()
        conn.close()
        return [ArtistType(id=row[0], name=row[1]) for row in artists]

    def resolve_albums(self, info):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, artist_id FROM albums')
        albums = cursor.fetchall()
        conn.close()
        return [AlbumType(id=row[0], title=row[1], artist=self.get_artist(row[2])) for row in albums]

    def resolve_tracks(self, info):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, album_id FROM tracks')
        tracks = cursor.fetchall()
        conn.close()
        return [TrackType(id=row[0], title=row[1], album=self.get_album(row[2])) for row in tracks]

    def get_artist(self, artist_id):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM artists WHERE id = ?', (artist_id,))
        artist = cursor.fetchone()
        conn.close()
        return ArtistType(id=artist[0], name=artist[1]) if artist else None

    def get_album(self, album_id):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, artist_id FROM albums WHERE id = ?', (album_id,))
        album = cursor.fetchone()
        conn.close()
        artist = self.get_artist(album[2]) if album else None
        return AlbumType(id=album[0], title=album[1], artist=artist) if album else None


# Define your mutations
class CreateArtist(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    artist_id = graphene.Int()

    def mutate(self, info, name):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO artists (name) VALUES (?)', (name,))
        conn.commit()
        artist_id = cursor.lastrowid
        print(f'Inserted artist with ID: {artist_id}')
        conn.close()
        return CreateArtist(artist_id=artist_id)


class CreateAlbum(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        artist_id = graphene.Int(required=True)

    album_id = graphene.Int()

    def mutate(self, info, title, artist_id):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO albums (title, artist_id) VALUES (?, ?)', (title, artist_id))
        conn.commit()
        album_id = cursor.lastrowid
        conn.close()
        return CreateAlbum(album_id=album_id)


class CreateTrack(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        album_id = graphene.Int(required=True)

    track_id = graphene.Int()

    def mutate(self, info, title, album_id):
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tracks (title, album_id) VALUES (?, ?)', (title, album_id))
        conn.commit()
        track_id = cursor.lastrowid
        conn.close()
        return CreateTrack(track_id=track_id)


class Mutation(graphene.ObjectType):
    create_artist = CreateArtist.Field()
    create_album = CreateAlbum.Field()
    create_track = CreateTrack.Field()


# Create the schema with Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
