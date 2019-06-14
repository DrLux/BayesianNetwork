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

	def set_evidence(self, var, value):
		node = self.get_node(var)
		node.set_node_evidence(value)
		

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
		mpe_value = current_best_value
		for node in self.nodes:
			if history_cpt.assignments:
				target_vars, target_ass = history_cpt.get_ass_for_vars(node.parents)
				current_best_value = node.maxed_cpt.best_value_for_Ass(target_vars, target_ass) #l' ultimo Ass inserito (quello dell' iterazione precedente)
			best_ass = node.cpt.get_var_ass_from_value(node.var.name,current_best_value)
			history_cpt.add(Assignment(node.var.name, best_ass, current_best_value))
		
		print("Valore finale MPE: ", mpe_value)
		history_cpt.print("Best assignments")

