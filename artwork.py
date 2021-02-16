from artwork_store import ArtworkStore
from main import add_artist


class Artwork:

    def __init__(self, artwork, price, artist_id, for_sale=True):
        self.artwork = artwork
        self.price = price
        self.artist_id = artist_id
        self.for_sale = for_sale

        self.artworkstore = ArtworkStore()

    def insert_artwork(self):
        if self.artist_id:
            self.artworkstore._add_artwork(self)
        else:
            add_artist()
