"""
BFS
"""
class AdjacencyList(object):
	def __init__(self):
		self.hashmap = dict()

	@property
	def hashmap(self):
	    return self._hashmap

	@hashmap.setter
	def hashmap(self, value):
	    self._hashmap = value

	def add_edge(self, source, destination):
		if not (source in self.hashmap):
			self.hashmap[source] = list()
		self.hashmap[source].append(destination)


class Forest(object):
	def __init__(self):
		self.forest = self.manual_forest_creation()

	def manual_forest_creation(self):
		adj_list = AdjacencyList()
		adj_list.add_edge(0,1)
		adj_list.add_edge(0,2)
		adj_list.add_edge(1,2)
		adj_list.add_edge(2,0)
		adj_list.add_edge(2,3)
		adj_list.add_edge(3,3)
		return adj_list.hashmap

	def get_forest(self):
		return self.forest

class BFS(object):
	def __init__(self, start_node):
		self.start_node = start_node
		self.bfs = []
		self.queue = [start_node]
		self.forest = self.get_forest()
		self.traveresd_nodes = self.create_all_nodes()

	def get_forest(self):
		forest = Forest()
		return forest.get_forest()

	def create_all_nodes(self):
		key_map = {}
		print self.forest
		for key, value in self.forest.items():
			key_map[key] = None
		return key_map

	def bfs_traversal(self, node):
		if not self.queue:
			return False
		else:
			if self.traveresd_nodes[node] == 1:
				self.traveresd_nodes[node] = 1
				self.bfs.append(node)
				self.queue.extend(self.forest[node])
				self.queue.remove(node)
				next_node = self.queue[0]
				self.queue = self.queue[1:]
				return self.bfs_traversal(next_node)
			else:
				return False

	def do_bfs(self):
		self.bfs_traversal(self.start_node)
		for i in self.bfs:
			print i

def main():
	bfs = BFS(2)
	bfs.do_bfs()

if __name__ == "__main__":
	main()





