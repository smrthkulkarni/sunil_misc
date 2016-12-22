"""
Program to check if the given tree is a bst or not
BST - Binary search tree
 a. left node < root node
 b. right node > root node
 c. tree must be binary tree   
    4  
   / \
  2   5
 /\
1  3
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

def create_node(val):
	return Node(None, val, None)

def manual_tree_creation():
	tree = create_node(4)
	tree.left = create_node(2)
	tree.left.left = create_node(1)
	tree.left.right = create_node(3)
	tree.right = create_node(5)
	return tree

def is_bst(tree, min, max):
	if not tree:
		return 1
	if tree.value < min or tree.value > max:
		return 0
	return is_bst(tree.left, min, tree.value - 1) and is_bst(tree.right, tree.value + 1, max)

def main():
	tree = manual_tree_creation()
	is_tree = is_bst(tree, -1000000, 1000000)
	if is_tree == 0:
		print "Not a bst"
	else:
		print "Valid bst"

if __name__ == "__main__":
	main()