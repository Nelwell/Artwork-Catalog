import sqlite3
from database_config import db_path
from errors import ArtworkError


class ArtworkStore:
    """ Singleton class to hold and manage a list of Books. All Bookstore objects created are the same object.
    Provides operations to add, update, delete, and query the store. """

    # instance = None
    #
    # class __ArtworkStore:

    def __init__(self):
        create_artist_table = 'CREATE TABLE IF NOT EXISTS artists (name TEXT COLLATE NOCASE, email TEXT, artist_id INTEGER PRIMARY KEY, UNIQUE(email COLLATE NOCASE))'

        create_artwork_table = 'CREATE TABLE IF NOT EXISTS artworks (artwork TEXT, price REAL, artist_id INTEGER REFERENCES artists, for_sale BOOLEAN, UNIQUE(artwork COLLATE NOCASE))'

        enable_fk = 'PRAGMA foreign_keys = ON'

        with sqlite3.connect(db_path) as conn:
            conn.execute(enable_fk)  # ensures foreign key support is enabled on older versions of Python
            conn.execute(create_artist_table)
            conn.execute(create_artwork_table)
        conn.close()

    def _add_artist(self, artist):
        """ Adds artist to db.
        Raises BookError if a book with exact author and title (not case sensitive) is already in the store.
        :param artist the Book to add """

        insert_artist = 'INSERT INTO artists (name, email, artist_id) VALUES (?, ?, ?)'

        try:
            with sqlite3.connect(db_path) as conn:
                res = conn.execute(insert_artist, (artist.name, artist.email, artist.artist_id))
                new_id = res.lastrowid  # Get the ID of the new row in the table
                artist.artist_id = new_id  # Set this artist's ID
            conn.close()
            return True
        except sqlite3.IntegrityError:
            print(f'Error - {artist} is already in the database.')
            return False

    def _add_artwork(self, artwork):
        """ Adds artwork to store.
        Raises BookError if a book with exact author and title (not case sensitive) is already in the store.
        :param artist the Book to add """

        insert_artwork = 'INSERT INTO artworks (artwork, price, artist_id, for_sale) VALUES (?, ?, ?, ?)'

        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute(insert_artwork, (artwork.artwork, artwork.price, artwork.artist_id, artwork.for_sale))
                # new_id = res.lastrowid  # Get the ID of the new row in the table
                # artwork.artist_id = new_id  # Set this artist's ID
        except sqlite3.IntegrityError as e:
            raise ArtworkError(f'Error - this artist is already in the database. {artwork}') from e
        finally:
            conn.close()

    def _update_availability(self, artwork):
        """ Updates the information for an artwork. Assumes id has not changed and updates author, title and read values
        Raises BookError if book does not have id
        :param artwork the Artwork to update
        """

        if not artwork.artist_id:
            raise ArtworkError('Book does not have ID, can\'t update')

        query_update_availability = 'UPDATE artworks SET artwork = ?, price = ?, artist_id = ?, for_sale = ? WHERE artist_id = ?'

        with sqlite3.connect(db_path) as conn:
            updated = conn.execute(query_update_availability, (artwork.artwork, artwork.price, artwork.artist_id, artwork.for_sale))
            rows_modified = updated.rowcount

        conn.close()

        if rows_modified == 0:
            raise ArtworkError(f'Artwork with id {artwork.id} not found.')

    def _get_artist_id(self, artist_name):

        # search_term = artist_name
        # search_term = '%'+search_term+'%'

        query_id = 'SELECT artist_id FROM artists WHERE name LIKE ?'

        try:
            with sqlite3.connect(db_path) as conn:
                artist_id = conn.execute(query_id, (artist_name,)).fetchone()[0]
        except TypeError as e:
            raise ArtworkError(f'Error - this artist is not in the database. {artist_name}') from e
        finally:
            conn.close()

        return artist_id


    # def __new__(cls):
    #     """ The __new__ magic method handles object creation. (Compare to __init__ which initializes an object.)
    #     If there's already a Bookstore instance, return that. If not, then create a new one
    #     This way, there can only ever be one __Bookstore, which uses the same database. """
    #
    #     if not ArtworkStore.instance:
    #         ArtworkStore.instance = ArtworkStore.__BookStore()
    #     return ArtworkStore.instance
    #
    # def __getattr__(self, name):
    #     return getattr(self.instance, name)
    #
    # def __setattr__(self, name, value):
    #     return setattr(self.instance, name, value)
