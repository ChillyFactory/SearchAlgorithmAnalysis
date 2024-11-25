import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys
import psutil, os

sys.setrecursionlimit(10**8)  # Increase the recursion limit

# Common target for testing
TARGET = 5000

def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def search(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self.search(root.left, key)
        return self.search(root.right, key)

class RBNode:
    RED = True
    BLACK = False

    def __init__(self, key, color=RED, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left or None
        self.right = right or None
        self.parent = parent

class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(key=None, color=RBNode.BLACK)  # Sentinel node for leaves
        self.root = self.NIL

    def search(self, key):
        return self._search_tree(self.root, key)

    def _search_tree(self, node, key):
        if node == self.NIL or key == node.key:
            return node
        if key < node.key:
            return self._search_tree(node.left, key)
        return self._search_tree(node.right, key)

    def insert(self, key):
        new_node = RBNode(key, color=RBNode.RED, left=self.NIL, right=self.NIL)
        self._insert_node(new_node)
        self._fix_insert(new_node)

    def _insert_node(self, new_node):
        parent = None
        current = self.root
        while current != self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right
        new_node.parent = parent
        if not parent:  # Tree was empty
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.color = RBNode.RED

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == RBNode.RED:
            if node.parent == node.parent.parent.left:  # Parent is a left child
                uncle = node.parent.parent.right
                if uncle.color == RBNode.RED:  # Case 1: Uncle is red
                    node.parent.color = RBNode.BLACK
                    uncle.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:  # Case 2: Node is right child
                        node = node.parent
                        self._left_rotate(node)
                    # Case 3: Node is left child
                    node.parent.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    self._right_rotate(node.parent.parent)
            else:  # Parent is a right child
                uncle = node.parent.parent.left
                if uncle.color == RBNode.RED:  # Case 1: Uncle is red
                    node.parent.color = RBNode.BLACK
                    uncle.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:  # Case 2: Node is left child
                        node = node.parent
                        self._right_rotate(node)
                    # Case 3: Node is right child
                    node.parent.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    self._left_rotate(node.parent.parent)
        self.root.color = RBNode.BLACK

    def _left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.NIL:
            right_child.left.parent = node
        right_child.parent = node.parent
        if not node.parent:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def _right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.NIL:
            left_child.right.parent = node
        left_child.parent = node.parent
        if not node.parent:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

def generate_data(size):
    data = random.sample(range(size * 10), size)
    return data

def print_memory_usage():
    process = psutil.Process(os.getpid())
    return f"Memory usage: {process.memory_info().rss / 1024**2:.2f} MB"

def benchmark_search_methods():
    data_sizes = [100, 10**3, 10**4, 10**5]
    results = []

    for size in data_sizes:
        data = generate_data(size)
        sorted_data = sorted(data)

        # Linear Search
        start = time.perf_counter()
        linear_search(data, TARGET)
        linear_time = (time.perf_counter() - start) * 1e3
        print(f"Data size: {len(data)} | Linear Search Complete | {print_memory_usage()}")

        # Binary Search
        start = time.perf_counter()
        binary_search(sorted_data, TARGET)
        binary_time = (time.perf_counter() - start) * 1e3
        print(f"Data size: {len(data)} | Binary Search Complete | {print_memory_usage()}")

        # Binary Search Tree
        bst = BinarySearchTree()
        root = None
        for num in sorted_data:
            root = bst.insert(root, num)
        start = time.perf_counter()
        bst.search(root, TARGET)
        bst_time = (time.perf_counter() - start) * 1e3
        print(f"Data size: {len(data)} | Binary Search Tree Complete | {print_memory_usage()}")

        # Red-Black Tree
        rbt = RedBlackTree()
        for num in sorted_data:
            rbt.insert(num)
        start = time.perf_counter()
        try:
            rbt.search(TARGET)
        except KeyError:
            pass
        rbt_time = (time.perf_counter() - start) * 1e3
        print(f"Data size: {len(data)} | RB Tree Complete | {print_memory_usage()}")

        # Store results
        results.append((size, linear_time, binary_time, bst_time, rbt_time))

    return results

def display_results():
    results = benchmark_search_methods()
    df = pd.DataFrame(results, columns=["Data Size", "Linear Search", "Binary Search", "BST Search", "RBT Search"])
    print(df)

    plt.figure(figsize=(10, 6))
    for col in ['Linear Search', 'Binary Search', 'BST Search', 'RBT Search']:
        plt.plot(df['Data Size'], df[col], marker='o', label=col)

    plt.xlabel('Data Size')
    plt.ylabel('Time (ms)')
    plt.title('Search Algorithm Performance by Data Size')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log') 
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    display_results()

