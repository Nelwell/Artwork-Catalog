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

artwork = Artwork(artwork='', price=float, artist_id=int, for_sale=True)
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
        actual_rows = self.get_artist_data()

        # assertCountEqual will compare two iterables, e.g. a list of tuples returned from DB
        self.assertCountEqual(expected_rows, actual_rows)

        example_artist2 = Artist('Cassie', 'cassie@yahoo.com', 2)
        add_artist_example2 = artwork_store._add_artist(example_artist2)

        self.assertTrue(add_artist_example2)

        expected_results = [('john', 'john@gmail.com', 1), ('Cassie', 'cassie@yahoo.com', 2)]
        actual_results = self.get_artist_data()

        self.assertCountEqual(expected_results, actual_results)

    def test_confirm_artwork_added(self):
        example_artwork = Artwork('summer day', 50.99, 3, True)
        add_artwork_example = artwork_store._add_artwork(example_artwork)

        self.assertTrue(add_artwork_example)

    def test_add_artist_with_same_email_returns_false_and_raises_integrity_error(self):
        artist_one_example = Artist('Harry', 'harry@gmail.com', 3)
        artwork_store._add_artist(artist_one_example)

        same_artist_email = Artist('Potter', 'harry@gmail.com', 4)
        add_same_email = artwork_store._add_artist(same_artist_email)  # shouldn't be allowed to add duplicate email

        self.assertFalse(add_same_email)
        self.assertRaises(sqlite3.IntegrityError)  # should also raise IntegrityError upon adding second entry with same email

        expected_rows = [('Harry', 'harry@gmail.com', 3)]  # only first artist should be in db
        actual_rows = self.get_artist_data()

        # assertCountEqual will compare two iterables, e.g. a list of tuples returned from DB
        self.assertCountEqual(expected_rows, actual_rows)

    def test_add_artwork_with_same_name_returns_false_and_raises_integrity_error(self):
        artwork_example = Artwork('Lunar Flesh', 65.99, 6, True)
        artwork_store._add_artwork(artwork_example)

        artwork_same_name_example = Artwork('Lunar Flesh', 35.55, 7, False)
        same_name_artwork_added = artwork_store._add_artwork(artwork_same_name_example)

        self.assertFalse(same_name_artwork_added)
        self.assertRaises(sqlite3.IntegrityError)  # should raise IntegrityError with artwork of same name regardless of other parameter values

        artwork_example2 = Artwork('Cream Skies', 1200, 8, False)
        artwork_store._add_artwork(artwork_example2)

        expected_rows = [('Lunar Flesh', 65.99, 6, True), ('Cream Skies', 1200, 8, False)]  # only artworks with unique names should be found in db
        actual_rows = self.get_artwork_data()

        # assertCountEqual will compare two iterables, e.g. a list of tuples returned from DB
        self.assertCountEqual(expected_rows, actual_rows)

    def get_artist_data(self):
        with sqlite3.connect(test_db_path) as conn:
            rows = conn.execute('SELECT * FROM artists').fetchall()
        conn.close()
        return rows

    def get_artwork_data(self):
        with sqlite3.connect(test_db_path) as conn:
            rows = conn.execute('SELECT * FROM artworks').fetchall()
        conn.close()
        return rows


if __name__ == '__main__':
    unittest.main()
