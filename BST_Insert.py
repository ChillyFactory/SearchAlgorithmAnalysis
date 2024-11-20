import time
import random

# Represents a node in the binary search tree (BST)
class Node:
    def __init__(self, key):
        self.left = None  # Left child
        self.right = None  # Right child
        self.key = key  # Node value

# Inserts a value into the BST
def insert(root, key):
    new_node = Node(key)  # Create a new node
    if root is None:  # If tree is empty, return new node as root
        return new_node

    parent = None
    curr = root
    # Traverse to find the correct position
    while curr is not None:
        parent = curr
        if key < curr.key:
            curr = curr.left
        elif key > curr.key:
            curr = curr.right
        else:
            return root  # Value already exists, no insertion needed

    # Attach the new node to the parent
    if key < parent.key:
        parent.left = new_node
    else:
        parent.right = new_node

    return root

# Measures the time to insert values into a BST
def measure_insertion_time(data_size, repetitions):
    total_time = 0
    for _ in range(repetitions):
        root = None  # Start with an empty tree
        data = random.sample(range(1, data_size * 10), data_size)  # Unique random values

        # Measure time for inserting all values
        start_time = time.time()
        for key in data:
            root = insert(root, key)
        end_time = time.time()

        total_time += (end_time - start_time)

    # Return the average time per repetition
    return total_time / repetitions

# Get data sizes and repetitions from the user
data_sizes = input("Enter data sizes separated by spaces (e.g., 100 1000 5000): ").split()
data_sizes = [int(size) for size in data_sizes]  # Convert input to integers
repetitions = int(input("Enter the number of repetitions for averaging: "))

# Measure and print the insertion time for each data size
for size in data_sizes:
    avg_time = measure_insertion_time(size, repetitions)
    print(f"Average time to insert {size} elements ({repetitions} repetitions): {avg_time:.5f} seconds")
