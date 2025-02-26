class Node:
    def __init__(self, val, next):
        self.val = val
        self.next = next


def detectCycle(head):
    p1 = head
    p2 = head.next.next

    while p1 and p2:
        if p1.val == p2.val:
            return True
        p1 = p1.next
        p2 = p2.next.next
    return False


n3 = Node(3, None)
n2 = Node(2, n3)
# n1 = Node(1, n2)

# n3.next = n2

print(detectCycle(n2))
        