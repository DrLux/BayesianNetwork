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

	def order_nodes(self,net_nodes):#a.insert(posizione,valore)
		ordered_nodes = []
		node_leaf = []
		
		#aggiungo i root
		for r in self.roots:
			ordered_nodes.append(self.nodes[r])
			net_nodes.remove(self.nodes[r])	

		#estrapolo le foglie
		for node in net_nodes:
			if not node.var.name in self.graph:
				node_leaf.append(node)
				net_nodes.remove(node)

		#aggiungo i nodi intermedi
		while net_nodes: #finché non ho svuotato tutto net_nodes
			for node in net_nodes:
				if not node.var.name in self.roots:
					if all([self.nodes[p] in ordered_nodes for p in node.parents]): #se tutti i padri del nodo sono gia nella rete
						ordered_nodes.append(node)
						net_nodes.remove(node)

		#riaggiungo le foglie
		ordered_nodes += node_leaf
		 
		return ordered_nodes,self.nodes