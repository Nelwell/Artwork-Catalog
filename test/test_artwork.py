import sqlite3
import unittest
from unittest import TestCase

import database_config

test_artwork_db_path = 'database/test_artist_artwork.db'
database_config.db_path = test_artwork_db_path

from artist import Artist
from artwork_store import ArtworkStore
from errors import ArtworkError
from artwork import Artwork

artwork = Artwork(artwork='', price=float, artist_id=int, for_sale=True)
artwork_store = ArtworkStore()


class TestArtistArtworksDB(TestCase):

    def setUp(self):
        # ensure tables exist and clear DB so it's empty before tests start

        ArtworkStore()

        with sqlite3.connect(test_artwork_db_path) as conn:
            conn.execute('DELETE FROM artists')
            conn.execute('DELETE FROM artworks')
        conn.close()

    def test_all_artwork_associated_with_artist_id_is_returned(self):
        # List of artists with unique IDs
        example_artist_list = [Artist('John', 'john@gmail.com', 1),
                               Artist('Gary', 'gary@hotmail.com', 3)]

        # add each to db
        for artist in example_artist_list:
            artwork_store._add_artist(artist)

        # list of artworks assigned to artist IDs
        example_artwork_list = [Artwork('Pigeon Scape', 150, 1, True),
                                Artwork('Tarnished Hallow', 75, 1, False),
                                Artwork('Bog Keeper', 140, 1, True),
                                Artwork('Dance Rush', 20, 1, True),
                                Artwork('Patchwork Sammy', 85, 5, True),
                                Artwork('Basked Valley', 560, 3, False),
                                Artwork('Patchwork Sammy', 85, 4, True),
                                Artwork('Baked Patty', 1600, 3, False)]

        # add each artwork to db
        for art in example_artwork_list:
            artwork_store._add_artwork(art)

        # what is actually found in db based on artist ID foreign key
        actual_john_artwork_list = artwork.get_all_artist_artwork(1)
        actual_gary_artwork_list = artwork.get_all_artist_artwork(3)

        # what's expected from db when ran from John and Gary (artists)
        expected_john_artwork = [Artwork('Pigeon Scape', 150, 1, True),
                                 Artwork('Tarnished Hallow', 75, 1, False),
                                 Artwork('Bog Keeper', 140, 1, True),
                                 Artwork('Dance Rush', 20, 1, True)]

        expected_gary_artwork = [Artwork('Basked Valley', 560, 3, False),
                                 Artwork('Baked Patty', 1600, 3, False)]

        # Checks that list of tuples are equivalent to each other
        self.assertListEqual(expected_john_artwork, actual_john_artwork_list)
        self.assertListEqual(expected_gary_artwork, actual_gary_artwork_list)

    # Test found bug where function was not returning a list, but just a single artwork object - fixed
    def test_only_artworks_searched_by_given_id_are_returned(self):
        # List of artists with unique IDs
        example_artist_list = [Artist('John', 'john@gmail.com', 1),
                               Artist('Gary', 'gary@hotmail.com', 3),
                               Artist('Paula', 'paula@yahoo.com', 5)]

        # add each to db
        for artist in example_artist_list:
            artwork_store._add_artist(artist)

        # list of artworks assigned to artist IDs
        example_artwork_list = [Artwork('Pigeon Scape', 150, 1, True),
                                Artwork('Tarnished Hallow', 75, 1, False),
                                Artwork('Bog Keeper', 140, 1, True),
                                Artwork('Dance Rush', 20, 1, True),
                                Artwork('Patchwork Sammy', 85, 5, True),
                                Artwork('Basked Valley', 560, 3, False),
                                Artwork('Patchwork Sammy', 85, 4, True),
                                Artwork('Baked Patty', 1600, 3, False)]

        # add each artwork to db
        for art in example_artwork_list:
            artwork_store._add_artwork(art)

        # what is actually found in db based on artwork ID foreign key of Artist ID
        actual_artwork_id_1_list = artwork.get_artwork_by_id(1)
        actual_artwork_id_3_list = artwork.get_artwork_by_id(3)
        actual_artwork_id_5_list = artwork.get_artwork_by_id(5)

        # what is expected from db when ran based on provided Artwork IDs
        expected_artwork_id_1_list = [Artwork('Pigeon Scape', 150, 1, True),
                                      Artwork('Tarnished Hallow', 75, 1, False),
                                      Artwork('Bog Keeper', 140, 1, True),
                                      Artwork('Dance Rush', 20, 1, True)]

        expected_artwork_id_3_list = [Artwork('Basked Valley', 560, 3, False),
                                      Artwork('Baked Patty', 1600, 3, False)]

        expected_artwork_id_5_list = [Artwork('Patchwork Sammy', 85, 5, True)]

        # Checks that list of tuples are equivalent to each other
        self.assertListEqual(expected_artwork_id_1_list, actual_artwork_id_1_list)
        self.assertListEqual(expected_artwork_id_3_list, actual_artwork_id_3_list)
        self.assertEqual(expected_artwork_id_5_list, actual_artwork_id_5_list)

    def test_only_available_artist_artworks_are_returned(self):
        # List of artists with unique IDs
        example_artist_list = [Artist('John', 'john@gmail.com', 1),
                               Artist('Gary', 'gary@hotmail.com', 3),
                               Artist('Paula', 'paula@yahoo.com', 5)]

        # add each to db
        for artist in example_artist_list:
            artwork_store._add_artist(artist)

        # list of artworks with availability statuses of True or False
        example_artwork_list = [Artwork('Pigeon Scape', 150, 1, True),
                                Artwork('Tarnished Hallow', 75, 1, False),
                                Artwork('Bog Keeper', 140, 1, True),
                                Artwork('Dance Rush', 20, 1, True),
                                Artwork('Patchwork Sammy', 85, 5, True),
                                Artwork('Basked Valley', 560, 3, False),
                                Artwork('Patchwork Sammy', 85, 4, True),
                                Artwork('Baked Patty', 1600, 3, False)]

        # add each artwork to db
        for art in example_artwork_list:
            artwork_store._add_artwork(art)

        # returned artworks with True status of availability based on given Artowrk ID foreign key to Artist ID primary key
        actual_available_artwork_id_1_list = artwork.get_all_artist_available_artwork(1)
        actual_available_artwork_id_3_list = artwork.get_all_artist_available_artwork(3)
        actual_available_artwork_id_5_list = artwork.get_all_artist_available_artwork(5)

        # what is expected from db when ran based on provided Artwork IDs
        expected_available_artwork_id_1_list = [Artwork('Pigeon Scape', 150, 1, True),
                                                Artwork('Bog Keeper', 140, 1, True),
                                                Artwork('Dance Rush', 20, 1, True)]

        expected_available_artwork_id_3_list = []

        expected_available_artwork_id_5_list = [Artwork('Patchwork Sammy', 85, 5, True)]

        # Checks that list of tuples are equivalent to each other
        self.assertListEqual(expected_available_artwork_id_1_list, actual_available_artwork_id_1_list)
        self.assertListEqual(expected_available_artwork_id_3_list, actual_available_artwork_id_3_list)
        self.assertEqual(expected_available_artwork_id_5_list, actual_available_artwork_id_5_list)

    def get_artwork_data(self):
        with sqlite3.connect(test_artwork_db_path) as conn:
            rows = conn.execute('SELECT * FROM artworks').fetchall()
        conn.close()
        return rows


if __name__ == '__main__':
    unittest.main()
