from artwork_store import ArtworkStore


class Artist:

    def __init__(self, name, email, artist_id=None):
        self.name = name
        self.email = email
        self.artist_id = artist_id

        self.artworkstore = ArtworkStore()

    def insert_artist(self):
        """ Checks if ID already exists for book object being passed. If yes, then calls update_book method.
            update_book method takes newly entered data to update existing book object.
            If book ID is not already present when book object is passed in, function will call add_book method.
            add_book method takes new book object attributes to build a new record in DB with auto-generated ID. """
        # if self.artist_id:
        self.artworkstore._commit_artist(self)
        # else:
        #     self.bookstore._add_book(self)
