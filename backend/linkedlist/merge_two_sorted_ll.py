class Node:
    def __init__(self, val, next):
        self.val = val
        self.next = next
    

def merge(l1: Node, l2: Node):  # SO(M + N) TO(M + N)
    if not l1.next:
        return l2
    if not l2.next:
        return l1
    
    if l1.val <= l2.val:
        l1.next = merge(l1.next, l2)
        return l1
    else:
        l2.next = merge(l1, l2.next)
        return l2

# also try itterable way

def printLL(head):
    temp = head
    while temp:
        print(temp.val)
        temp = temp.next

l1 = Node(1, Node(4, Node(6, None)))
l2 = Node(2, Node(3, Node(5, None)))

printLL(merge(l1, l2))

