import time
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# Deletes a node with the given key from the BST (iterative method)
def del_iterative(root, key):
    curr = root
    prev = None

    # Find the node to delete and its parent
    while curr is not None and curr.key != key:
        prev = curr
        if curr.key < key:
            curr = curr.right
        else:
            curr = curr.left

    # If the key is not found, return the original tree
    if curr is None:
        return root

    # Case 1: Node has at most one child
    if curr.left is None or curr.right is None:
        new_curr = curr.right if curr.left is None else curr.left

        # Handle the case where the node to delete is the root
        if prev is None:
            return new_curr

        # Update the parent's left or right pointer
        if curr == prev.left:
            prev.left = new_curr
        else:
            prev.right = new_curr

    # Case 2: Node has two children
    else:
        # Find the inorder successor (leftmost node in right subtree)
        p = None
        temp = curr.right
        while temp.left is not None:
            p = temp
            temp = temp.left

        # Update pointers to remove the inorder successor
        if p is not None:
            p.left = temp.right
        else:
            curr.right = temp.right

        # Replace current node's key with the successor's key
        curr.key = temp.key

    return root

# Performs an inorder traversal and prints the tree
def inorder(root):
    if root is not None:
        inorder(root.left)
        print(root.key, end=" ")
        inorder(root.right)

# Inserts a key into the BST
def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root

# Measures the time taken to delete a key from a BST
def measure_deletion_time(data_size, delete_key, repeat=100):
    root = None
    # Generate random values for the BST
    data = random.sample(range(1, data_size * 10), data_size - 1)
    data.append(delete_key)  # Ensure the delete_key is in the BST
    random.shuffle(data)  # Shuffle the data for randomness

    # Build the BST
    for key in data:
        root = insert(root, key)

    # Measure the time for deletion (averaged over repetitions)
    start_time = time.perf_counter()
    for _ in range(repeat):
        _ = del_iterative(root, delete_key)
    end_time = time.perf_counter()

    return (end_time - start_time) / repeat  # Return the average time

# Input parameters
data_sizes = input("Enter data sizes separated by spaces (e.g., 100 1000 5000): ").split()
data_sizes = [int(size) for size in data_sizes]
delete_key = int(input("Enter the key to delete: "))
repeat_count = int(input("Enter the number of repetitions for averaging: "))

# Measure and display the deletion time for each data size
for size in data_sizes:
    elapsed_time = measure_deletion_time(size, delete_key, repeat_count)
    print(f"Time taken to delete key {delete_key} in {size} elements: {elapsed_time:.8f} seconds")
