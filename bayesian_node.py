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