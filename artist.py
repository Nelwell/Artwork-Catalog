from artwork_store import ArtworkStore
from main import add_artwork


class Artist:

    def __init__(self, name, email, artist_id=None):
        self.name = name
        self.email = email
        self.artist_id = artist_id

        self.artworkstore = ArtworkStore()

    def insert_artist(self):
        if self.artist_id:
            add_artwork()
        else:
            self.artworkstore._add_artist(self)
