"""
Connect same level
"""

class Node(object):
	def __init__(self, val, left=None, right = None,
				 height = None, level_linking = None):
		self.left = left
		self.value = val
		self.right = right
		self.height = height
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

class BFS(object):
	def __init__(self):
		self.tree = self.get_tree()
		self.bfs = []
		self.queue = [self.tree]		
		self.traveresd_nodes = dict()

	def get_tree(self):
		tree = Tree()
		return tree.manual_tree_creation()

	def bfs_traversal(self, node):
		if not self.queue:
			return False
		else:
			if node not in self.traveresd_nodes:
				self.traveresd_nodes[node] = 1
				node.height = self.find_height_of_tree(node)
				self.bfs.append(node)
				if node.left:
					self.queue.append(node.left)
				if node.right:
					self.queue.append(node.right)
				self.queue.remove(node)
				if not self.queue:
					return False
				next_node = self.queue[0]
				return self.bfs_traversal(next_node)
		return False

	def find_height_of_tree(self, root):
		if root:
			return max(self.find_height_of_tree(root.left),
					   self.find_height_of_tree(root.right)) + 1
		return 0

	def do_bfs(self):
		print "Print tree"
		print self.tree.value
		print self.tree.left.value
		print self.tree.right.value
		print self.tree.left.left.value
		print self.tree.left.right.value
		print self.tree.right.right.value
		print "================"
		print "Inside bfs"
		self.bfs_traversal(self.tree)
		for i in self.bfs:
			print i.height, i.value
		print "================"

	def same_level_linking(self):
		prev_node = None
		print "$$$$$$$$$$$"
		for id, node in enumerate(self.bfs):
			if id == 0:
				prev_node = node
			else:
				if prev_node.height == node.height:
					prev_node.level_linking = node
					prev_node = node
				prev_node = node

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
	bfs = BFS()
	bfs.do_bfs()
	bfs.same_level_linking()
	bfs.print_same_level_root()

if __name__ == "__main__":
	main()
