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
		self.factor = CPT()

		
	def set_node_evidence(self,ass):
		self.cpt.set_evidence(self.var.name, ass)

	def print(self):
		print("\n var: ", self.var.name)
		print("domain: ", self.var.domain)
		print("ctp: ", self.cpt.print())
		print("parents: ", self.parents)
		self.factor.print("Factor")

	 
	def max_out(self):
		if DEBUG:
			self.cpt.print("cpt (prima del max_out)")
		self.factor = self.cpt.max_out(self.var.name)
		if DEBUG:
			self.factor.print("factor dopo il max out")

	def sum_out(self, target_var):
		if DEBUG:
			self.cpt.print("cpt (prima del sum_out)")
		self.cpt = self.cpt.sum_out(target_var)
		if DEBUG:
			self.cpt.print("factor (dopo il sum_out)")


		
	def pointwise_product(self,other_factor):
		if DEBUG:			
			self.cpt.print("cpt prima del pointwise_product")
		self.cpt = self.cpt.pointwise_product(other_factor.factor) 
		if DEBUG:
			self.cpt.print("cpt dopo il pointwise_product")
