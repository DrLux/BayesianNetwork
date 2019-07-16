DEBUG = False 

class CPT:
	def __init__(self):
		self.vars = []
		self.cpt = dict()

	
	def add(self,ass,value): 
		self.cpt[tuple(ass)] = value
		
	def set_vars(self, vars):
	    self.vars = vars

	def print(self, message="Print CPT"): 
		print(message)
		print(self.vars)
		for ass,value in self.cpt.items():
			print(ass," -> ",value)
		

	def max_out(self,target):
		if DEBUG:
			print("target max_out: ", target)
		factor = CPT()
		for ass,value in self.cpt.items():
			new_ass = list(ass) #il list serve per copiare i valori e non solo l'indirizzo
			new_vars = list(self.vars) #qui si può ottimizzare
			index_target = new_vars.index(target)
			if len(new_vars) > 1: #il caso in cui la variabile da eliminare è l' unica rimasta fa eccezione
				del new_vars[index_target]
				del new_ass[index_target]#rimuove l' ass corrispondende alla variabile target (by index)
			key = tuple(new_ass)
			if key in factor.cpt: 
				factor.cpt[key] = max(self.cpt[ass], factor.cpt[key])
			else:
				factor.cpt[key] = self.cpt[ass]
		
		factor.vars = new_vars
		return factor
		
	def pointwise_product(self,other_cpt):
		pointwise = CPT()
		common_var = sorted(set(self.vars).intersection(set(other_cpt.vars)))
		for ass,val in self.cpt.items():
			for other_ass,other_val in other_cpt.cpt.items():	
				if all([ass[self.vars.index(c_v)] == other_ass[other_cpt.vars.index(c_v)] for c_v in common_var]):
					new_ass = list(ass) #copio la lista non passo il puntatore
					new_vars = list(self.vars) #non lo faccio staticamente fuori dal loop perché devo rispettare l' ordine
					for i in range(len(other_cpt.vars)):#aggiunge le var e i relativi ass dell' altro nodo
						if other_cpt.vars[i] not in common_var:
							new_ass.append(other_ass[i])
							new_vars.append(other_cpt.vars[i])
					if DEBUG:
						print(other_val," * ", val, " = ", other_val*val)
					pointwise.cpt[tuple(new_ass)] = val* other_val	
		pointwise.vars = list(new_vars)
		return pointwise    
		
	def sum_out(self,target):
		if DEBUG:
			print("target max_out: ", target)
		factor = CPT()
		for ass,value in self.cpt.items():
			new_ass = list(ass) #il list serve per copiare i valori e non solo l'indirizzo
			new_vars = list(self.vars) #qui si può ottimizzare
			index_target = new_vars.index(target)
			if len(new_vars) > 1: #il caso in cui la variabile da eliminare è l' unica rimasta fa eccezione
				del new_vars[index_target]
				del new_ass[index_target]#rimuove l' ass corrispondende alla variabile target (by index)
			key = tuple(new_ass)
			if key in factor.cpt: 
				factor.cpt[key] = self.cpt[ass] + factor.cpt[key]
			else:
				factor.cpt[key] = self.cpt[ass]
		
		factor.vars = new_vars
		return factor

	def best_value(self):
		return max(list(self.cpt.values()))

	#ritorna il best assignment dati una lista di variabili e il rispettivo valore
	def best_ass_for_node_var(self,parents_var, parents_ass, node_name):
		best_ass = None
		best_value = -1
		if parents_var:
			for ass, val in self.cpt.items():
				if isinstance(parents_var, (list, tuple)):
					current_entry = all([ass[self.vars.index(p_v)] == parents_ass[parents_var.index(p_v)] for p_v in parents_var])
				else:
					current_entry =  ass[self.vars.index(parents_var)] == parents_ass

				if current_entry:
					if val > best_value:
						best_ass = ass[self.vars.index(node_name)] #prendo sempre il primo valore, ovvero del nodo corrente
						best_value = val

		else:
			for ass, val in self.cpt.items():
				if val > best_value:
					best_ass = ass[self.vars.index(node_name)] #prendo sempre il primo valore, ovvero del nodo corrente
					best_value = val
		return best_ass