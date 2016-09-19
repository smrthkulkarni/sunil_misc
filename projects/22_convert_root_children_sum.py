"""
Convert to a tree where sum of child equal to parent node.
Make the leaf zero
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
        tree = self.create_node(10)
        tree.left = self.create_node(-2)
        tree.right = self.create_node(6)
        tree.left.left = self.create_node(8)
        tree.left.right = self.create_node(-4)
        tree.right.left = self.create_node(7)
        tree.right.right = self.create_node(5)
        return tree

    def get_tree(self):
        return self.tree

def parent_to_child_sum(root):
    if not root:
        return 0;
    old_val = root.value
    root.value = parent_to_child_sum(root.left) + parent_to_child_sum(root.right)
    return root.value + old_val;
    
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

