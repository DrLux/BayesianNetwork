from bayesian_node import *

class BayesNet:
	def __init__(self, variables, nodes):
		self.nodes = nodes
		self.variables = variables

	def print(self):
		for node in self.nodes:
			node.print()

	def get_node(self, name):
		for node in self.nodes:
			if node.var.name==name:
				return node
		return None

	def set_evidence(self, var, value): #fallo direttamente nel menu
		node = self.get_node(var)
		node.set_node_evidence(value)

	def get_all_name_vars(self):
		return [v.name for v in self.variables]

    
	def mpe(self,evidences):
		history = CPT()
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
	
		history.vars = [node.cpt.best_value()]

		parents_ass = []		
		for node in self.nodes:
			for p in node.parents:
				parents_ass.append(history.cpt[p])
			best_ass = node.cpt.best_ass_for_node_var(node.parents, parents_ass)
			history.cpt[node.var.name] = best_ass
			parents_ass.clear()
		

		history.print("Best assignments")


	def map(self,evidences,map_vars):
		for e in evidences:
			self.set_evidence(e,evidences[e])
		
		all_vars = self.get_all_name_vars()
		node_to_preserve = set(map_vars).union(set(list(evidences.keys())))
		vars_to_remove = set(all_vars).difference(node_to_preserve)
		nodes_to_remove = []
		
		for map_v in vars_to_remove:
			for node in self.nodes:
				if map_v in node.parents:
					if DEBUG:
						print("\n nome node in corso: ",node.var.name)
					node.cpt = node.cpt.pointwise_product(self.get_node(map_v).cpt)
					node.sum_out(map_v)
					node.parents.remove(map_v)
				if node.var.name == map_v:
					nodes_to_remove.append(node)

		print("FINE MAP ")
		for node in nodes_to_remove:
			self.nodes.remove(node)		

		self.mpe(dict())

