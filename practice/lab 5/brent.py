# Python program to implement
# Brent's cycle detection algorithm
# to detect cycle in a linked list.

# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Pointer to next node


# Linked List class
class LinkedList:
    def __init__(self):
        self.head = None  # Initialize empty list

    # Insert a new node at the beginning
    def push(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    # Print the linked list
    def printList(self):
        temp = self.head
        while temp:
            print(temp.data, end=" ")
            temp = temp.next
        print()

    # Brent's Cycle Detection
    # Returns (start_node_of_cycle, cycle_length)
    def detectCycle(self):
        temp = self.head
        if not temp:
            return None, 0  # Empty list, no cycle

        # Initialize pointers
        first_p = temp            # Slow pointer
        second_p = temp.next      # Fast pointer
        power = 1                 # Power of 2 for jumps
        length = 1                # Distance from first_p to second_p

        # Phase 1: Detect if a cycle exists
        while second_p and second_p != first_p:
            if length == power:
                print(f"Length/Power = {length}")
                # Move first_p forward to where second_p is
                first_p = second_p
                power *= 2
                length = 0
            second_p = second_p.next
            length += 1

        # If second_p reached None, no cycle
        if not second_p:
            return None, 0

        # Cycle detected; store cycle length
        cycle_length = length

        # Phase 2: Find start of the cycle
        first_p = second_p = self.head
        # Move second_p ahead by cycle length
        for _ in range(cycle_length):
            second_p = second_p.next

        # Move both pointers at same speed until they meet
        while second_p != first_p:
            second_p = second_p.next
            first_p = first_p.next

        # first_p (or second_p) now points to start of cycle
        return first_p, cycle_length


# -------------------------
# Driver code for testing
# -------------------------
llist = LinkedList()
llist.push(50)
llist.push(20)
llist.push(15)
llist.push(4)
llist.push(10)

# Create a loop for testing
# 10 -> 4 -> 15 -> 20 -> 50 -> 15 (cycle starts at 15)
llist.head.next.next.next.next.next = llist.head.next.next

# Detect cycle
start_node, cycle_len = llist.detectCycle()

if start_node:
    print(f"Loop found at node with data {start_node.data} and cycle length {cycle_len}")
else:
    print("No Loop")
