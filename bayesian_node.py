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
		self.maxed_cpt = CPT()

		
	def set_node_evidence(self,value):
		self.cpt.set_evidence(self.var.name, value)


	def print(self):
		print("\n var: ", self.var.name)
		print("domain: ", self.var.domain)
		print("ctp: ", self.cpt.print())
		print("parents: ", self.parents)
		self.maxed_cpt.print("Maxed Cpt")

	 
	def max_out(self):
		if DEBUG:
			self.cpt.print("cpt (prima del max_out)")
		self.maxed_cpt = self.cpt.max_out(self.var.name)
		if DEBUG:
			self.maxed_cpt.print("maxed_cpt (dopo il max_out)")

	def sum_out(self, target_var):
		if DEBUG:
			self.cpt.print("cpt (prima del sum_out)")
		self.cpt = self.cpt.sum_out(target_var)
		if DEBUG:
			self.cpt.print("maxed_cpt (dopo il sum_out)")


		
	def pointwise_product(self,maxed_node):
		if DEBUG:			
			self.cpt.print("cpt prima del pointwise_product")
			
		self.cpt = self.cpt.pointwise_product(maxed_node.maxed_cpt) 

		if DEBUG:
			self.cpt.print("cpt dopo il pointwise_product")