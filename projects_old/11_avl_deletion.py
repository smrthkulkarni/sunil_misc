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
		return 1 + max(self.compute_height(root.left), self.compute_height(root.right))

	def rotate_right(self, y_node):
		x_node = y_node.left
		l_node = x_node.right

		x_node.right = y_node
		y_node.left = l_node

		x_node.height = self.compute_height(x_node)
		y_node.height = self.compute_height(y_node)
		return x_node

	def rotate_left(self, y_node):
		x_node = y_node.right
		l_node = x_node.left

		x_node.left = y_node
		y_node.right = l_node

		x_node.height = self.compute_height(x_node)
		y_node.height = self.compute_height(y_node)
		return x_node

	def get_avl_tree(self, root):
		print root.value
		if not (root.left) and not(root.right):
			return root

		if (root.left.height - root.right.height > 1):
			if(root.left.right.height == 0):
				self.rotate_right(root)
			else:
				self.rotate_right(root)
				self.rotate_left(root)

		if (root.left.height - root.right.height < -1):
			if(root.right.left.height == 0):
				self.rotate_left(root)
			else:
				self.rotate_left(root)
				self.rotate_right(root)
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

	def search(self, root, value):
		if not root:
			return 
		else:
			if root.value == value:
				return root
			elif root.value > value:
				return self.search(root.left, value)
			else:
				return self.search(root.right, value)

	def find_parent_node(self, root, value, prev):
		if root.value == value:
			return root, prev
		elif root.value > value:
			prev = root
			return self.find_parent_node(root.left, value, prev)
		else:
			prev = root
			return self.find_parent_node(root.right, value, prev)

	def find_predecessor_inorder(self, root):
		if not (root.left) and not(root.right):
			return root
		if root.right:
			return self.find_predecessor_inorder(root.right)
		else:
			return self.find_predecessor_inorder(root.left)

	def delete(self, root, value):
		root_value = self.search(root, value)
		print "search value"
		print root_value.value
		if not (root_value.left) and not (root_value.right):
			print "both null"
			(new_root, prev) = self.find_parent_node(root, value, root)
			if prev.value > value:
				prev.left = None
			else:
				prev.right = None
			return root

		if not (root_value.left) or not(root_value.right):
			print "left or right null"
			(new_root, prev) = self.find_parent_node(root, value, root)
			print "find parent result"
			print root.value, new_root.value, prev.value
			if prev.value > value:
				if not root_value.left:
					prev.left = root_value.right
				else:
					prev.left = root_value.left
			else:
				if not root_value.left:
					prev.right = root_value.right
				else:
					prev.right = root_value.left
			return root
		else:
			predecessor_node = self.find_predecessor_inorder(root_value.left)
			print "predecessor_node.value"
			print predecessor_node.value
			(cur, prev) = self.find_parent_node(root, value, root)
			print "new_root.value"
			print cur.value

			if prev.value > value:
				prev.left = predecessor_node
			else:
				prev.right = predecessor_node

			tmp_node = predecessor_node
			if predecessor_node.left != cur.left:
				predecessor_node.left = cur.left
			else:
				predecessor_node.left = None
			predecessor_node.right = cur.right
			cur = None			
			return root

def main():
	avl = AVL()
	root = avl.insert(None, 8)
	root = avl.insert(root, 100)
	root = avl.insert(root, 3)
	root = avl.insert(root, 1)
	root = avl.insert(root, 6)
	root = avl.insert(root, 4)
	root = avl.insert(root, 7)
	root = avl.insert(root, 14)
	root = avl.insert(root, 13)
	avl.preorder_traversal(root)

	print "Deleting values"
	root = avl.delete(root,6)
	print root.value
	print "Traversal"
	avl.preorder_traversal(root)
	

if __name__ == "__main__":
	main()
