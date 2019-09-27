class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def put(self, key, item):
        # get the bucket list where this item will go.
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]

        # insert the item to the end of the bucket list.
        bucket_list.append(HashEntry(key, item))

    def hash_key(self, key):
        bucket = hash(key) % len(self.table)
        return bucket

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def get(self, key):
        # get the bucket list where this key would be.
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for entry in bucket_list:
            if entry.key == key:
                return entry.item
        # the key is not found.
        return None

    def get_bucket(self, key):
        # get the bucket list where this key would be.
        bucket = self.hash_key(key)
        return self.table[bucket]

    def get_table(self):
        return self.table


class HashEntry:

    def __init__(self, key, item):
        self.key = key
        self.item = item

