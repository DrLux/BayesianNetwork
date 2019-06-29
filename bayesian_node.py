from cpt import *

class BayesVar:
	def __init__(self, name, domain):
		self.name = name
		self.domain = domain
	

class BayesNode:
	def __init__(self, var, parents, cpt):
		self.var = var
		self.parents = parents
		self.cpt = cpt
		self.factor = cpt
		self.free = True #se non è stato ancora fattorizzato

	def set_node_evidence(self,ass):
		self.cpt.set_evidence(self.var.name, ass)

	def print(self):
		print("\n var: ", self.var.name)
		print("domain: ", self.var.domain)
		print("parents: ", self.parents)
		self.cpt.print("cpt")
		self.factor.print("Factor")


	def max_out(self):
		self.factor = self.cpt.max_out(self.var.name)
	
	def pointwise_product(self,other_factor):
		self.cpt = self.cpt.pointwise_product(other_factor.factor) 
	
	def sum_out(self):
		#print("prima ", self.cpt.print())
		self.factor = self.cpt.sum_out(self.var.name)
		#print("dopo ", self.cpt.print())
	'''
	def get_associated_vars(self): #versione dumb perché i metodi piu avanzati non funzionano inspiegabilmente
		diff = []
		for a in self.cpt.vars:
			if not a == self.var.name:
				diff.append(a)
		return diff
	

	#fa il max out su tutte le variabili della cpt che non sono tra i parent del nodo
	def full_max_out(self):
		var_to_max = set(self.get_associated_vars())-set(self.parents)
		self.factor = self.cpt
		for v in var_to_max:
			self.factor = self.factor.max_out(v)
		#self.factor = self.factor.max_out(self.var.name)
		
		
	'''