

# The Hash Table aids the packages in being quickly accessed throughout the program
class HashTable:

    def __init__(self, initial_capacity=10):
        self.table = []
        self.keys = []
        for i in range(initial_capacity):
            self.table.append([])

    # Adds a entry to the hash table
    def put(self, key, item):
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]
        if key not in self.keys:
            self.keys.append(key)
        bucket_list.append(HashEntry(key, item))

    # Adds a key to the hash table
    def hash_key(self, key):
        bucket = hash(key) % len(self.table)
        return bucket

    # Access an entry using a key from the hash table
    def get(self, key):
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]

        # O(n)
        for entry in bucket_list:
            if entry.key == key:
                return entry.item

        return None

    # Remove an entry using a key from the hash table
    def remove(self, key, item):
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]

        # O(n)
        for entry in bucket_list:
            if entry.item == item:
                bucket_list.remove(entry)
                break

    # Access an entire bucket or list from the hash table
    def get_bucket(self, key):
        bucket = self.hash_key(key)
        return self.table[bucket]

    # Access the entire table of the hash table
    def get_table(self):
        return self.table

    # Access the keys on the hash table
    def keys(self):
        return self.keys


# The Hash Entry holds onto all the information for each entry in the hash table
class HashEntry:

    def __init__(self, key, item):
        self.key = key
        self.item = item

