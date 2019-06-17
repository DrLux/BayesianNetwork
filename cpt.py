DEBUG = True 


class CPT:
	def __init__(self):
		self.assignments = []

	
	def add(self,Assignment): 
		self.assignments.append(Assignment)

	def print(self, message="Print CPT"): 
		print(message)
		for entry in self.assignments:
			entry.print()
		
	#supporta una sola variabile e un solo valore
	def set_evidence(self,name_var,ass):
		for entry in self.assignments:
			index = entry.vars.index(name_var)
			if entry.ass[index] != ass:
				entry.val = 0
	
	def max_out(self,target):
		if DEBUG:
			print("target max_out: ", target)
		dict_maxed_cpt = dict()
		for entry in self.assignments:
			new_ass = list(entry.ass)
			new_vars = list(entry.vars)
			index_target = entry.vars.index(target)
			if len(new_vars) > 1: #il caso in cui la variabile da eliminare è l' unica rimasta fa eccezione
				del new_vars[index_target]
				del new_ass[index_target]#rimuove l' ass corrispondende alla variabile target (by index)
			key = tuple(new_ass)
			if key in dict_maxed_cpt: 
				dict_maxed_cpt[key] = max(entry.val, dict_maxed_cpt[key])
			else:
				dict_maxed_cpt[key] = entry.val
		return self.dict_to_cpt(new_vars,dict_maxed_cpt)

	def dict_to_cpt(self,new_vars,dict_maxed_cpt):
		new_cpt = CPT()
		for ass,value in dict_maxed_cpt.items():
			new_cpt.add(Assignment(new_vars,ass,value))
		return new_cpt

	def old_max_out(self,target):
		if DEBUG:
			print("target max_out: ", target)
		maxed_cpt = CPT()
		for entry in self.assignments:
			new_vars = list(entry.vars) 
			new_ass = list(entry.ass)
			index_target = entry.vars.index(target)
			if len(new_vars) > 1: #il caso in cui la variabile da eliminare è l' unica rimasta fa eccezione
				del new_vars[index_target]
				del new_ass[index_target]#rimuove l' ass corrispondende alla variabile target (by index)
			if maxed_cpt.contains(new_vars,new_ass):
				new_val = max(entry.val,maxed_cpt.get_value(new_vars,new_ass))
				maxed_cpt.update(new_vars,new_ass, new_val)
			else:
				maxed_cpt.add(Assignment(new_vars,new_ass, entry.val))
		return maxed_cpt
	
	def contains(self,vett_vars,vett_ass):
		print("Entato in cointains")
		for entry in self.assignments:
			if entry.contains(vett_vars,vett_ass): #ferma il ciclo appena hai un match
				print("Uscito precocemente da cointains")
				return True
		print("Uscita standard da cointains")
		return False

	def update(self,vett_vars,vett_ass,val):
		for entry in self.assignments:
			if entry.contains(vett_vars,vett_ass): 
				entry.val = val

	def get_value(self,vett_vars,vett_ass):
		for entry in self.assignments:
			if entry.contains(vett_vars,vett_ass):
				return entry.val

	def pointwise_product(self,other_cpt):
		new_cpt = CPT()
		for entry in self.assignments:
			for other_entry in other_cpt.assignments:
				if entry.partial_contains(other_entry.vars,other_entry.ass) or other_entry.partial_contains(entry.vars,entry.ass): 
					new_vars = list(entry.vars) #copio la lista non passo il puntatore
					new_ass = list(entry.ass) #copio la lista non passo il puntatore
					for i in range(len(other_entry.vars)):#aggiunge le var e i relativi ass dell' altro nodo
						if other_entry.vars[i] not in new_vars:
							new_vars.append(other_entry.vars[i])
							new_ass.append(other_entry.ass[i])
					if DEBUG:
						print(other_entry.val," * ", entry.val, " = ", other_entry.val*entry.val)
					new_cpt.add(Assignment(new_vars,new_ass,(other_entry.val*entry.val)))	

		return new_cpt

	def get_best_ass(self, target_var, history):
		best_ass = None
		for entry in self.assignments:
			if not best_ass or best_ass.val < entry.val : #se best_ass è vuoto o comunque inferiore ad entry
				best_ass = entry    
		return best_ass

	def get_var_ass_from_value(self, target_var, target_value):
		for entry in self.assignments:
			if entry.val == target_value:
				return entry.get_var_ass(target_var)
	
	def	best_value_for_Ass(self,target_vals, target_ass):
		best_value = -1
		for entry in self.assignments:
			if entry.contains(target_vals, target_ass):
				best_value = max(best_value, entry.val)
		return best_value

	#da una lista di Ass devo crearne uno che contiene solo var-ass interessate. 
	#Se il nodo ha i padri (vett_vars =! null) allora cerca l' ass di quelli 
	#Se vett_vars è nullo cerco l' ass del nodo precedente, ovvero l' ultimo in lista
	def get_ass_for_vars(self,parents_vars):
		target_ass = []
		target_vars = [] #se il nodo ha parenti quelli sono i suoi target, altrimenti inizializzera con array vuoto
		if (parents_vars):#se il nodo attuale ha parents
			for entry in self.assignments:
				for v in parents_vars:
					if v in entry.vars:
						target_vars.append(v)
						target_ass.append(entry.get_var_ass(v))
		else: #se non li ha usa l' ultimo nodo visto finora
			target_vals =  self.assignments[-1].vars
			target_ass = self.assignments[-1].ass
		return target_vars, target_ass

	def best_value(self):
		best_value = -1
		for entry in self.assignments:
			best_value = max(best_value, entry.val)
		return best_value

	def sum_out(self,target):
		maxed_cpt = CPT()
		for entry in self.assignments:
			new_vars = list(entry.vars) 
			new_ass = list(entry.ass)
			index_target = entry.vars.index(target)
			if len(new_vars) > 1: #il caso in cui la variabile da eliminare è l' unica rimasta fa eccezione
				del new_vars[index_target]
				del new_ass[index_target]#rimuove l' ass corrispondende alla variabile target (by index)
			if maxed_cpt.contains(new_vars,new_ass):
				new_val = entry.val + maxed_cpt.get_value(new_vars,new_ass)
				maxed_cpt.update(new_vars,new_ass, new_val)
			else:
				maxed_cpt.add(Assignment(new_vars,new_ass, entry.val))
		return maxed_cpt

class Assignment:
	def __init__(self, vars, ass, val):
		self.vars = vars
		self.ass = ass
		self.val = val

	def print(self,message=""):
		print(message, self.vars, " = ", self.ass, " ->", self.val)

	#verifica (solo tra le variabili in comune tra quelle date e quelle di self.vars) che tutti i rispettivi ass coincidano con quelli delle rispettive variabili in self.ass
	def partial_contains(self,vett_vars,vett_ass):
		common_vars = list(set(vett_vars).intersection(self.vars))
		#crea un vettore di booleani che all() mette tutti in and
		return all([self.ass[self.vars.index(common_vars[i])] == vett_ass[vett_vars.index(common_vars[i])] for i in range(len(common_vars))])


	#per ogni var in vett_vars controlla che sia in self.vars e che il corrispondente ass coincida con quello in self.ass
	def contains(self,vett_vars,vett_ass):
		#crea un vettore di booleani che all() mette tutti in and
		if vett_vars: 
			return all([vett_vars[i] in self.vars and self.ass[self.vars.index(vett_vars[i])] == vett_ass[i] for i in range(len(vett_vars))])
		else: #voglio solo vedere se in questa entry c'è un determinato assignments (senza rispettiva var)
			return (vett_ass in self.ass) 


	#la variabile passata è una singola var
	def get_var_ass(self,var):		
		if isinstance(self.ass, list):
			index_var = self.vars.index(var)
			return self.ass[index_var]
		else:
			return self.ass

	 