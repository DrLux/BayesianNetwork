from bayesian_node import *

class BayesNet:
	def __init__(self, variables, nodes, dict_nodes):
		self.nodes = nodes # node
		self.variables = variables # node.var
		self.dict_nodes = dict_nodes # string -> node
	
	def remove_node(self, node):
		self.nodes.remove(node)
		self.variables.remove(node.var)
		del self.dict_nodes[node.var.name]

	def print(self):
		for node in self.nodes:
			node.print()

	def get_all_nodes_var(self):
		return list(self.dict_nodes.keys())
		
	def set_evidence(self, evidences):
		for var in evidences:
			node = self.dict_nodes[var]
			node.set_node_evidence(evidences[var])#assignment
    
	def mpe(self,evidences):
		self.set_evidence(evidences)
		
		factors = []
		for node in reversed(self.nodes):
			factors.append(node.cpt)
			factors = self.max_out_factor(node, factors) 
		
		#print("Evidences: ", evidences)
		#self.retropropagate_assignments(factors[0])
		
			
	def retropropagate_assignments(self,cpt_last_node):
		history = CPT()
		history.vars = [cpt_last_node.best_value()]
		parents_ass = []	
		for i in range(0,len(self.nodes)):
			if (i == 0):
				best_ass = self.nodes[i].cpt.best_ass_for_node_var(None,None,self.nodes[i].var.name)
				history.cpt[self.nodes[i].var.name] = best_ass
			else:
				if self.nodes[i].parents:
					for p in self.nodes[i].parents:#se non ho i parent lo faccio sul nodo precedente
						parents_ass.append(history.cpt[p])
					best_ass = self.nodes[i].cpt.best_ass_for_node_var(self.nodes[i].parents, parents_ass,self.nodes[i].var.name)
				else:
					best_ass = self.nodes[i].cpt.best_ass_for_node_var(self.nodes[i-1].var.name,history.cpt[self.nodes[i-1].var.name],self.nodes[i].var.name)
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
		if not map_vars:
			self.mpe(evidences)

		if evidences:
			vars_to_preserve = set(map_vars).union(set(list(evidences.keys())))
		else: 
			vars_to_preserve = set(map_vars)
		vars_to_remove = set(self.get_all_nodes_var()).difference(vars_to_preserve)
		vars_to_remove = list(reversed(self.order_vars_to_remove(vars_to_remove))) #le ordino in senso topologico
	
		
		factors = []
		for node in reversed(self.nodes):
			factors.append(self.make_factor(node.cpt,evidences))
			if node.var.name in vars_to_remove:
				factors = self.sum_out_factor(node.var.name, factors) 
		for node in reversed(self.nodes):
			if node.var.name in vars_to_preserve:
				factors = self.max_out_factor(node, factors)
			else:
				self.nodes.remove(node)
		
		#print("Evidences: ", evidences)
		#print("Map var: " )
		#for v in vars_to_preserve:
		#	print(v.var.name)
		#self.retropropagate_assignments(factors[0])
		

	def make_factor(self,cpt,evidences):
		factor = CPT()
		factor.vars = cpt.vars
		no_evidence = True
		for e in evidences:
			if e in cpt.vars:
				no_evidence = False
				for ass,val in cpt.cpt.items():
					if ass[cpt.vars.index(e)] == evidences[e]:
						factor.cpt[ass] = val		
		if no_evidence:
			return cpt		
		return factor
		

	def sum_out_factor(self,var_to_remove, factors):
		result = []
		new_factor = None
		for f in factors:
			if var_to_remove in f.vars:
				if new_factor:
					new_factor = new_factor.pointwise_product(f)
				else:
					new_factor = f
			else:
				result.append(f)
		new_factor = new_factor.sum_out(var_to_remove)
		result.append(new_factor)
		return result
		

	def max_out_factor(self,node_to_remove, factors):
		result = []
		new_factor = None
		for f in factors:
			if node_to_remove.var.name in f.vars:
				if new_factor:
					new_factor = new_factor.pointwise_product(f)
				else:
					new_factor = f
			else:
				result.append(f)
	
		node_to_remove.cpt = new_factor
		new_factor = new_factor.max_out(node_to_remove.var.name)
		result.append(new_factor)
		node_to_remove.parents = new_factor.vars
		return result