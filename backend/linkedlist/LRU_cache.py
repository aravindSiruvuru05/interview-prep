

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class LRUCache:
    def __init__(self, size):
        self.size = size
        self.cache = {}
        self.head = None
        self.tail = None
        self.head.next = self.tail
        self.tail.prev = self.head

   
    def add(self, node):
        next = self.head.next
        self.head.next = node
        
        node.prev = self.head
        node.next = next

        next.prev = node
    
   
    def remove(self, node):
        l = node.left
        r = node.right
        l.right = r
        r.left = l
    
    def put(self, key, val):
        if key in self.cache:
            node = self.cache[key]

            node.val = val

            self.remove(node)
            self.add(node)
        else:
            if len(self.cache) >= self.size:
                lru = self.tail.prev
                self.remove(lru)
                del self.cache[key]
            nn = Node(val)
            self.cache[key] = nn
            self.add(nn)

    def get(self, key):
        if key in self.cache:
            curr = self.cache[key]
            self.remove(curr)
            self.add(curr)
            return curr.val
        return -1



cache = LRUCache(3)

cache.put(1, 1) 
cache.put(2, 2) 
cache.put(3, 3) 

print(cache.get(1)) 

cache.put(4, 4) 

print(cache.get(2)) 
print(cache.get(3)) 
print(cache.get(4)) 
