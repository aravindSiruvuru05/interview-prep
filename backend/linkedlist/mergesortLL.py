class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_sorted_lists(l1, l2):
    dummy = ListNode()
    tail = dummy

    while l1 and l2:
        if l1.val < l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 or l2  # Append remaining elements
    return dummy.next

def find_middle(head):
    slow, fast = head, head
    prev = None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    if prev:
        prev.next = None  # Split the list into two halves
    return slow

def merge_sort(head):
    if not head or not head.next:
        return head

    mid = find_middle(head)
    left = merge_sort(head)
    right = merge_sort(mid)

    return merge_sorted_lists(left, right)

# Helper function to print the list
def print_list(head):
    while head:
        print(head.val, end=" -> ")
        head = head.next
    print("None")

# Example usage:
head = ListNode(4, ListNode(2, ListNode(1, ListNode(3))))
print("Original List:")
print_list(head)

sorted_head = merge_sort(head)
print("Sorted List:")
print_list(sorted_head)
