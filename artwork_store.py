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
        create_artist_table = 'CREATE TABLE IF NOT EXISTS artists (name TEXT COLLATE NOCASE, email TEXT COLLATE NOCASE, artist_id INTEGER PRIMARY KEY)'

        create_artwork_table = 'CREATE TABLE IF NOT EXISTS artworks (artwork TEXT, price REAL, artist_id INTEGER REFERENCES artists, for_sale BOOLEAN, UNIQUE(artwork COLLATE NOCASE))'

        conn = sqlite3.connect(db_path)
        enable_fk = 'PRAGMA foreign_keys = ON'

        with conn:
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
        except sqlite3.IntegrityError as e:
            raise ArtworkError(f'Error - this artist is already in the database. {artist}') from e
        finally:
            conn.close()

    def _add_artwork(self, artwork):
        """ Adds artwork to store.
        Raises BookError if a book with exact author and title (not case sensitive) is already in the store.
        :param artist the Book to add """

        insert_artwork = 'INSERT INTO artworks (artwork, price, artist_id, for_sale) VALUES (?, ?, ?, ?)'

        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute(insert_artwork, (artwork.artwork, artwork.price, artwork.artist_id, artwork.for_sale))
                # artist = conn.execute('select * from artists where name = ?', artwork.artist_id)
                # print(artist)
                # new_id = res.lastrowid  # Get the ID of the new row in the table
                # artwork.artist_id = new_id  # Set this artist's ID
        except sqlite3.IntegrityError as e:
            raise ArtworkError(f'Error - this artist is already in the database. {artwork}') from e
        finally:
            conn.close()

    def _get_artist_id(self, artist_name):
        query_id = 'SELECT artist_id FROM artists WHERE name LIKE ?'
        try:
            with sqlite3.connect(db_path) as conn:
                artist_id = conn.execute(query_id, (artist_name,)).fetchone()[0]
        except sqlite3.IntegrityError as e:
            raise ArtworkError(f'Error - this artist is already in the database. {artist_name}') from e
        finally:
            conn.close()
        return artist_id
