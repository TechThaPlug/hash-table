
from hash_table import HashTable


def main():
    table = HashTable()

    print("=" * 45)
    print("          HASH TABLE DEMONSTRATION")
    print("=" * 45)

    # Add items
    table.add("golf", "sport")
    table.add("rose", "flower")

    # Add colliding keys
    table.add("dear", "friend")
    table.add("read", "book")

    print("\n1. Initial hash table:")
    print(table.collection)

    # Look up values
    print("\n2. Looking up values:")
    print("golf:", table.lookup("golf"))
    print("rose:", table.lookup("rose"))
    print("dear:", table.lookup("dear"))
    print("read:", table.lookup("read"))

    # Demonstrate collision handling
    print("\n3. Collision handling:")
    print("'dear' hash:", table.hash("dear"))
    print("'read' hash:", table.hash("read"))
    print("Both keys share the same bucket.")

    # Remove one colliding key
    print("\n4. Removing 'dear':")
    table.remove("dear")

    print("dear:", table.lookup("dear"))
    print("read:", table.lookup("read"))

    print("\n5. Final hash table:")
    print(table.collection)

    print("\nHash table demonstration completed!")


if __name__ == "__main__":
    main()
