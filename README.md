# Python Hash Table

A Python implementation of a hash table using separate chaining to handle hash collisions.

## Features

- Hash calculation using character ASCII values.
- Add key-value pairs.
- Look up stored values.
- Remove individual key-value pairs.
- Handle hash collisions using nested dictionaries.
- Preserve other entries when removing a colliding key.
- Automated unit tests using Python's unittest framework.

## Project Structure

```text
hash-table/
├── tests/
│   └── test_hash_table.py
├── hash_table.py
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Requirements

- Python 3.13 or later.

No external dependencies are required.

## Installation

Clone the repository:

```bash
git clone https://github.com/TechThaPlug/hash-table.git
cd hash-table
```

Create a virtual environment:

```bash
py -3.13 -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

## Usage

Run the demonstration:

```bash
python main.py
```

## Running Tests

Execute the automated test suite:

```bash
python -m unittest discover -s tests -v
```

## How It Works

The hash function calculates the sum of the ASCII values of every character in a string.

For example:

```python
hash("golf")  # 424
```

Different keys can produce the same hash value. This is called a collision.

This implementation handles collisions through separate chaining, storing multiple key-value pairs in a nested dictionary under the same hash value.

Example:

```python
{
    412: {
        "dear": "friend",
        "read": "book"
    }
}
```

## License

This project is licensed under the MIT License.
