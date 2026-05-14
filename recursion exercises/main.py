class Node:
    def __init__(self, value):
        self._value = value
        self._next = None

    @property
    def value(self):
        """Getter for value"""
        return self._value
    
    @value.setter
    def value(self, value):
        """Setter for value"""
        self._value = value

    @property
    def next(self):
        """Getter for next"""
        return self._next
    
    @next.setter
    def next(self, next_node):
        """Setter for next"""
        self._next = next_node

class LinkedList:
    def __init__(self):
        self.head = None  # The first node in the list

    def append(self, value):
        """Add a new node to the end of the list."""
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:  # Traverse to the end of the list
                current = current.next
            current.next = new_node

    def display(self):
        """Display the values in the linked list."""
        current = self.head
        while current:
            print(current.value, end=" -> ")
            current = current.next
        print("None")

