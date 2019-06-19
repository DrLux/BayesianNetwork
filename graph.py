class Graph:
	def __init__(self):
		self.graph = dict()
		self.roots = []
		self.nodes = dict()

	def add_nodes(self,name,node):
		self.nodes[name] = node
	
	def add_root(self, root):
		self.roots += root

	def add(self,node,parents):
		for p in parents:
			if p in self.graph:
				self.graph[p] += node
			else:
				self.graph[p] = node

	def order_nodes(self,net_nodes):
		frontier = set(self.roots)
		topoligical_order = self.roots
		for node in topoligical_order:
			if node in self.graph:
				children = set(self.graph[node])
				only_new_children = children-frontier
				topoligical_order += list(only_new_children)
				frontier = frontier.union(only_new_children)			

		ordered_nodes = []	
		for to in topoligical_order:
			ordered_nodes.append(self.nodes[to])
			
		return ordered_nodes

		