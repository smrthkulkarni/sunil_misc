"""
Connect same level
"""

class Node(object):
	def __init__(self, val, left=None, right = None,
				 height = None, level_linking = None):
		self.left = left
		self.value = val
		self.right = right
		self.level_linking = level_linking

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

class Tree(object):
	def __init__(self):
		self._head = None

	@property
	def head(self):
	    return self._head

	def manual_tree_creation(self):
		self._head = Node(100)
		
		self.head.left = Node(50)
		self.head.right = Node(150)
		self.head.left.left = Node(25)
		self.head.left.right = Node(75)
		self.head.right.right = Node(175)
		return self.head

class LevelLinking(object):
	def __init__(self):
		self.tree = self.get_tree()
		self.level_linking = []
		self.queue = [self.tree]		
		self.traveresd_nodes = dict()

	def get_tree(self):
		tree = Tree()
		return tree.manual_tree_creation()

	def connect_level(self, root):
		if not root:
			return False
		else:
			if root.left:
				if root.right:
					root.left.level_linking = root.right
				else:
					root.left.level_linking = self.get_adjacent_trees_child(root)
			if root.right:
				root.right.level_linking = self.get_adjacent_trees_child(root)
		self.connect_level(root.left)
		self.connect_level(root.right)


	def get_adjacent_trees_child(self, root):
		if root.level_linking:
			if root.level_linking.left:
				return root.level_linking.left
			elif root.level_linking.right:
				return root.level_linking.right
			else:
				return None
		else:
			return None

	def print_same_level_root(self):
		print "Print same level"
		print self.tree.value
		print self.tree.level_linking
		print self.tree.left.value
		print self.tree.left.level_linking.value
		print self.tree.left.left.value
		print self.tree.left.left.level_linking.value
		print self.tree.left.left.level_linking.level_linking.value
		

def main():
	level_linking = LevelLinking()
	level_linking.connect_level(level_linking.tree)
	level_linking.print_same_level_root()

if __name__ == "__main__":
	main()
