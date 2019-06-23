from bayesian_node import *

class BayesNet:
	def __init__(self, variables, nodes, dict_nodes):
		self.nodes = nodes
		self.variables = variables
		self.dict_nodes = dict_nodes

	def print(self):
		for node in self.nodes:
			node.print()

	def get_all_nodes_var(self):
		return list(self.dict_nodes.keys())
		
	def set_evidence(self, var, ass): #fallo direttamente nel menu
		node = self.dict_nodes[var]
		node.set_node_evidence(ass)
    
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
			
		#node.print()
		
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


	def order_vars_to_remove(self,vars_to_remove):
		encode_vett_vars = dict()
		ordered_vars = []
		for v in vars_to_remove:
			encode_vett_vars[self.nodes.index(self.dict_nodes[v])] = v
		for index in sorted(encode_vett_vars.keys()):
			ordered_vars.append(self.nodes[index].var.name)
		return ordered_vars

	def map(self,evidences,map_vars):
		for e in evidences:
			self.set_evidence(e,evidences[e])
		
		if evidences:
			vars_to_preserve = set(map_vars).union(set(list(evidences.keys())))
		else: 
			vars_to_preserve = set(map_vars)
		vars_to_remove = set(self.get_all_nodes_var()).difference(vars_to_preserve)
		vars_to_remove = list(reversed(self.order_vars_to_remove(vars_to_remove)))

		
		nodes_to_process = []
		
		#moltiplico verso il padre
		node_parents = False
		print("vars_to_remove: ",vars_to_remove)
		for v  in vars_to_remove: 
			for node in self.nodes: 
				if v in node.parents:
					node_parents = True
					self.dict_nodes[v].cpt = self.dict_nodes[v].cpt.pointwise_product(node.cpt)
					node.parents.remove(v)
					node.parents += self.dict_nodes[v].parents
					nodes_to_process.append(node)
			if node_parents:
				node_to_sumout = self.dict_nodes[v]
				node_to_sumout.sum_out(v)
				for n in nodes_to_process:
					n.factor = node_to_sumout.cpt
					n.cpt = n.factor
			else:#da verificare se il caso foglia da i risultati giusti. In realtà osserco che moltiplicare e fare sum out rida la stessa cpt che c'era in origine, mi sa che le fogtlie si possono eliminare direttamente e basta
				for p in self.dict_nodes[v].parents: 
					self.dict_nodes[p].cpt = self.dict_nodes[p].cpt.pointwise_product(self.dict_nodes[v].cpt) 
					self.dict_nodes[p].cpt = self.dict_nodes[p].cpt.sum_out(v)
			self.nodes.remove(self.dict_nodes[v])
		
		#parte mpe
		maxed_node = None #inizio mpe
		for node in reversed(self.nodes):
			if node in nodes_to_process:
				node.full_max_out()
				maxed_node = node
			elif node.var.name in vars_to_preserve:
				if maxed_node:
					node.pointwise_product(maxed_node)
				node.max_out()
				maxed_node = node
		self.retropropagate_assignments(node)
		
		self.print()

	def retropropagate_assignments(self,last_node):
		history = CPT()
		history.vars = [last_node.cpt.best_value()]
		parents_ass = []	
		for i in range(0,len(self.nodes)):
			if (i == 0):
				best_ass = last_node.cpt.best_ass_for_node_var(None,None)
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