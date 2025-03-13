# Node234 class - represents a node in a 2-3-4 tree
class Node234:
    def __init__(self, keyA, left_child=None, middle1_child=None):
        self.A = keyA
        self.B = 0
        self.C = 0
        self.key_count = 1
        self.left = left_child
        self.middle1 = middle1_child
        self.middle2 = None
        self.right = None
    
    # Appends 1 key and 1 child to this node.
    # Preconditions:
    # 1. This node has 1 or 2 keys
    # 2. key > all keys in this node
    # 3. Child subtree contains only keys > key
    def append_key_and_child(self, key, child):
        if self.key_count == 1:
            self.B = key
            self.middle2 = child
        else:
            self.C = key
            self.right = child
        self.key_count += 1
    
    # Returns the left, middle1, middle2, or right child if the child_index
    # argument is 0, 1, 2, or 3, respectively.
    # Returns None if the child_index argument is < 0 or > 3.
    def get_child(self, child_index):
        if child_index == 0:
            return self.left
        elif child_index == 1:
            return self.middle1
        elif child_index == 2:
            return self.middle2
        elif child_index == 3:
            return self.right
        return None

    # Returns 0, 1, 2, or 3 if the child argument is this node's left,
    # middle1, middle2, or right child, respectively.
    # Returns -1 if the child argument is not a child of this node.
    def get_child_index(self, child):
        if child == self.left:
            return 0
        elif child == self.middle1:
            return 1
        elif child == self.middle2:
            return 2
        elif child == self.right:
            return 3
        return -1

    # Returns this node's A, B, or C key, if the key_index argument is
    # 0, 1, or 2, respectively.
    # Returns 0 if the key_index argument is < 0 or > 2.
    def get_key(self, key_index):
        if key_index == 0:
            return self.A
        elif key_index == 1:
            return self.B
        elif key_index == 2:
            return self.C
        return 0
   
    # Returns this node's key count.
    def get_key_count(self):
        return self.key_count

    # Returns 0, 1, or 2, if the key argument is this node's A, B, or
    # C key, respectively.
    # Returns -1 if the key is not in this node.
    def get_key_index(self, key):
        if key == self.A:
            return 0;
        elif self.key_count > 1 and key == self.B:
            return 1
        elif self.key_count > 2 and key == self.C:
            return 2
        return -1
   
    # Returns true if this node has the specified key, false otherwise.
    def has_key(self, key):
        if key == self.A or (self.key_count > 1 and key == self.B):
            return True
        return self.key_count > 2 and key == self.C

    # Inserts a new key into the proper location in this node.
    # Precondition: This node is a leaf and has 2 or fewer keys
    def insert_key(self, key):
        if key < self.A:
            self.C = self.B
            self.B = self.A
            self.A = key
        elif self.key_count == 1 or key < self.B:
            self.C = self.B
            self.B = key
        else:
            self.C = key
        self.key_count += 1
   
    # Inserts a new key into the proper location in this node, and
    # sets the children on either side of the inserted key.
    # Precondition: This node has 2 or fewer keys
    def insert_key_with_children(self, key, left_child, right_child):
        if key < self.A:
            self.C = self.B
            self.B = self.A
            self.A = key
            self.right = self.middle2
            self.middle2 = self.middle1
            self.middle1 = right_child
            self.left = left_child
        elif self.key_count == 1 or key < self.B:
            self.C = self.B
            self.B = key
            self.right = self.middle2
            self.middle2 = right_child
            self.middle1 = left_child
        else:
            self.C = key
            self.right = right_child
            self.middle2 = left_child
        self.key_count += 1

    # Returns true if this node is a leaf, false otherwise.
    def is_leaf(self):
        return self.left == None

    # Returns the child of this node that would be visited next in the
    # traversal to search for the specified key.
    def next_node(self, key):
        if key < self.A:
            return self.left
        elif self.key_count == 1 or key < self.B:
            return self.middle1
        elif self.key_count == 2 or key < self.C:
            return self.middle2
        return self.right

    # Removes key A, B, or C from this node, if key_index is 0, 1, or 2,
    # respectively. Other keys and children are shifted as necessary.
    def remove_key(self, key_index):
        if key_index == 0:
            self.A = self.B
            self.B = self.C
            self.left = self.middle1
            self.middle1 = self.middle2
            self.middle2 = self.right
            self.right = None
            self.key_count -= 1
        elif key_index == 1:
            self.B = self.C
            self.middle2 = self.right
            self.right = None
            self.key_count -= 1
        elif key_index == 2:
            self.right = None
            self.key_count -= 1

    # Removes and returns the rightmost child. Several cases exist:
    # 1. If this node's right child is not None, then right is assigned with
    #    None and the previous right child is returned.
    # 2. Otherwise, if this node's middle2 child is not None, then middle2 is
    #    assigned with None and the previous middle2 child is returned.
    # 3. Otherwise no action is taken, and None is returned.
    # No keys are changed in any case, nor the key_count.
    def remove_rightmost_child(self):
        removed_node = None
        if self.right != None:
            removed_node = self.right
            self.right = None
        elif self.middle2 != None:
            removed_node = self.middle2
            self.moddle2 = None
        return removed_node

    # Removes and returns the rightmost key. Three possible cases exist:
    # 1. If this node has 3 keys, key_count is decremented C is returned.
    # 2. If this node has 2 keys, key_count is decremented B is returned.
    # 3. Otherwise no action is taken and 0 is returned.
    # No children are changed in any case.
    def remove_rightmost_key(self):
        removed_key = 0
        if self.key_count == 3:
            removed_key = self.C
            self.key_count -= 1
        elif self.key_count == 2:
            removed_key = self.B
            self.key_count -= 1
        return removed_key

    # Sets the left, middle1, middle2, or right child if the child_index
    # argument is 0, 1, 2, or 3, respectively.
    # Does nothing if the child_index argument is < 0 or > 3.
    def set_child(self, child, child_index):
        if child_index == 0:
            self.left = child
        elif child_index == 1:
            self.middle1 = child
        elif child_index == 2:
            self.middle2 = child
        elif child_index == 3:
            self.right = child
   
    # Sets all four of this node's child references.
    def set_children(self, left, middle1, middle2, right):
        self.left = left
        self.middle1 = middle1
        self.middle2 = middle2
        self.right = right

    # Sets this node's A, B, or C key if the key_index argument is 0, 1, or
    # 2, respectively.
    # Does nothing if the key_index argument is < 0 or > 2.
    def set_key(self, key, key_index):
        if key_index == 0:
            self.A = key
        elif key_index == 1:
            self.B = key
        elif key_index == 2:
            self.C = key
   
    # Sets this node's key_count variable to new_key_count, provided new_key_count
    # is in the range [1,3]. On sucess, True is returned. On failure, no change
    # occurs and False is returned.
    def set_key_count(self, new_key_count):
        if new_key_count <= 0 or new_key_count > 3:
            return False
        
        self.key_count = new_key_count
        return True