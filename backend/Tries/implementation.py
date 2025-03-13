class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """ Inserts a word into the Trie """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """ Searches for an exact word in the Trie """
        node = self.root
        for char in word:
            if char not in node.children:
                return False  # Word not found
            node = node.children[char]
        return node.is_end_of_word  # Return True if it's a complete word

    def starts_with(self, prefix):
        """ Checks if there is any word in the Trie that starts with a given prefix """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False  # Prefix not found
            node = node.children[char]
        return True  # Prefix exists in the Trie

    def search_with_prefix(self, prefix):
        """ Returns all words that start with the given prefix """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # No words with this prefix
            node = node.children[char]

        words = []
        self._dfs(node, prefix, words)
        return words

    def _dfs(self, node, prefix, words):
        """ Helper DFS function to collect words from a given TrieNode """
        if node.is_end_of_word:
            words.append(prefix)
        for char, next_node in node.children.items():
            self._dfs(next_node, prefix + char, words)


# Example Usage:
words = ["apple", "app", "apricot", "banana", "bat", "batman", "cat", "cap"]
trie = Trie()

# Insert words into Trie
for word in words:
    trie.insert(word)

# Search for exact words
print(trie.search("apple"))      # True
print(trie.search("appl"))       # False
print(trie.search("banana"))     # True
print(trie.search("batman"))     # True
print(trie.search("batwoman"))   # False

# Search for words with a given prefix
print(trie.starts_with("ap"))    # True
print(trie.starts_with("bat"))   # True
print(trie.starts_with("cap"))   # True
print(trie.starts_with("dog"))   # False

# Find all words with a given prefix
print(trie.search_with_prefix("ap"))   # ['apple', 'app', 'apricot']
print(trie.search_with_prefix("bat"))  # ['bat', 'batman']
print(trie.search_with_prefix("c"))    # ['cat', 'cap']
print(trie.search_with_prefix("z"))    # []

