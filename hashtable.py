class HashTable:

    def __init__(self, initial_capacity=10):
        self.table = []
        self.keys = []
        for i in range(initial_capacity):
            self.table.append([])

    def __iter__(self):
        all_entries = []
        for key in self.keys:
            all_entries.append(self.get(key))
        return iter(all_entries)

    def put(self, key, item):
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]
        self.keys.append(key)
        bucket_list.append(HashEntry(key, item))

    def hash_key(self, key):
        bucket = hash(key) % len(self.table)
        return bucket

    def get(self, key):
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]

        for entry in bucket_list:
            if entry.key == key:
                return entry.item

        return None

    def get_bucket(self, key):
        bucket = self.hash_key(key)
        return self.table[bucket]

    def get_table(self):
        return self.table

    def keys(self):
        return self.keys


class HashEntry:

    def __init__(self, key, item):
        self.key = key
        self.item = item

