"""
sum of child equal to parent node
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
		tree = self.create_node(26)
		tree.left = self.create_node(10)
		tree.left.left = self.create_node(3)
		tree.left.right = self.create_node(4)
		tree.left.right.left = self.create_node(6)
		tree.left.right.right = self.create_node(3)
		return tree

	def get_tree(self):
		return self.tree

def parent_to_child_sum(root):
	if not (root.left and root.right):
		return root.value
	left_node_val = parent_to_child_sum(root.left)
	right_node_val = parent_to_child_sum(root.right)
	if left_node_val and right_node_val:
		if root.value == (left_node_val + right_node_val):
			return root.value
	return False
	
def main():
	bt = BinaryTree()
	tree = bt.get_tree()
	if parent_to_child_sum(tree):
		print "The root is equal to sum of children"
	else:
		print "Root unequal to sum of children"

if __name__ == "__main__":
	main()

