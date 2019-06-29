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

		for node in net_nodes:
			if node.var.name in self.roots or len(ordered_nodes) == 0: #se sei root o tanto comunque la lista degli ordinati è vuota, mettiti in testa
				ordered_nodes.insert(0,node)
			else:		
				for i in range(0,len(ordered_nodes)):
					if node.var.name not in self.graph or len(ordered_nodes) == i+1: #se non è nel grafo, o sono arrivato alla fine significa che è una foglia, aggiungo in coda
						ordered_nodes.append(node)
						break
					else:
						parents = list(node.parents)
						if ordered_nodes[i].var.name in parents: #se incontro un mio parents elimino quel parents dalla lista
							parents.remove(ordered_nodes[i].var.name)
						
						if (ordered_nodes[i+1].var.name in self.graph[node.var.name]) or not parents: #se becco un mio figlio o ho passato tutti i miei parents mi aggiungo in quel punto
							ordered_nodes.insert(i+1,node)
							break
		return ordered_nodes,self.nodes,self.graph