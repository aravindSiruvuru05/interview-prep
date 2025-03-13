'''

class Node {
    int data; // 4 bytes
    Node left; 
    Node right; 
}

12 bytes per node 


             3
        22         5            = 84 bytes
               4       66
                
                  6         7
    
    [3, 22, 5, 21, 43, 4, 66, , , , , 6, 7] = str
    (7, 8, 9)
    
    2i + 1,  2i + 2
      
Max int: "2147483647"

size of this tree: 

 7 * 12 = 84 bytes
 7 * 4 = 28 bytes
 
 Requirements: 
 
 (i) space is minimized 
 (ii) given access to a node, find children in O(1) time
 
'''
from collections import deque

class Node:
    # node class, with left right and data
    pass 

class CompactTree: 
    
    def __init__(self, root, height):
        self.root = root
        self.height = height
        self.data = [] * ((2 ** height) - 1)
        self.emptyIdx = set()
        self.processData()
        
    def processData(self):
        curr = self.root
        q = deque([(curr, 0)])
        
        while q:
            node, i = q.popleft()
            self.data[i] = node.data
            
            if node.left and node.data:
                q.append((node.left, (2* i) + 1))
            else:
                self.emptyIdx.add((2* i) + 1)
                q.append((, (2* i) + 1))
            
            if node.right:
                q.append((node.right, (2* i) + 2))
            else:
                self.emptyIdx.add((2* i) + 2)
                
        return self.data
        
            
            
    
    
        
        
# this goes infinity as we are going recursivly even we are addin in else block so check for max lenght of array we are taking only then we push to q

        
        
        
        
        
        
        
        
        