import time
from bn_parser import *
import os 
from os.path import isfile, join
# sito dove scaricare le reti: '''http://www.bnlearn.com/bnrepository/

class Menu:
	def __init__(self):
		self.load_network()

	def load_network(self):
		print("Loading network...")
		start_time = time.time()
		networs_path = join(os.getcwd(), "networks")
		available_networks = os.listdir(networs_path)

		print('\n List of available networks: ')
		for net,index in enumerate(available_networks):
			print(net,") ",index)
		choice = input('\nWhich one do you want to load? (Insert index number):')

		self.path = join(networs_path, available_networks[int(choice)])
		self.network = load_net(self.path)
		self.evidences = dict()
		print("'",available_networks[int(choice)],"' Loaded in %s seconds!" % (time.time() - start_time),"\n")
		self.main_menu()

	def set_evidences(self,all_vars):
		print("\nAll the available variables: \n")
		print("0 )  [Back to Main Menu!]")
		for index,v in enumerate(all_vars):
			print(index+1, ") ", v.name)
		var_choice = input("\n Choose the variable:")
		if var_choice == '0':
			return 
		var = all_vars[int(var_choice)-1]
		for index,d in enumerate(var.domain):
			print(index, ") ", d)
		ass_choice = input("\n What assignment do you want?")
		ass = var.domain[int(ass_choice)]
		self.evidences[var.name] = ass
		self.set_evidences(all_vars)



	def select_map_var(self):
		all_vars = self.network.variables
		print("\nAll the available variables: \n")
		print("0 )  [Calculate MAP]")
		for index,v in enumerate(all_vars):
			if v.name in self.selected_map_vars or v.name in self.evidences.keys():
				print(v.name, "is already selected")
			else: 
				print(index+1, ") ", v.name)
		var_choice = input("\n Choose one MAP variables:")
		if var_choice == '0':
			return 
		if  all_vars[int(var_choice)-1].name not in self.selected_map_vars and all_vars[int(var_choice)-1].name not in self.evidences.keys():
			self.selected_map_vars.append(all_vars[int(var_choice)-1].name)
		self.select_map_var()

	def main_menu(self):
		'''all_vars = self.network.variables
		var = all_vars[0]
		ass = var.domain[0]
		self.evidences[var.name] = ass

		var = all_vars[10]
		ass = var.domain[3]
		self.evidences[var.name] = ass

		var = all_vars[16]
		ass = var.domain[2]
		self.evidences[var.name] = ass

		var = all_vars[12]
		ass = var.domain[1]
		self.evidences[var.name] = ass
		self.network.mpe(self.evidences)
		'''
		print("\nMain Menu")
		print("0) Change Network")
		print("1) Print Network")
		print("2) Set Evidences")
		print("3) MPE")
		print("4) MAP")
		print("5) [Quit!]")
		main_choice = input("\nWhat you want to do?")
		if main_choice == '0':
			self.load_network()
		elif main_choice == '1':
			self.network.print()
			self.main_menu()
		elif main_choice == '2':
			self.set_evidences(self.network.variables)
			self.main_menu()
		elif main_choice == '3':
			start_time = time.time()
			self.network.mpe(self.evidences)
			print("--- %s seconds ---" % (time.time() - start_time))
			self.network = load_net(self.path)
			self.main_menu()
		elif main_choice == '4':
			self.selected_map_vars = []
			self.select_map_var()
			self.network.map(self.evidences,self.selected_map_vars)
		


if __name__ == "__main__":
	Menu()
