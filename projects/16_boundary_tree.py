"""
Boundary travel in a tree
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
		tree = self.create_node(20)
		tree.left = self.create_node(8)
		tree.left.left = self.create_node(4)
		tree.left.right = self.create_node(12)
		tree.left.right.left = self.create_node(10)
		tree.left.right.right = self.create_node(14)
		tree.right = self.create_node(22)
		tree.right.right = self.create_node(25)
		return tree

	def get_tree(self):
		return self.tree

def find_left_nodes(tree):
	if (tree):
		if(tree.left or tree.right):
			print tree.value
			if tree.left:
				find_left_nodes(tree.left)
				return True
			else:
				find_left_nodes(tree.right)
				return True
	return False

def find_right_nodes(tree):
	if (tree):
		if(tree.left or tree.right):
			if tree.right:
				find_right_nodes(tree.right)
				print tree.value
				return True
			else:
				find_right_nodes(tree.left)
				print tree.value
				return True
	return False

def find_leaf_nodes(tree):
	if (tree):
		if not (tree.left or tree.right):
			print tree.value
			return True
		else:
			find_leaf_nodes(tree.left)
			find_leaf_nodes(tree.right)
			return True
	return False

def boundary_traversal():
	bin = BinaryTree()
	tree = bin.get_tree()
	find_left_nodes(tree)
	find_leaf_nodes(tree)
	find_right_nodes(tree)

def main():
	boundary_traversal()

if __name__ == "__main__":
	main()
