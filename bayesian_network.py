from bayesian_node import *

class BayesNet:
	def __init__(self, variables, nodes, dict_nodes):
		self.nodes = nodes
		self.variables = variables
		self.dict_nodes = dict_nodes

	def print(self):
		for node in self.nodes:
			node.print()

	def get_all_nodes(self):
		return list(self.dict_nodes.keys())
		
	def set_evidence(self, var, ass): #fallo direttamente nel menu
		node = self.dict_nodes[var]
		node.set_node_evidence(ass)
    
	def mpe(self,evidences):
		history = CPT()
		print(evidences)
		for e in evidences:
			self.set_evidence(e,evidences[e])
		maxed_node = None
		for node in reversed(self.nodes):
			if DEBUG:
				print("\n nome variabile: ",node.var.name)
			if maxed_node: #if maxed_out is not null
				node.pointwise_product(maxed_node)
			node.max_out()
			maxed_node = node
			
		node.print()
		
		history.vars = [node.cpt.best_value()]
		parents_ass = []	
		for i in range(0,len(self.nodes)):
			if (i == 0):
				best_ass = node.cpt.best_ass_for_node_var(None,None)
				history.cpt[self.nodes[i].var.name] = best_ass
			else:
				if self.nodes[i].parents:
					for p in self.nodes[i].parents:#se non ho i parent lo faccio sul nodo precedente
						parents_ass.append(history.cpt[p])
					best_ass = self.nodes[i].cpt.best_ass_for_node_var(self.nodes[i].parents, parents_ass)
				else:
					best_ass = self.nodes[i].cpt.best_ass_for_node_var(self.nodes[i-1].var.name,history.cpt[self.nodes[i-1].var.name])
				history.cpt[self.nodes[i].var.name] = best_ass
				parents_ass.clear()
		

		history.print("Best assignments")


	def map(self,evidences,map_vars):
		for e in evidences:
			self.set_evidence(e,evidences[e])
		
		if evidences:
			node_to_preserve = set(map_vars).union(set(list(evidences.keys())))
		else: 
			node_to_preserve = set(map_vars)
		vars_to_remove = sorted(set(self.get_all_nodes()).difference(node_to_preserve))
		vars_to_remove = (vars_to_remove)
		nodes_to_remove = []

		for map_v in vars_to_remove:
			for node in self.nodes:
				if map_v in node.parents:
					if DEBUG:
						print("\n nome node in corso: ",node.var.name)
					node.cpt = node.cpt.pointwise_product(self.dict_nodes[map_v].cpt)
					node.sum_out(map_v)
					node.parents.remove(map_v)
				if node.var.name == map_v:
					nodes_to_remove.append(node)

		for node in nodes_to_remove:
			self.nodes.remove(node)		

		print("fine map")
		self.mpe(dict())

