"""
AI Homework
"""

class Node(object):
    def __init__(self, val, left=None, right=None):
        self.value = val
        self.left = left        
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

class AdjacencyNode(object):
    def __init__(self, vertex_name, vertex_parent=None, actual_cost=0,\
                 path_cost=0, total_cost=0):
        self._vertex_name = vertex_name
        self._vertex_parent = vertex_parent
        self._actual_cost = actual_cost
        self._path_cost = path_cost
        self._total_cost = total_cost

    @property
    def vertex_name(self):
        return self._vertex_name

    @property
    def vertex_parent(self):
        return self._vertex_parent

    @vertex_parent.setter
    def vertex_parent(self, val):
        self._vertex_parent = val

    @property
    def path_cost(self):
        return self._path_cost

    @path_cost.setter
    def path_cost(self, val):
        self._path_cost = val

    @property
    def actual_cost(self):
        return self._actual_cost

    @actual_cost.setter
    def actual_cost(self, val):
        self._actual_cost = val

    @property
    def total_cost(self):
        return self._total_cost

    @total_cost.setter
    def total_cost(self, val):
        self._total_cost = val

class Graph(object):
    def __init__(self):
        self._node_map = dict()

    @property
    def node_map(self):
        return self._node_map

    def add_edge(self, vertex_a, vertex_b, edge_cost):
        if vertex_a not in self.node_map:
            self.node_map[vertex_a] = list()
        if vertex_b not in self.node_map:
            self.node_map[vertex_b] = list()
        new_adj_node = AdjacencyNode(vertex_b, vertex_a, edge_cost, edge_cost, edge_cost)
        adj_list_va = self.node_map[vertex_a]
        adj_list_va.append(new_adj_node)

class Stack(object):
    def __init__(self, max_size_of_stack):
        self._stack = None
        self._max_size = max_size_of_stack
        self._stack_size = 0

    @property
    def stack(self):
        return self._stack

    @property
    def max_size(self):
        return self._max_size

    @property
    def stack_size(self):
        return self._stack_size

    def push(self, val):
        if self._stack_size > self.max_size:
            raise Exception("Stack is full")
        else:
            self._stack = self.node_front_insertion(val)
            self._stack_size = self._stack_size + 1
        return self.stack

    def pop(self):
        val = None
        if self._stack_size == 0:
            raise Exception("Stack is empty")
        else:
            val = self.node_front_removal()
            self._stack_size = self.stack_size - 1
        return val

    def node_front_insertion(self, val):
        if not self.stack:
            return Node(val)
        else:
            new_node = Node(val)
            new_node.right = self.stack
            return new_node 

    def node_front_removal(self):
        val = None
        if self.stack_size == 1:
            val = self.stack.value
            self._stack = None
        else:
            val = self.stack.value
            self._stack = self.stack.right
        return val

class Queue(object):
    def __init__(self, max_size_of_queue):
        self._queue = None
        self._max_size = max_size_of_queue
        self.queue_size = 0
        self.end_pointer = None

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, val):
        self._queue = val

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, val):
        self._max_size = val

    def enqueue(self, val):
        if self.queue_size > self.max_size:
            raise Exception("Queue is full")
        new_node = self.node_end_insertion(val)
        if not self.queue:
            self.queue = new_node
        self.queue_size = self.queue_size + 1
        self.end_pointer = new_node
        return self.queue

    def dequeue(self):
        val = None
        if self.queue_size == 0:
            raise Exception("Queue is empty")
        else:
            val = self.node_front_removal()
            self.queue_size = self.queue_size - 1
        return val

    def node_end_insertion(self, val):
        if not self.queue:
            return Node(val)
        else:
            new_node = Node(val)
            self.end_pointer.right = new_node
            return new_node

    def node_front_removal(self):
        val = None
        if self.queue_size == 1:
            val = self.queue.value
            self.queue = None
        else:
            val = self.queue.value
            self.queue = self.queue.right
        return val

class PriorityQueueAdjacencyList(object):
    def __init__(self, max_size_of_queue):
        self._queue = None
        self._max_size = max_size_of_queue
        self.queue_size = 0
        
    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, val):
        self._queue = val

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, val):
        self._max_size = val

    def enqueue(self, val):
        if self.queue_size > self.max_size:
            raise Exception("Queue is full")
        self.queue_size = self.queue_size + 1
        return self.node_inbetween_insertion(val)
        
    def dequeue(self):
        val = None
        if self.queue_size == 0:
            raise Exception("Queue is empty")
        else:
            val = self.node_front_removal()
            self.queue_size = self.queue_size - 1
        return val

    def node_inbetween_insertion(self, val):     
        if not self.queue:
            self.queue = Node(val)
        else:
            new_node = Node(val)
            
            cur_iter_item = self.queue
            prev_iter_item = None
            
            while(cur_iter_item):
                if cur_iter_item.value.total_cost <= val.total_cost:
                    prev_iter_item = cur_iter_item 
                    cur_iter_item = cur_iter_item.right
                else:
                    if prev_iter_item is None:
                        new_node.right = self.queue
                        self.queue = new_node
                        return self.queue
                    break
            prev_iter_item.right = new_node
            new_node.right = cur_iter_item
        return self.queue

    def get_node_value_in_queue(self, node_name):
        itr = self.queue
        while(itr):
            if itr.value.vertex_name == node_name:
                return itr
            else:
                itr = itr.right
        raise Exception("Didnt find any node")

    def update_in_queue(self, adj_node):
        itr = self.queue
        head = itr
        prev = None
        while(itr):
            if itr.value.vertex_name == adj_node.vertex_name:
                if prev:
                    prev.right = itr.right
                    del itr
                    self.queue = head
                    self.node_inbetween_insertion(adj_node)
                else:
                    self.queue = self.queue.right
                    self.node_inbetween_insertion(adj_node)
                return 
            else:
                prev = itr
                itr = itr.right
            
        raise Exception("Not updated")

    def update_child_nodes_in_queue(self, parent_node, heuristic_cost, expand_node):
        itr = self.queue
        head = self.queue
        prev = None
        while(itr):
            if itr.value.vertex_parent == parent_node.vertex_name:
                del expand_node[itr.value.vertex_name]
                if prev:
                    prev.right = itr.right
                else:
                    self.queue = self.queue.right               
                cur = itr
                itr = itr.right
                del cur
            else:
                prev = itr
                itr = itr.right
        

    def node_front_removal(self):
        val = None
        if self.queue_size == 1:
            val = self.queue.value
            self.queue = None
        else:
            val = self.queue.value
            self.queue = self.queue.right
        return val

class BFS(object):
    def __init__(self, graph_obj):
        self._graph_obj = graph_obj
        self._explored = dict()
        self._traversed_path = dict()

    @property
    def graph_obj(self):
        return self._graph_obj

    @property
    def explored(self):
        return self._explored

    @property
    def traversed_path(self):
        return self._traversed_path

    def bfs_traversal(self, start, dest):
        q = Queue(25000)

        # Case when source & destination are same
        if start == dest:
            self.traversed_path[start] = AdjacencyNode(start)
            self.explored[start] = True
            return self.traversed_path

        q.enqueue(AdjacencyNode(start))
        self.explored[start] = True
        while(q.queue):
            expand_node = q.dequeue()
            
            if expand_node.vertex_parent in self.traversed_path:
                parent_vertex = self.traversed_path[expand_node.vertex_parent]
                expand_node.path_cost = parent_vertex.path_cost + 1
            else:
                expand_node.path_cost = 0
            self.traversed_path[expand_node.vertex_name] = expand_node

            all_adj_nodes = self.graph_obj.node_map[expand_node.vertex_name]
            for adj_node in all_adj_nodes:
                if adj_node.vertex_name in self.explored:
                    continue
                self.explored[adj_node.vertex_name] = True
                if adj_node.vertex_name == dest:
                    parent_vertex = self.traversed_path[adj_node.vertex_parent]
                    adj_node.path_cost = parent_vertex.path_cost + 1
                    self.traversed_path[adj_node.vertex_name] = adj_node
                    return self.traversed_path
                q.enqueue(adj_node)

    def write_to_output(self, result_list):
        with open("output.txt", "w") as fp:
            for result in result_list:
                fp.write(result)        

    def solution_traversal(self, start, dest):
        final_list = list()
        while(dest != start):
            vertex = self.traversed_path[dest]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
            dest = vertex.vertex_parent
        else:
            vertex = self.traversed_path[start]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
        
        self.write_to_output(final_list)

class DFS(object):
    def __init__(self, graph_obj):
        self._graph_obj = graph_obj
        self._explored = dict()
        self._traversed_path = dict()

    @property
    def graph_obj(self):
        return self._graph_obj

    @property
    def explored(self):
        return self._explored

    @property
    def traversed_path(self):
        return self._traversed_path

    def dfs_traversal(self, start, dest):
        s = Stack(25000)

        # Case when source & destination are same
        if start == dest:
            self.traversed_path[start] = AdjacencyNode(start)
            self.explored[start] = True
            return self.traversed_path

        s.push(AdjacencyNode(start))
        self.explored[start] = True
        while(s.stack):
            expand_node = s.pop()
            if expand_node.vertex_parent in self.traversed_path:
                parent_vertex = self.traversed_path[expand_node.vertex_parent]
                expand_node.path_cost = parent_vertex.path_cost + 1
            else:
                expand_node.path_cost = 0
            self.traversed_path[expand_node.vertex_name] = expand_node

            if expand_node.vertex_name == dest:
                return self.traversed_path

            all_adj_nodes = self.graph_obj.node_map[expand_node.vertex_name]
            all_adj_nodes.reverse()
            for adj_node in all_adj_nodes:
                if adj_node.vertex_name in self.explored:
                    continue
                self.explored[adj_node.vertex_name] = True
                parent_vertex = self.traversed_path[adj_node.vertex_parent]
                adj_node.path_cost = parent_vertex.path_cost + 1
                #self.traversed_path[adj_node.vertex_name] = adj_node
                s.push(adj_node)
            
    def write_to_output(self, result_list):
        with open("output.txt", "w") as fp:
            for result in result_list:
                fp.write(result)        

    def solution_traversal(self, start, dest):
        final_list = list()
        while(dest != start):
            vertex = self.traversed_path[dest]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
            dest = vertex.vertex_parent
        else:
            vertex = self.traversed_path[start]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
        self.write_to_output(final_list)

class UCS(object):
    def __init__(self, graph_obj):
        self._graph_obj = graph_obj
        self._explored = dict()
        self._traversed_path = dict()

    @property
    def graph_obj(self):
        return self._graph_obj

    @property
    def explored(self):
        return self._explored

    @property
    def traversed_path(self):
        return self._traversed_path

    def ucs_traversal(self, start, dest):
        pq = PriorityQueueAdjacencyList(25000)

        # Case when source & destination are same
        if start == dest:
            self.traversed_path[start] = AdjacencyNode(start)
            self.explored[start] = True
            return self.traversed_path

        pq.enqueue(AdjacencyNode(start))
        self.explored[start] = True
        while(pq.queue):
            expand_node = pq.dequeue()
            self.traversed_path[expand_node.vertex_name] = expand_node

            if expand_node.vertex_name == dest:
                return self.traversed_path            

            all_adj_nodes = self.graph_obj.node_map[expand_node.vertex_name]
            for adj_node in all_adj_nodes:
                if adj_node.vertex_name in self.explored:
                    if adj_node.vertex_name not in self.traversed_path:
                        
                        pq_value = pq.get_node_value_in_queue(adj_node.vertex_name)
                        if pq_value.value.total_cost > adj_node.actual_cost + expand_node.total_cost:
                            adj_node.total_cost = adj_node.actual_cost + expand_node.total_cost
                            adj_node.path_cost = adj_node.total_cost
                            pq.update_in_queue(adj_node)
                else:
                    self.explored[adj_node.vertex_name] = True
                    parent_vertex = self.traversed_path[adj_node.vertex_parent]
                    adj_node.total_cost = parent_vertex.total_cost + adj_node.actual_cost
                    adj_node.path_cost = adj_node.total_cost
                    pq.enqueue(adj_node)

    def write_to_output(self, result_list):
        with open("output.txt", "w") as fp:
            for result in result_list:
                fp.write(result)        

    def solution_traversal(self, start, dest):
        final_list = list()
        while(dest != start):
            vertex = self.traversed_path[dest]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
            dest = vertex.vertex_parent
        else:
            vertex = self.traversed_path[start]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
        self.write_to_output(final_list)


class AStar(object):
    def __init__(self, graph_obj, heuristic_dict):
        self._graph_obj = graph_obj
        self._explored = dict()
        self._traversed_path = dict()
        self._heuristic_dict = heuristic_dict

    @property
    def graph_obj(self):
        return self._graph_obj

    @property
    def explored(self):
        return self._explored

    @property
    def traversed_path(self):
        return self._traversed_path

    @traversed_path.setter
    def traversed_path(self, val):
        self._traversed_path = val

    @property
    def heuristic_dict(self):
        return self._heuristic_dict

    def _update_child_nodes_in_traversed_path(self, parent_vertex, priority_queue_obj):
        for node_name, node in self.traversed_path.iteritems():
            if not node:
                continue
            if node.vertex_parent == parent_vertex:
                self.traversed_path[node.vertex_name] = None
                del self.explored[node.vertex_name]
                priority_queue_obj.update_child_nodes_in_queue(node, self.heuristic_dict, self.explored)
                self._update_child_nodes_in_traversed_path(node_name, priority_queue_obj)

    def remove_none_from_traversed_path(self):
        traverse_dict = dict(self.traversed_path)
        for key, value in traverse_dict.iteritems():
            if not value:
                del self.traversed_path[key]                

    def astar_traversal(self, start, dest):
        pq = PriorityQueueAdjacencyList(25000)

        # Case when source & destination are same
        if start == dest:
            self.traversed_path[start] = AdjacencyNode(start)
            self.explored[start] = True
            return self.traversed_path

        pq.enqueue(AdjacencyNode(start))
        self.explored[start] = True
        while(pq.queue):
            expand_node = pq.dequeue()
            self.traversed_path[expand_node.vertex_name] = expand_node

            if expand_node.vertex_name == dest:
                return self.traversed_path            

            all_adj_nodes = self.graph_obj.node_map[expand_node.vertex_name]
            for adj_node in all_adj_nodes:
                if adj_node.vertex_name in self.explored:
                    if adj_node.vertex_name in self.traversed_path:
                        if self.traversed_path[adj_node.vertex_name].total_cost > adj_node.actual_cost + expand_node.path_cost\
                                                        + self.heuristic_dict[adj_node.vertex_name]:
                            adj_node.path_cost = adj_node.actual_cost + expand_node.path_cost
                            adj_node.total_cost = adj_node.path_cost + self.heuristic_dict[adj_node.vertex_name]
                            del self.traversed_path[adj_node.vertex_name]
                            pq.enqueue(adj_node)
                            

                            self._update_child_nodes_in_traversed_path(adj_node.vertex_name, pq)
                            self.remove_none_from_traversed_path()
                            pq.update_child_nodes_in_queue(adj_node, self.heuristic_dict, self.explored)
                    
                    if adj_node.vertex_name not in self.traversed_path:
                        pq_value = pq.get_node_value_in_queue(adj_node.vertex_name)
                        if pq_value.value.total_cost > adj_node.actual_cost + expand_node.path_cost\
                                                        + self.heuristic_dict[adj_node.vertex_name]:
                            adj_node.path_cost = adj_node.actual_cost + expand_node.path_cost
                            adj_node.total_cost = adj_node.path_cost + self.heuristic_dict[adj_node.vertex_name]
                            pq.update_in_queue(adj_node)
                else:
                    self.explored[adj_node.vertex_name] = True
                    parent_vertex = self.traversed_path[adj_node.vertex_parent]
                    adj_node.path_cost = adj_node.actual_cost + expand_node.path_cost
                    adj_node.total_cost = adj_node.path_cost + self.heuristic_dict[adj_node.vertex_name]
                    pq.enqueue(adj_node)
            
    def write_to_output(self, result_list):
        with open("output.txt", "w") as fp:
            for result in result_list:
                fp.write(result)        

    def solution_traversal(self, start, dest):
        final_list = list()
        while(dest != start):
            vertex = self.traversed_path[dest]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
            dest = vertex.vertex_parent
        else:
            vertex = self.traversed_path[start]
            result = ' '.join([vertex.vertex_name, str(vertex.path_cost)]) + '\n'
            final_list.insert(0, result)
        self.write_to_output(final_list)




class ReadInput(object):
    def __init__(self):
        self._algo_type = None
        self._start = None
        self._dest = None
        self._num_traffic = None
        self._traffic_input = []
        self._num_heuristic = None
        self._heuristic_dict = []

    @property
    def algo_type(self):
        return self._algo_type

    @property
    def start(self):
        return self._start

    @property
    def dest(self):
        return self._dest

    @property
    def num_traffic(self):
        return self._num_traffic

    @property
    def traffic_input(self):
        return self._traffic_input

    @property
    def num_heuristic(self):
        return self._num_heuristic

    @property
    def heuristic_dict(self):
        return self._heuristic_dict
    
    def read(self):
        with open("input.txt", "r") as fp:
            lines = fp.readlines()
            self._algo_type = lines[0].strip()
            self._start = lines[1].strip()
            self._dest = lines[2].strip()

            self._num_traffic = lines[3].strip()
            for i in xrange(0, int(self.num_traffic)):
                self._traffic_input.append(lines[4+i].strip())

            self._num_heuristic = lines[4+int(self.num_traffic)].strip()
            for j in xrange(0, int(self.num_heuristic)):
                self._heuristic_dict.append(lines[5+int(self.num_traffic)+j].strip())
def main():
    read_input = ReadInput()
    read_input.read()
    graph = Graph()
    heuristic_dict = dict()
    for week_day_traffic in read_input.traffic_input:
        week_traffic = [x.strip() for x in week_day_traffic.split()]
        heuristic_dict[week_traffic[0].strip()] = 0
        heuristic_dict[week_traffic[1].strip()] = 0
        graph.add_edge(week_traffic[0].strip(), week_traffic[1].strip(), int(week_traffic[2].strip()))
    
    if read_input.algo_type == "BFS":
        bfs_obj = BFS(graph)
        bfs_obj.bfs_traversal(read_input.start, read_input.dest)
        bfs_obj.solution_traversal(read_input.start, read_input.dest)

    if read_input.algo_type == "DFS":
        dfs_obj = DFS(graph)
        dfs_obj.dfs_traversal(read_input.start, read_input.dest)
        dfs_obj.solution_traversal(read_input.start, read_input.dest)

    if read_input.algo_type == "UCS":
        ucs_obj = UCS(graph)
        ucs_obj.ucs_traversal(read_input.start, read_input.dest)
        ucs_obj.solution_traversal(read_input.start, read_input.dest)

    if read_input.algo_type == "A*":
        
        for sunday_traffic in read_input.heuristic_dict:
            sunday_traffic = [x.strip() for x in sunday_traffic.split()]
            heuristic_dict[sunday_traffic[0]] = int(sunday_traffic[1])
        astar_obj = AStar(graph, heuristic_dict)
        astar_obj.astar_traversal(read_input.start, read_input.dest)
        astar_obj.solution_traversal(read_input.start, read_input.dest)

if __name__ == "__main__":
    main()