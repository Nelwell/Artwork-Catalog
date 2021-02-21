import sqlite3
import unittest
from unittest import TestCase

import database_config

test_db_path = 'database/test_artworks.db'
database_config.db_path = test_db_path

from artist import Artist
from artwork_store import ArtworkStore
from errors import ArtworkError

from artwork import Artwork

artwork_store = ArtworkStore()


class TestArtworksDB(TestCase):

    def setUp(self):
        # ensure tables exist and clear DB so it's empty before tests start

        ArtworkStore()

        with sqlite3.connect(test_db_path) as conn:
            conn.execute('DELETE FROM artists')
            conn.execute('DELETE FROM artworks')
        conn.close()

    def test_confirm_artist_added(self):
        example_artist = Artist('john', 'john@gmail.com', 1)
        add_artist_example = artwork_store._add_artist(example_artist)

        self.assertTrue(add_artist_example)

        expected_rows = [('john', 'john@gmail.com', 1)]
        actual_rows = self.get_all_data()

        # assertCountEqual will compare two iterables, e.g. a list of tuples returned from DB
        self.assertCountEqual(expected_rows, actual_rows)

        example_artist2 = Artist('Cassie', 'cassie@yahoo.com', 2)
        add_artist_example2 = artwork_store._add_artist(example_artist2)

        self.assertTrue(add_artist_example2)

        expected_results = [('john', 'john@gmail.com', 1), ('Cassie', 'cassie@yahoo.com', 2)]
        actual_results = self.get_all_data()

        self.assertCountEqual(expected_results, actual_results)

    def test_confirm_artwork_added(self):
        example_artwork = Artwork('summer day', 50.99, 3, True)
        add_artwork_example = artwork_store._add_artwork(example_artwork)

        self.assertTrue(add_artwork_example)

    def test_add_artist_with_same_email(self):
        artist_one = Artist('Harry', 'harry@gmail.com')
        artwork_store._add_artist(artist_one)

        same_artist_email = Artist('Potter', 'harry@gmail.com')
        add_same_email = artwork_store._add_artist(same_artist_email)  # shouldn't be allowed to add duplicate email

        self.assertFalse(add_same_email)
        self.assertRaises(sqlite3.IntegrityError)

        # expected_rows = [('Jake', 'jake@gmail.com')]  # only first artist
        # actual_rows = self.get_all_data()

        # assertCountEqual will compare two iterables, e.g. a list of tuples returned from DB
        # self.assertCountEqual(expected_rows, actual_rows)

        # expected_rows = [('Example', 25)]
        # actual_rows = self.get_all_data()
        #
        # # assertCountEqual will compare two iterables, e.g. a list of tuples returned from DB
        # self.assertCountEqual(expected_rows, actual_rows)
        #
        # example2 = Artist('Another Example', 30)
        # added2 = test_db_path.add_artist(example2)
        #
        # self.assertTrue(added2)
        #
        # expected_rows = [('Example', 25), ('Another Example', 30)]
        # actual_rows = self.get_all_data()
        #
        # self.assertCountEqual(expected_rows, actual_rows)

    # def test_add_duplicate_name_artist(self):
    #     example = Artist('Example', 25)
    #     added = test_db_path.add_artist(example)
    #
    #     example2 = Artist('Example', 40)  # same name
    #     added2 = test_db_path.add_artist(example2)
    #
    #     self.assertFalse(added2)
    #
    #     expected_rows = [('Example', 25)]  # only one artist
    #     actual_rows = self.get_all_data()
    #
    #     # assertCountEqual will compare two iterables, e.g. a list of tuples returned from DB
    #     self.assertCountEqual(expected_rows, actual_rows)
    #
    # def get_all_data(self):
    #     with sqlite3.connect('test_art.sqlite') as conn:
    #         rows = conn.execute('SELECT * FROM artist').fetchall()
    #     conn.close()
    #     return rows

    def get_all_data(self):
        with sqlite3.connect(test_db_path) as conn:
            rows = conn.execute('SELECT * FROM artists').fetchall()
        conn.close()
        return rows


if __name__ == '__main__':
    unittest.main()
