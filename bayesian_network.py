from bayesian_node import *

class BayesNet:
	def __init__(self, variables, nodes, dict_nodes, dict_children):
		self.nodes = nodes # node
		self.variables = variables # string
		self.dict_nodes = dict_nodes # string -> node
		self.dict_children = dict_children # string -> string

	def print(self):
		for node in self.nodes:
			node.print()

	def get_all_nodes_var(self):
		return list(self.dict_nodes.keys())
		
	def set_evidence(self, evidences):
		for var in evidences:
			node = self.dict_nodes[var]
			node.set_node_evidence(evidences[e])#assignment
    
	def mpe(self,evidences):
		self.set_evidence(evidences)
		maxed_node = None
		for node in reversed(self.nodes):
			if DEBUG:
				print("\n nome variabile: ",node.var.name)
			if maxed_node: #if maxed_out is not null
				node.pointwise_product(maxed_node)
			node.max_out()
			maxed_node = node

		self.retropropagate_assignments(maxed_node)

			
	def retropropagate_assignments(self,last_node):
		history = CPT()
		history.vars = [last_node.cpt.best_value()]
		parents_ass = []	
		for i in range(0,len(self.nodes)):
			if (i == 0):
				best_ass = last_node.cpt.best_ass_for_node_var(None,None,last_node.var.name)
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

	def make_factor(self,var_node, factors): 
		factors.append(self.dict_nodes[var_node].cpt)
		self.dict_nodes[var_node].free = False
		if var_node in self.dict_children:
			for c in self.dict_children[var_node]:
				if self.dict_nodes[c].free:
					factors.append(self.dict_nodes[c].cpt)
					self.dict_nodes[c].free = False	
		
		'''else: #sembra non necessario
			stop = False
			for p in self.dict_nodes[var_node].parents:
				if self.dict_nodes[p].free and stop == False:
					factors.append(self.dict_nodes[p].cpt)
					self.dict_nodes[p].free = False
					stop = True'''


	def remove_non_map(self, factors,vars_to_remove):
		new_factor = None
		processed_factors = []
		
		'''
		for v in vars_to_remove:
			for f in factors:
				if v in f.vars:
					if new_factor:
						new_factor = new_factor.pointwise_product(f) #estraggo i fattori della var e li moltiplico tra loro 
						processed_factors.append(f)
					else:
						new_factor = f
						processed_factors.append(f)
			new_factor = new_factor.sum_out(v)
			factors.append(new_factor)
			new_factor = None
			for rf in processed_factors:
				factors.remove(rf)
			processed_factors = []
		
		final_fact = factors.pop(0)
		for fa in factors:
			final_fact = final_fact.pointwise_product(fa)
		'''
		for f in factors:
			if new_factor:
				new_factor = new_factor.pointwise_product(f) #estraggo i fattori della var e li moltiplico tra loro 
			else:
				new_factor = f
		for v in vars_to_remove:
			new_factor = new_factor.sum_out(v)

		final_fact = new_factor
		return final_fact
		
	def map(self,evidences,map_vars):
		if not map_vars:
			self.mpe(evidences)

		if evidences:
			vars_to_preserve = set(map_vars).union(set(list(evidences.keys())))
		else: 
			vars_to_preserve = set(map_vars)
		vars_to_remove = set(self.get_all_nodes_var()).difference(vars_to_preserve)
		vars_to_remove = list(reversed(self.order_vars_to_remove(vars_to_remove))) #le ordino in senso topologico
	
		#Setto le evidenze		
		self.set_evidence(evidences)

		#Raccoglo i fattori
		factors = []
		for v in vars_to_remove:
			self.make_factor(v,factors)

		
		#Rimuovo i fattori non map (sum_out)
		factor = self.remove_non_map(factors,vars_to_remove)
		#print("print di facor prima di mpe")
		#factor.print()

		#Propago sui nodi MAP (max_out)
		for node in reversed(self.nodes):
			if node.var.name in vars_to_preserve:
				if node.free:
					node.cpt = node.cpt.pointwise_product(factor)
					#print("print iniziale: ", node.cpt.print())
				else:
					node.cpt = factor
				node.factor = node.cpt #mi salvo la cpt per la redistribuzione degli assegnamenti dopo
				node.cpt = node.cpt.max_out(node.var.name)
				#print("print dopo il max out di ", node.var.name," : ", node.cpt.print())

				factor = node.cpt
				node.parents = node.cpt.vars
			else:
				self.nodes.remove(node)

		#Retropropagazione degli assegnamenti
		print("printo cpt finale")
		factor.print()
		#self.print()
		history = CPT()
		for i in range(0,len(self.nodes)):
			if (i == 0):
				history.vars = [self.nodes[i].factor.best_value()]
				best_ass = self.nodes[i].factor.best_ass_for_node_var(None,None, self.nodes[i].var.name)
				history.cpt[self.nodes[i].var.name] = best_ass
			else:
				#print(history.print())
				best_ass = self.nodes[i].factor.best_ass_for_node_var(list(history.cpt.keys()),list(history.cpt.values()),self.nodes[i].var.name)
				history.cpt[self.nodes[i].var.name] = best_ass

		history.print("Best assignments")
		