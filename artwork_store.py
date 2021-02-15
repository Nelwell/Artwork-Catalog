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

        create_artwork_table = 'CREATE TABLE IF NOT EXISTS artworks (artist_id INTEGER REFERENCES artists, artwork TEXT, price REAL, for_sale BOOLEAN, UNIQUE(artwork COLLATE NOCASE))'

        conn = sqlite3.connect(db_path)
        # enable_fk = 'PRAGMA foreign_keys = ON'

        with conn:
            # conn.execute(enable_fk)
            conn.execute(create_artist_table)
            conn.execute(create_artwork_table)

        conn.close()

    def _commit_artist(self, artist):
        """ Adds book to store.
        Raises BookError if a book with exact author and title (not case sensitive) is already in the store.
        :param artist the Book to add """

        insert_sql = 'INSERT INTO artists (name, email, artist_id) VALUES (?, ?, ?)'

        try:
            with sqlite3.connect(db_path) as conn:
                res = conn.execute(insert_sql, (artist.name, artist.email, artist.artist_id))
                new_id = res.lastrowid  # Get the ID of the new row in the table
                artist.id = new_id  # Set this book's ID
        except sqlite3.IntegrityError as e:
            raise ArtworkError(f'Error - this artist is already in the database. {artist}') from e
        finally:
            conn.close()
