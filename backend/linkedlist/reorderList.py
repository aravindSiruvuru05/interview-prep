# Reorder Linked List
# You are given the head of a singly linked-list.

# The positions of a linked list of length = 7 for example, can intially be represented as:

# [0, 1, 2, 3, 4, 5, 6]

# Reorder the nodes of the linked list to be in the following order:

# [0, 6, 1, 5, 2, 4, 3]

# Notice that in the general case for a list of length = n the nodes are reordered to be in the following order:

# [0, n-1, 1, n-2, 2, n-3, ...]

# You may not modify the values in the list's nodes, but instead you must reorder the nodes themselves.

# Example 1:

# Input: head = [2,4,6,8]

# Output: [2,8,4,6]

class Node:
    def __init__(self, val, next):
        self.val = val
        self.next = next
    

class LL:
    def __init__(self, head = None):
        self.head = head
        
    def helper(self, revNode):
        if not revNode: # we go till the end of linked list and then return the initial nodes one by one as we will get the revrse node from the parameter
            return self.head
        curr = self.helper(revNode.next)
        temp = curr.next
        curr.next = revNode
        revNode.next = temp
        return temp

    def reorder(self):
        self.helper(self.head)

def printLL(head):
    temp = head
    while temp:
        print(temp.val)
        temp = temp.next 

n1 = Node(1, Node(2, Node(3, Node(4, Node(5, None)))))
ll = LL(n1)

ll.reorder()

printLL(ll.head)



    
