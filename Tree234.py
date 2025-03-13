from Node234 import Node234
from Tree234Iterator import Tree234Iterator

class Tree234:
    # Initializes the tree by assigning the root node reference with None.
    def __init__(self):
        self.root = None
    
    def alloc_node(self, key, left_child = None, middle1_child = None):
        return Node234(key, left_child, middle1_child)
    
    # Recursive helper function for search.
    def search_recursive(self, key, node):
        if node == None:
            return None
        #
        # Check if the node contains the key
        if  node.has_key(key):
            return node
        #
        # Recursively search the appropriate subtree
        return self.search_recursive(key, node.next_node(key))
    
    # Splits a full node, moving the middle key up into the parent node.
    # Returns the parent of the split node.
    # Precondition: nodeParent has one or two keys.
    def split(self, node, node_parent):
        key0 = node.get_key(0)
        key1 = node.get_key(1)
        key2 = node.get_key(2)
        child0 = node.get_child(0)
        child1 = node.get_child(1)
        child2 = node.get_child(2)
        child3 = node.get_child(3)
        split_left = self.alloc_node(key0, child0, child1)
        split_right = self.alloc_node(key2, child2, child3)
        if node_parent != None:
            node_parent.insert_key_with_children(key1, split_left, split_right)
        else:
            # Split root
            node_parent = self.alloc_node(key1, split_left, split_right)
            self.root = node_parent
        return node_parent
    
    # Fuses a parent node and two children into one node.
    # Precondition: left_node and right_node must have one key each.
    def fuse(self, parent, left_node, right_node):
        if parent is self.root and parent.get_key_count == 1:
            return self.fuse_root()
        left_node_index = parent.get_child_index(left_node)
        middle_key = parent.get_key(left_node_index)
        fused_node = self.alloc_node(left_node.get_key(0))
        fused_node.set_key(middle_key, 1)
        fused_node.set_key(right_node.get_key(0), 2)
        fused_node.set_key_count(3)
        fused_node.set_children(left_node.get_child(0), left_node.get_child(1),
            right_node.get_child(0), right_node.get_child(1))
        key_index = parent.get_key_index(middle_key)
        parent.remove_key(key_index)
        parent.set_child(fused_node, key_index)
        return fused_node
    
    # Fuses the tree's root node with the root's two children.
    # Precondition: Each of the three nodes must have one key each.
    def fuse_root(self):
        old_left = self.root.get_child(0)
        old_middle1 = self.root.get_child(1)
        self.root.set_key(self.root.get_key(0), 1)
        self.root.set_key(old_left.get_key(0), 0)
        self.set_key(old_middle1.get_key(0), 2)
        self.set_key_count(3)
        self.root.set_children(old_left.get_child(0), old_left.get_child(1),
            old_middle1.get_child(0), old_middle1.get_child(1))
        return self.root
    
    # Searches for, and returns, the minimum key in a subtree
    def get_min_key(self, node):
        current = node
        while current.get_child(0) != None:
            current = current.get_child(0)
        return current.get_key(0)
    
    # Finds and replaces one key with another. The replacement key must
    # be known to be a key that can be used as a replacement without violating
    # any of the 2-3-4 tree rules.
    def key_swap(self, node, existing_key, replacement):
        if node == None:
            return False
        key_index = node.get_key_index(existing_key)
        if key_index == -1:
            next = node.next_node(existing_key)
            return self.key_swap(next, existing_key, replacement)
        node.set_key(replacement, key_index)
        return True
    
    # Rotates or fuses to add 1 or 2 additional keys to a node with 1 key.
    def merge(self, node, node_parent):
        # Get references to node's siblings
        node_index = node_parent.get_child_index(node)
        left_sibling = node_parent.get_child(node_index - 1)
        right_sibling = node_parent.get_child(node_index + 1)
        #
        # Check siblings for a key that can be transferred
        if left_sibling != None and left_sibling.get_key_count() >= 2:
            self.rotate_right(left_sibling, node_parent)
        elif right_sibling and right_sibling.get_key_count() >= 2:
            self.rotate_left(right_sibling, node_parent)
        else: # fuse
            if left_sibling == None:
                node = self.fuse(node_parent, node, right_sibling)
            else:
                node = self.fuse(node_parent, left_sibling, node)
        return node
    
    def rotate_left(self, node, node_parent):
        # Get the node's left sibling
        node_index = node_parent.get_child_index(node)
        left_sibling = node_parent.get_child(node_index - 1)
        #
        # Get the key from the parent that will be copied into the left sibling
        key_for_sibling = node_parent.get_key(node_index - 1)
        #
        # Append the key to the left sibling
        left_sibling.append_key_and_child(key_for_sibling, node.get_child(0))
        #
        # Replace the parent's key that was appended to the left sibling
        node_parent.set_key(node.get_key(0), node_index - 1)
        #
        # Remove key A and left child from node
        node.remove_key(0)
    
    def rotate_right(self, node, node_parent):
        # Get the node's right sibling
        node_index = node_parent.get_child_index(node)
        right_sibling = node_parent.get_child(node_index + 1)
        #
        # Get the key from the parent that will be copied into the right sibling
        key_for_right_sibling = node_parent.get_key(node_index)
        #
        # Shift key and child references in right sibling
        right_sibling.set_key(right_sibling.get_key(1), 2)
        right_sibling.set_key(right_sibling.get_key(0), 1)
        right_sibling.set_child(right_sibling.get_child(2), 3)
        right_sibling.set_child(right_sibling.get_child(1), 2)
        right_sibling.set_child(right_sibling.get_child(0), 1)
        #
        # Set key A and the left child of right_sibling
        right_sibling.set_key(key_for_right_sibling, 0)
        right_sibling.set_key(node.remove_rightmost_child(), 0)
        #
        # right_sibling has gained a key
        right_sibling.set_key_count(right_sibling.get_key_count() + 1)
        #
        # Replace the parent's key that was prepended to the right sibling
        node_parent.set_key(node.remove_rightmost_key(), node_index)
    
    
    # Inserts a new key into this tree, provided the tree doesn't already
    # contain the same key.
    def insert(self, key, node = None, node_parent = None):
        # Special case for empty tree
        if self.root == None:
            self.root = self.alloc_node(key)
            return self.root
        #
        # If the node argument is None, recursively call with root
        if node == None:
            return self.insert(key, self.root, None)
        #
        # Check for duplicate key
        if node.has_key(key):
            # Duplicate keys are not allowed
            return None
        #
        # Preemptively split full nodes
        if node.get_key_count() == 3:
            node = self.split(node, node_parent)
        #
        # If node is not a leaf, recursively insert into child subtree
        if not node.is_leaf():
            return self.insert(key, node.next_node(key), node)
        #
        # key can be inserted into leaf node
        node.insert_key(key)
        return node
    
    # Searches this tree for the specified key. If found, the node containing
    # the key is returned. Otherwise None is returned.
    def search(self, key):
        return self.search_recursive(key, self.root)
    
    # Returns the number of keys in this tree.
    def __len__(self):
        count = 0
        nodes = [self.root]
        while len(nodes) > 0:
            node = nodes.pop()
            if node != None:
                # Add the number of keys in the node to the count
                count = count + node.get_key_count()
                #
                # Push children
                for i in range(4):
                    nodes.append(node.get_child(i))
        return count
    
    # Finds and removes the specified key from this tree.
    def remove(self, key):
        # Special case for tree with 1 key
        if self.root.is_leaf() and self.root.get_key_count() == 1:
            if self.root.get_key(0) == key:
                self.root = None
                return True
            return False
        
        current_parent = None
        current = self.root
        while current != None:
            # Merge any non-root node with 1 key
            if current.get_key_count() == 1 and current is not self.root:
                current = self.merge(current, current_parent)
            #
            # Check if current node contains key
            key_index = current.get_key_index(key)
            if key_index != -1:
                if current.is_leaf():
                    current.remove_key(key_index)
                    return True
                #
                # The node contains the key and is not a leaf, so the key is
                # replaced with the successor
                tmp_child = current.get_child(key_index + 1)
                tmp_key = self.get_min_key(tmp_child)
                self.remove(tmp_key)
                self.key_swap(self.root, key, tmp_key)
                return True
            #
            # Current node does not contain key, so continue down tree
            current_parent = current
            current = current.next_node(key)
        # key not found
        return False
    
    # Added to support iteration through the trees keys with a for-in loop
    def __iter__(self):
        return Tree234Iterator(self.root)