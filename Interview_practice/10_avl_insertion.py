"""
AVL tree implementation
Insertion
"""
class Node(object):
	def __init__(self, val, height, left=None, right = None):
		self.left = left
		self.value = val
		self.right = right
		self.height = height

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

	@property
	def height(self):
	    return self._height
	@height.setter
	def height(self, value):
	    self._height = value

class AVL(object):
	def compute_height(self, root):
		if not (root.left and root.right):
			return 0
		return 1 + max(compute_height(root.left), compute_height(root.right))

	def rotate_right(self, y_node):
		x_node = y_node.left
		l_node = x_node.right

		x_node.right = y_node
		y_node.left = l_node

		x_node.height = compute_height(x_node)
		y_node.height = compute_height(y_node)
		return x_node

	def rotate_left(self, y_node):
		x_node = y_node.right
		l_node = x_node.left

		x_node.left = y_node
		y_node.right = l_node

		x_node.height = compute_height(x_node)
		y_node.height = compute_height(y_node)
		return x_node

	def get_avl_tree(self, root):
		if not (root.left and root.right):
			return root

		if (root.left.height - root.right.height > 1):
			if(root.left.right.height == 0):
				rotate_right(root)
			else:
				rotate_right(root)
				rotate_left(root)

		if (root.left.height - root.right.height < -1):
			if(root.right.left.height == 0):
				rotate_left(root)
			else:
				rotate_left(root)
				rotate_right(root)
		return root

	def get_balance_factor(self, root):
		if root.left and root.right:
			return root.left.height - root.right.height
		elif root.left:
			return root.left.height
		else:
			return root.right.height

	def insert(self, root, value):
		if not root:
			return Node(value, 0)
		if(root.value < value):
			root.right = self.insert(root.right, value)
		elif(root.value > value):
			root.left = self.insert(root.left, value)
		else:
			raise "Duplicate"

		root.height = self.compute_height(root)
		balance_factor = self.get_balance_factor(root)
		return self.get_avl_tree(root)

	def preorder_traversal(self, root):
		if root:			
			print root.value
			self.preorder_traversal(root.left)
			self.preorder_traversal(root.right)

def main():
	avl = AVL()
	root = avl.insert(None, 100)
	print root.value
	root = avl.insert(root, 50)
	root = avl.insert(root, 25)
	root = avl.insert(root, 10)
	avl.preorder_traversal(root)

if __name__ == "__main__":
	main()
