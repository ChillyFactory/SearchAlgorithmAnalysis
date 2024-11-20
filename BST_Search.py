import time
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


# Search for a key in a Binary Search Tree (BST)
def search(root, key):
    curr = root
    while curr is not None:
        if curr.key == key:  # Key found
            return curr
        elif curr.key < key:  # Go to the right subtree
            curr = curr.right
        else:  # Go to the left subtree
            curr = curr.left
    return None  # Key not found


# Insert a key into the BST
def insert(root, key):
    if root is None:
        return Node(key)  # Create a new node if the tree is empty
    if key < root.key:
        root.left = insert(root.left, key)  # Insert into the left subtree
    else:
        root.right = insert(root.right, key)  # Insert into the right subtree
    return root


# Measure the time it takes to search for a key in the BST
def measure_search_time(data_size, search_key, repeat=100):
    root = None
    # Generate random numbers to fill the BST
    data = random.sample(range(1, data_size * 10), data_size - 1)  # Unique random numbers
    data.append(search_key)  # Ensure the search key is in the tree
    random.shuffle(data)  # Shuffle to randomize the order of insertion

    # Build the BST
    for key in data:
        root = insert(root, key)

    # Measure the average search time over multiple repetitions
    start_time = time.perf_counter()
    for _ in range(repeat):
        found_node = search(root, search_key)
    end_time = time.perf_counter()

    elapsed_time = (end_time - start_time) / repeat
    return elapsed_time, found_node is not None


# Get input values dynamically from the user
data_sizes = input("Enter data sizes separated by spaces (e.g., 100 1000 5000): ").split()
data_sizes = [int(size) for size in data_sizes]
search_key = int(input("Enter the key to search for: "))
repeat_count = int(input("Enter the number of repetitions for averaging: "))

# Measure and display the search time for each data size
for size in data_sizes:
    elapsed_time, found = measure_search_time(size, search_key, repeat_count)
    status = "found" if found else "not found"
    print(f"Time taken to search for key {search_key} in {size} elements: {elapsed_time:.8f} seconds ({status})")
