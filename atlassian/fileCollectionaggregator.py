# 📌 Problem Statement: Collection Size Tracker
# You are asked to implement a system to track file sizes across multiple collections in a storage system.
# Each file can belong to one or more collections. Files can be added or deleted, and collections can be dynamically created or removed as files are added or deleted.

# 📊 Requirements:
# Track the total size of each collection.

# Get the top N collections by total size at any point in time.

# If a collection’s total size becomes zero, it should be removed completely.

# Multiple collections can be attached to a file — when adding or deleting a file, update all relevant collections' total sizes.

# ✏️ Operations to Support:
# add_file(collections, file_size)
# → Adds a file of file_size to all collections listed.

# delete_file(collections, file_size)
# → Deletes a file of file_size from all collections listed.

# get_top_n_collections(n)
# → Returns the top n collections sorted by their total size in descending order.

from sortedcontainers import SortedDict # type: ignore
from collections import defaultdict

class CollectionTracker:
    def __init__(self):
        self.size_to_collections = SortedDict()    # size -> set of collections
        self.collection_sizes = defaultdict(int)   # collection -> total size

    def _update_size_group(self, collection, old_size, new_size):
        # Remove collection from old size group
        if old_size in self.size_to_collections:
            self.size_to_collections[old_size].remove(collection)
            if not self.size_to_collections[old_size]:
                del self.size_to_collections[old_size]

        # Add collection to new size group (if new_size > 0)
        if new_size > 0:
            if new_size not in self.size_to_collections:
                self.size_to_collections[new_size] = set()
            self.size_to_collections[new_size].add(collection)

    def add_file(self, collections, file_size):
        for collection in collections:
            old_size = self.collection_sizes[collection]
            new_size = old_size + file_size

            self._update_size_group(collection, old_size, new_size)
            self.collection_sizes[collection] = new_size

    def delete_file(self, collections, file_size):
        for collection in collections:
            old_size = self.collection_sizes[collection]
            new_size = old_size - file_size

            self._update_size_group(collection, old_size, new_size)

            if new_size > 0:
                self.collection_sizes[collection] = new_size
            else:
                del self.collection_sizes[collection]  # remove collection if size zero

    def get_top_n_collections(self, n):
        result = []
        for size in reversed(self.size_to_collections):
            for collection in self.size_to_collections[size]:
                result.append((collection, size))
                if len(result) == n:
                    return result
        return result

# -------------------------
# ✅ Example Usage

tracker = CollectionTracker()

# Adding files
tracker.add_file(["A"], 100)
tracker.add_file(["B"], 200)
tracker.add_file(["A", "C"], 150)  # file linked to multiple collections

print("Top 2 collections after adding files:")
print(tracker.get_top_n_collections(2))  # Expected: [('A', 250), ('B', 200)]

# Deleting a file
tracker.delete_file(["A", "C"], 150)

print("Top 2 collections after deleting:")
print(tracker.get_top_n_collections(2))  # Expected: [('B', 200), ('A', 100)]
