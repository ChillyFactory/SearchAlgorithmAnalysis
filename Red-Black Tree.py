import time
import random
from collections import deque

# Node class to represent each node in the RBT
class Node:
    def __init__(self, data):
        self.data = data # Node's data
        self.color = 'R'  # By default, new nodes are red
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0) # Sentinel node (representing None)
        self.TNULL.color = 'B'  # Sentinel is always black
        self.root = self.TNULL # Initially, the tree is empty

    def left_rotate(self, x):
        y = x.right # Set y to the right child of x
        x.right = y.left # Make y's left child the new right child of x

        if y.left != self.TNULL:
            y.left.parent = x # Update parent of y's left child
        y.parent = x.parent # Set y's parent to x's parent

        if x.parent is None:
            self.root = y #If x was the root, now y becomes the new root

        elif x == x.parent.left:
            x.parent.left = y #If x was left child, y becomes left child

        else:

            x.parent.right = y # If x was right child, y becomes right child

        y.left = x # Set x as the left child of y
        x.parent = y # Set y as the parent of x

    def right_rotate(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent

        if x.parent is None:
            self.root = y

        elif x == x.parent.right:
            x.parent.right = y

        else:
            x.parent.left = y

        y.right = x # Set x as the right child of y
        x.parent = y # Set y as the parent of x

    # Fixes any violations of the RBT properties after an insert operation
    def fix_insert(self, k):
        while k.parent.color == 'R': # Case where the parent is red (violation)

            if k.parent == k.parent.parent.left: #Parent is left child of grandparent
                u = k.parent.parent.right # uncle node

                if u.color == 'R': # Case 1: uncle is red
                    u.color = 'B'
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent

                else:
                    if k == k.parent.right: # Case 2: k is right child of its parent
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.right_rotate(k.parent.parent) #right rotate to fix imbalance
            else:
                u = k.parent.parent.left # Parent is right child of grandparent

                if u.color == 'R': #Case 1: uncle is red
                    u.color = 'B'
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent
                else:
                    if k == k.parent.left: # Case 2: k is left child of its parent
                        k = k.parent
                        self.right_rotate(k) # right rotate to fix imbalance
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.left_rotate(k.parent.parent)

            if k == self.root: # If root is reached, stop the loop
                break
        self.root.color = 'B'

    # Insert a new node with given key into the RBT
    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'R' #new nodes are red

        y = None
        x = self.root

        # Find the right place to insert the new node
        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # Insert node into the tree
        node.parent = y
        if y is None:
            self.root = node #If the tree is empty, the new node becomes root
        elif node.data < y.data:
            y.left = node # If the node is smaller, it becomes the left child
        else:
            y.right = node # Otherwise, it becomes the right child

        # Fix Red-Black properties if violated after insertion
        if node.parent is None:
            node.color = 'B' # Root node is always black
            return

        if node.parent.parent is None:
            return #No fix needed if the parent has no parent

        self.fix_insert(node)

    def print_tree(self): #Print the tree level by level BFS (Breadth-First Search)
        if self.root == self.TNULL:
            print("Empty Tree")
        else:
            self._print_by_levels(self.root)

    def _print_by_levels(self, root): #Helper function for level-order traversal of the tree (BFS)
        queue = deque([root]) # Use a queue to store nodes for BFS
        level = 0
        while queue:
            level_size = len(queue) #Get the number of nodes at this level
            current_level = [] #List to store nodes at the current level
            for _ in range(level_size):
                node = queue.popleft() # Pop node from the queue
                if node != self.TNULL:
                    current_level.append(f"{node.data}({node.color})") # Append node data with color
                    if node.left != self.TNULL:
                        queue.append(node.left) # Add left child to the queue
                    if node.right != self.TNULL:
                        queue.append(node.right) # Add right child to the queue

            if current_level:
                print(f"Level {level}:")
                for i in range(len(current_level)):
                    node_str = current_level[i]
                    node = self._get_node_by_str(node_str)
                    if node != self.TNULL:
                        # Verify if its right or left child
                        if node.parent != self.TNULL and node.parent is not None:
                            relation = f"Parent -> {node.parent.data}({node.parent.color})"
                            print(f"{node.data}({node.color})  {relation}")
                        else:
                            print(f"{node.data}({node.color}) Root node")
            level += 1

    def _get_node_by_str(self, node_str):
        # Iterate over all nodes in the tree and check if their string representation matches the input string
        for node in self._get_all_nodes(self.root):
            # Compare node's data and color in the format "data(color)" to the given node_str
            if f"{node.data}({node.color})" == node_str:
                return node # If a match is found, return the corresponding node
        return self.TNULL # If no match is found, return the sentinel node

    def _get_all_nodes(self, node):
        # This function returns all the nodes of the tree (using Depth-First Search, DFS)
        nodes = [] # Initialize an empty list to store the nodes
        if node != self.TNULL:
            nodes.append(node)
            if node.left != self.TNULL: # If the left child is not TNULL
                nodes.extend(self._get_all_nodes(node.left))
            if node.right != self.TNULL:  # If the right child is not TNULL
                nodes.extend(self._get_all_nodes(node.right))
        return nodes # Return the list of all nodes in the tree

    def _inorder_helper(self, node):
        if node != self.TNULL: # Ensure the node is not TNULL before proceeding
            self._inorder_helper(node.left) # Recursively traverse the left subtree
            print(f"{node.data}({node.color})", end=" ")
            self._inorder_helper(node.right) # Recursively traverse the right subtree

    # Search for a node with a given key
    def search_tree(self, key):
        return self._search_tree_helper(self.root, key)

    # Helper function for searching the tree
    def _search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node
        if key < node.data:
            return self._search_tree_helper(node.left, key)
        return self._search_tree_helper(node.right, key)

    # Delete a node with the given key from the tree
    def delete_node(self, data):
        node = self.search_tree(data)
        if node != self.TNULL:
            self._delete_node_helper(node)
            print(f"Node {data} deleted successfully.")
        else:
            print(f"Node {data} not found.")

    # Helper function to delete a node
    def _delete_node_helper(self, node):
        # If the node has at least one child, take the successor node (smallest in right subtree)
        if node.left == self.TNULL or node.right == self.TNULL:
            temp = node
        else:
            temp = self._min_value_node(node.right)
            node.data = temp.data  # Copy the value of the successor node
            node = temp  # Now delete the successor node
            if node == self.TNULL:
                return

        # If the node has one non-null child
        if node.left != self.TNULL:
            child = node.left
        else:
            child = node.right

        # Update the parent pointer of the child node
        child.parent = node.parent

        if node.parent is None:
            self.root = child  # If the node is the root, the child becomes the new root
        elif node == node.parent.left:
            node.parent.left = child  # If node is left child, update parent's left pointer
        else:
            node.parent.right = child  # If node is right child, update parent's right pointer

        # If the deleted node was black, fix RBT properties
        if node.color == 'B':
            self._fix_delete(child)

        node = None  # Clear reference to the deleted node

    # Fix the RBT after a node deletion
    def _fix_delete(self,x):
        while x != self.root and x.color == 'B': # Continue fixing as long as x is black and not root

            if x == x.parent.left: # If x is a left child
                w = x.parent.right # Get sibling w
                if w.color == 'R': # Case 1: Sibling is red
                    w.color = 'B' # Recolor sibling to black
                    x.parent.color = 'R' # Recolor parent to red
                    self.left_rotate(x.parent) # Rotate left to fix imbalance
                    w = x.parent.right # Reevaluate the sibling

                if w.left.color == 'B' and w.right.color == 'B': # Case 2: Both children are black
                    w.color = 'R' # Recolor sibling to red
                    x = x.parent # Move up the tree to the parent
                else:
                    if w.right.color == 'B': # Case 3: Right child of sibling is black
                        w.left.color = 'B' # Recolor left child of sibling
                        w.color = 'R' # Recolor sibling to red
                        self.right_rotate(w) # Rotate right to fix imbalance
                        w = x.parent.right # Reevaluate the sibling

                    w.color = x.parent.color # Recolor sibling to march parent's color
                    x.parent.color = 'B' # Recolor parent to black
                    w.right.color = 'B' # Recolor right child of sibling to black
                    self.left_rotate(x.parent) # Rotate left to fix imbalance
                    x = self.root # Tree fixed, Exit loop

            else: # If x is a right child
                w = x.parent.left 
                if w.color == 'R': # Case 1: Sibling is red
                    w.color = 'B'
                    x.parent.color = 'R'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                
                if w.right.color == 'B' and w.left.color == 'B': # Case 2: Both children are black
                    w.color = 'R'
                    x = x.parent
                else:
                    if w.left.color == 'B': # Case 3: Left child of sibling is black
                        w.right.color = 'B'
                        w.color = 'R'
                        self.left_rotate(w)
                        w = x.parent.left # Reevaluate the children 
                    w.color = x.parent.color
                    x.parent.color = 'B'
                    w.left.color = 'B'
                    self.right_rotate(x.parent)
                    x = self.root # Exit loop

        x.color = 'B' # Ensure the node is black when done

    def _min_value_node(self, node):
        current = node
        while current.left != self.TNULL:
            current = current.left
        return current

# Function to generate a random sample and insert into the RBT
def generate_random_sample(size):
    return random.sample(range(1, size * 10), size)

def main_menu():
    print("Welcome to the Red-Black Tree Operations")
    
    data_sizes_input = input("Enter multiple data sizes (separated by space): ")
    data_sizes = list(map(int, data_sizes_input.split()))
    
    trees = {}

    # Generate trees for each size
    for data_size in data_sizes:
        random_data = generate_random_sample(data_size)
        print(f"\nGenerated random sample of size {data_size}: {random_data}")
        rb_tree = RedBlackTree()
        # Insert the random data into the tree
        for value in random_data:
            rb_tree.insert(value)
        trees[data_size] = rb_tree
        print(f"Tree with {data_size} nodes created.")
    
    while True:
        print("\nSelect a tree to operate on:")
        for idx, size in enumerate(data_sizes):
            print(f"{idx+1}. Tree with {size} nodes")
        
        choice = input(f"Enter your choice (1-{len(data_sizes)}): ")
        try:
            selected_tree_size = data_sizes[int(choice)-1]
            selected_tree = trees[selected_tree_size]
            break
        except (IndexError, ValueError):
            print("Invalid choice. Please select a valid tree.")
    
    while True:
        print("\nRed-Black Tree Operations Menu")
        print("1. Insert a new node")
        print("2. Search for a node")
        print("3. Delete a node")
        print("4. Display Tree")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            value = int(input("Enter value to insert: "))
            start_time = time.time()
            selected_tree.insert(value)
            end_time = time.time()
            insertion_time = (end_time - start_time) * 1000 #time in ms
            print(f"Node {value} inserted in {insertion_time:.8f} miliseconds.")
        
        elif choice == '2':
            value = int(input("Enter value to search: "))
            start_time = time.time()
            result = selected_tree.search_tree(value)
            end_time = time.time()
            search_time = (end_time - start_time)
            if result != selected_tree.TNULL:
                print(f"Node {value} found in {search_time:.6f} miliseconds.")
            else:
                print(f"Node {value} not found.")
        
        elif choice == '3':
            value = int(input("Enter value to delete: "))
            start_time = time.time()
            selected_tree.delete_node(value)
            end_time = time.time()
            deletion_time = (end_time - start_time) * 1000
            print(f"Node {value} deleted in {deletion_time:.6f} miliseconds.")
        
        elif choice == '4':
            start_time = time.perf_counter()
            selected_tree.print_tree()
            end_time = time.perf_counter()
            print(f"Time taken to print the tree: {end_time - start_time:.6f} seconds.")
        
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
