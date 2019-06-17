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
			print("node.name: ",node.var.name)
			if node.var.name==name:
				return node
		return None

	def set_evidence(self, var, value):
		node = self.get_node(var)
		node.set_node_evidence(value)

	def get_all_name_vars(self):
		return [v.name for v in self.variables]

	def mpe(self,evidences):
		history_cpt = CPT()
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

		current_best_value = node.maxed_cpt.best_value()
		best_ass = node.cpt.get_var_ass_from_value(node.var.name,current_best_value)
		print("current_best_value: ",current_best_value)
		print("best_ass: ",best_ass)

		'''current_best_value = node.maxed_cpt.best_value()
								mpe_value = current_best_value
								for node in self.nodes:
									if history_cpt.assignments:
										target_vars, target_ass = history_cpt.get_ass_for_vars(node.parents)
										current_best_value = node.maxed_cpt.best_value_for_Ass(target_vars, target_ass) #l' ultimo Ass inserito (quello dell' iterazione precedente)
									best_ass = node.cpt.get_var_ass_from_value(node.var.name,current_best_value)
									history_cpt.add(Assignment(node.var.name, best_ass, current_best_value))'''
		
		#print("Valore finale MPE: ", mpe_value)
		history_cpt.print("Best assignments")

	def map(self,evidences,map_vars):
		#for e in evidences:
		#	self.set_evidence(e,evidences[e])

		all_vars = self.get_all_name_vars()
		node_to_preserve = set(map_vars).union(set(list(evidences.keys())))
		vars_to_remove = set(all_vars).difference(node_to_preserve)
		nodes_to_remove = []
		
		for map_v in vars_to_remove:
			for node in self.nodes:
				if map_v in node.parents:
					node.cpt = node.cpt.pointwise_product(self.get_node(map_v).cpt)
					node.cpt = node.cpt.sum_out(map_v)
					node.parents.remove(map_v)
				if node.var.name == map_v:
					nodes_to_remove.append(node)

		for node in nodes_to_remove:
			self.nodes.remove(node)		

		self.mpe(evidences)

