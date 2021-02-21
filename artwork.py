import sqlite3
from artwork_store import ArtworkStore
from database_config import db_path


class Artwork:

    def __init__(self, artwork, price, artist_id, for_sale=True):
        self.artwork = artwork
        self.price = price
        self.artist_id = artist_id
        self.for_sale = for_sale

        self.artworkstore = ArtworkStore()

    def insert_artwork(self):
        # if self.artist_id:
        self.artworkstore._add_artwork(self)

    def update_artwork(self):
        self.artworkstore._update_availability(self)

    def __str__(self):
        availability = 'is for sale' if self.for_sale else 'is not for sale'
        return f'Artist ID {self.artist_id}, Artwork: {self.artwork}, Price: {self.price}. {self.artwork} {availability}.'

    def __repr__(self):
        return f'Artist ID {self.artist_id} Artwork: {self.artwork} Price: {self.price} For Sale: {self.for_sale}'

    def __eq__(self, other):
        """ Overrides the Python == operator so one book can be tested for equality to another book based on attribute values """
        if isinstance(self, other.__class__):
            return self.artist_id == other.artist_id and self.artwork == other.artwork and self.price == other.price and self.for_sale == other.for_sale
        return False

    def __ne__(self, other):
        """ Overrides the != operator """
        if not isinstance(self, other.__class__):
            return True

        return self.artist_id != other.artist_id or self.artwork != other.artwork or self.price != other.price or self.for_sale != other.for_sale

    def __hash__(self):
        """ And Python makes us implement __hash__ if __eq__ is overriden """
        return hash((self.artist_id, self.artwork, self.price, self.for_sale))


    def get_artwork_by_id(self, artist_id):
        """ Searches list for Artwork with associated ID of given artist name,
        :param artist_id the ID to search for
        :returns the artwork, if found, or None if artwork not found.
        """

        query_artwork_id = 'SELECT artist_id, * FROM artworks WHERE artist_id = ?'

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This row_factory allows access to data by row name
        rows = conn.execute(query_artwork_id, (artist_id,))
        artwork_data = rows.fetchone()  # Get first result

        if artwork_data:
            artwork = Artwork(artwork_data['artwork'], artwork_data['price'], artwork_data['artist_id'], artwork_data['for_sale'])
        else:
            return None  # If artwork ID not found in db
        conn.close()

        return artwork

    def get_all_artist_artwork(self, artist_id):
        """ :returns entire artwork list associated with an artist """

        query_get_all_artworks = 'SELECT rowid, * FROM artworks WHERE artist_id = ?'

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query_get_all_artworks, (artist_id,))
        artworks = []

        for r in rows:
            artwork = Artwork(r['artwork'], r['price'], r['artist_id'], r['for_sale'])
            artworks.append(artwork)
        conn.close()

        return artworks

    def get_all_artist_available_artwork(self, artist_id):
        """ :returns entire available artwork list associated with an artist """

        query_get_all_artworks = 'SELECT rowid, * FROM artworks WHERE artist_id = ? AND for_sale = TRUE'

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query_get_all_artworks, (artist_id,))
        artworks = []

        for r in rows:
            artwork = Artwork(r['artwork'], r['price'], r['artist_id'], r['for_sale'])
            artworks.append(artwork)
        conn.close()

        return artworks
