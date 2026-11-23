
class HashTable:
    """A hash table that handles collisions using separate chaining."""

    def __init__(self):
        self.collection = {}

    def hash(self, key):
        """Calculate a hash value from a string key."""
        return sum(ord(character) for character in key)

    def add(self, key, value):
        """Add a key-value pair to the hash table."""
        key_hash = self.hash(key)

        if key_hash not in self.collection:
            self.collection[key_hash] = {}

        self.collection[key_hash][key] = value

    def remove(self, key):
        """Remove a key-value pair without affecting collisions."""
        key_hash = self.hash(key)

        if key_hash in self.collection and key in self.collection[key_hash]:
            del self.collection[key_hash][key]

            if not self.collection[key_hash]:
                del self.collection[key_hash]

    def lookup(self, key):
        """Return the value associated with a key, or None."""
        key_hash = self.hash(key)

        if key_hash in self.collection:
            return self.collection[key_hash].get(key)

        return None
