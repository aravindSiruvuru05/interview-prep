class Node:
    def __init__(self, value):
        self.data = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def  insertAtHead(self, value):
        newNode = Node(value)
        if self.head == None:
            self.head = newNode
        else:   
            currHead = self.head
            self.head = newNode
            newNode.next = currHead

    def insertAtTail(self, value):
        newNode = Node(value)
        if not self.head:
            self.head = newNode
            return
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = newNode

    def printLL(self):
        temp = self.head
        while temp:
            print(temp.data)
            temp = temp.next
    
    def insertAtPosition(self, pos, value):
        if pos <= 0:
            print('Invalid pos')
            return  
        if pos == 1:
            self.insertAtHead(value)
            return
        newNode = Node(value)
        temp = self.head
        for _ in range(pos - 2):
            if not temp:
                print("position out of bounds")
                return
            temp = temp.next
        newNode.next = temp.next
        temp.next = newNode

    def deleteHead(self):
        if not self.head:
            print("no head")
            return
        self.head = self.head.next
    
    def deleteTail(self):
        if not self.head:
            print("cant delete in empty ll")
            return    
        if not self.head.next:
            self.head = None
            return

        temp = self.head
        while temp.next and temp.next.next:
            temp = temp.next
        temp.next = None

    def deleteAtPos(self, pos):
        if pos <= 0:
            print("Invalid Position")
            return
        if pos == 1:
            self.head = self.head.next
        temp = self.head
        for _ in range(pos - 2):
            if not temp.next:
                print("Pos out of bounds")
                return
            temp = temp.next
            pos -= 1
        if temp.next:
            temp.next = temp.next.next

        
        



ll = LinkedList()
ll.insertAtHead(1)
ll.insertAtHead(2)
ll.insertAtTail(3)
ll.insertAtHead(4)
ll.insertAtPosition(1, 10)
ll.insertAtTail(3)
ll.insertAtHead(5)
ll.insertAtPosition(3, 13)
ll.deleteAtPos(3)
# ll.deleteTail()
# ll.deleteTail()
# ll.deleteTail()
# ll.deleteTail()
# ll.deleteTail()
# ll.deleteTail()
ll.deleteTail()
ll.printLL()
 

# 5 10 13 4 2 1 3 3  