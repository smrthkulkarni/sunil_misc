"""
Convert to a tree where sum of child equal to parent node.
Only increase the node value
"""
class Node(object):
    def __init__(self, left, val, right):
        self.left = left
        self.value = val
        self.right = right      

    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, value):
        self._left = value

    @property
    def val(self):
        return self._val
    @val.setter
    def val(self, value):
        self._val = value

    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, value):
        self._right = value

class BinaryTree(object):
    def __init__(self):
        self.tree = self.manual_tree_creation()

    def create_node(self, val):
        return Node(None, val, None)

    def manual_tree_creation(self):
        tree = self.create_node(50)
        tree.left = self.create_node(7)
        tree.right = self.create_node(2)
        tree.left.left = self.create_node(3)
        tree.left.right = self.create_node(5)
        tree.right.left = self.create_node(1)
        tree.right.right = self.create_node(30)
        return tree

    def get_tree(self):
        return self.tree

def get_right_most_leaf(root):
    if root:
        if root.right:
            return get_right_most_leaf(root.right)
        elif root.left:
            return get_right_most_leaf(root.left)
        else:
            return root
    return

def increment(root, diff):
    if root.left:
        root.left.value = root.left.value + diff
        increment(root.left, diff)
    elif root.right:
        root.right.value = root.right.value + diff
        increment(root.right, diff)

def parent_to_child_sum(root):
    left_data = 0
    right_data = 0
    if not root or not (root.left and root.right):
        return
    else:
        parent_to_child_sum(root.left)
        parent_to_child_sum(root.right)

        if root.left:
            left_data = root.left.value
        if root.right:
            right_data = root.right.value

        diff = (left_data + right_data) - root.value
        if diff > 0:
            root.value = root.value + diff

        if diff < 0:
            increment(root, -diff)
   
def in_order_traversal(root):
    if root:
        in_order_traversal(root.left)
        print root.value, 
        in_order_traversal(root.right)
    
def main():
    bt = BinaryTree()
    tree = bt.get_tree()
    parent_to_child_sum(tree)
    in_order_traversal(tree)

if __name__ == "__main__":
    main()

