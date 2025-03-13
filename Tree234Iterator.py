from Node234 import Node234

"""class Tree234Iterator:
    def __init__(self, root):
        # Your code here (remove placeholder line below)
        pass
    
    # Returns the tree's next key, or raises StopIteration if no more keys exist
    def __next__(self):
        # Your code here (remove placeholder line below)
        raise StopIteration"""
class Tree234Iterator:
    def __init__(self, root):
        # Initialize the iterator with the root of the tree
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        # Push all left children of the node onto the stack
        while node:
            self.stack.append(node)
            node = node.left

    def __iter__(self):
        # Return the iterator object
        return self

    def __next__(self):
        # Return the next smallest element in the tree
        if not self.stack:
            raise StopIteration

        # Pop the smallest element from the stack
        node = self.stack.pop()
        result = node.key

        # If the node has a right child, push all its left children onto the stack
        if node.right:
            self._push_left(node.right)

        return result   