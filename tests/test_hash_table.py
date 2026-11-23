
import unittest

from hash_table import HashTable


class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.table = HashTable()

    def test_collection_starts_empty(self):
        self.assertEqual(self.table.collection, {})

    def test_hash_golf(self):
        self.assertEqual(self.table.hash("golf"), 424)

    def test_hash_dear(self):
        self.assertEqual(self.table.hash("dear"), 412)

    def test_hash_read(self):
        self.assertEqual(self.table.hash("read"), 412)

    def test_hash_fcc(self):
        self.assertEqual(self.table.hash("fcc"), 300)

    def test_hash_cfc(self):
        self.assertEqual(self.table.hash("cfc"), 300)

    def test_add_item(self):
        self.table.add("rose", "flower")
        self.assertEqual(
            self.table.collection,
            {441: {"rose": "flower"}}
        )

    def test_add_multiple_items(self):
        self.table.add("golf", "sport")
        self.table.add("rose", "flower")

        self.assertEqual(self.table.lookup("golf"), "sport")
        self.assertEqual(self.table.lookup("rose"), "flower")

    def test_add_collision(self):
        self.table.add("dear", "friend")
        self.table.add("read", "book")

        self.assertEqual(
            self.table.collection[412],
            {"dear": "friend", "read": "book"}
        )

    def test_add_second_collision(self):
        self.table.add("fcc", "coding")
        self.table.add("cfc", "chemical")

        self.assertEqual(
            self.table.collection[300],
            {"fcc": "coding", "cfc": "chemical"}
        )

    def test_lookup_existing_key(self):
        self.table.add("golf", "sport")
        self.assertEqual(self.table.lookup("golf"), "sport")

    def test_lookup_missing_key(self):
        self.assertIsNone(self.table.lookup("missing"))

    def test_lookup_collision(self):
        self.table.add("dear", "friend")
        self.table.add("read", "book")

        self.assertEqual(self.table.lookup("dear"), "friend")
        self.assertEqual(self.table.lookup("read"), "book")

    def test_remove_existing_key(self):
        self.table.add("golf", "sport")
        self.table.remove("golf")

        self.assertIsNone(self.table.lookup("golf"))

    def test_remove_missing_key(self):
        self.table.remove("missing")
        self.assertEqual(self.table.collection, {})

    def test_remove_preserves_collision(self):
        self.table.add("dear", "friend")
        self.table.add("read", "book")

        self.table.remove("dear")

        self.assertIsNone(self.table.lookup("dear"))
        self.assertEqual(self.table.lookup("read"), "book")

    def test_remove_last_collision(self):
        self.table.add("dear", "friend")
        self.table.remove("dear")

        self.assertNotIn(412, self.table.collection)

    def test_update_existing_key(self):
        self.table.add("golf", "sport")
        self.table.add("golf", "game")

        self.assertEqual(self.table.lookup("golf"), "game")

    def test_empty_string_key(self):
        self.table.add("", "empty")
        self.assertEqual(self.table.lookup(""), "empty")

    def test_remove_empty_string_key(self):
        self.table.add("", "empty")
        self.table.remove("")

        self.assertIsNone(self.table.lookup(""))

    def test_multiple_collisions_and_removals(self):
        self.table.add("dear", "friend")
        self.table.add("read", "book")
        self.table.add("dare", "challenge")

        self.table.remove("read")

        self.assertEqual(self.table.lookup("dear"), "friend")
        self.assertIsNone(self.table.lookup("read"))
        self.assertEqual(self.table.lookup("dare"), "challenge")


if __name__ == "__main__":
    unittest.main()
