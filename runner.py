import time
import os 
from os.path import isfile, join
import matplotlib.pyplot as plt
# sito dove scaricare le reti: '''http://www.bnlearn.com/bnrepository/

class Menu:
	def __init__(self):
		self.load_network()

	def load_network(self):
		print("Loading network...")
		networs_path = join(os.getcwd(), "BayesianNetwork/networks")
		available_networks = os.listdir(networs_path)

		print('\n List of available networks: ')
		for net,index in enumerate(available_networks):
			print(net,") ",index)
		choice = input('\nWhich one do you want to load? (Insert index number):')
    
		start_time = time.time()
		self.path = join(networs_path, available_networks[int(choice)])
		self.network = load_net(self.path)
		self.evidences = dict()
		self.network_name = available_networks[int(choice)]
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

	def plot_data(self,x_axis,y_axis,x_label,y_label,title):
		plt.plot(x_axis,y_axis)
		plt.ylabel(y_label)
		plt.xlabel(x_label)
		plt.title(title+" on "+self.network_name)
		plt.savefig(self.network_name+x_label+'_'+title+'.jpg')
		plt.close() # Close a figure window
		print("Dumped ",self.network_name," ",x_label+'_'+title+'.jpg')

	def main_menu(self):
		print("\nMain Menu")
		print("0) Change Network")
		print("1) Print Network")
		print("2) Set Evidences")
		print("3) MPE")
		print("4) MAP")
		print("5) Benchmark Dimension")
		print("6) Benchmark Evidences")
		print("7) Benchmark Map Vars")
		print("8) [Quit!]")
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
			start_time = time.time()
			self.selected_map_vars = []
			self.select_map_var()
			self.network.map(self.evidences,self.selected_map_vars)
			print("--- %s seconds ---" % (time.time() - start_time))
		elif main_choice == '5':
			#MPE DIMENSION
			x_axis = []
			y_axis = []
			
			for i in range(0, len(self.network.nodes)):
				for n in range(0,i):
					self.network.remove_node(self.network.nodes[-1])
				start_time = time.time()
				self.network.mpe(self.evidences,True)
				x_axis.append(len(self.network.nodes)) 
				y_axis.append(time.time() - start_time)

				self.network = load_net(self.path)
			self.plot_data(x_axis,y_axis,"Dimension","Execution Time", "MPE")

			#MAP DIMENSION
			x_axis = []
			y_axis = []
			for i in range(0, len(self.network.nodes)):
				print("Iterazione numero ",i)
				self.selected_map_vars = []
				for n in range(0,i):
					self.network.remove_node(self.network.nodes[-1])
				x_axis.append(len(self.network.nodes))
				for m in range(0,int(len(self.network.nodes)/2)):
					self.selected_map_vars.append(self.network.nodes[m])
				start_time = time.time()
				self.network.map(self.evidences,self.selected_map_vars,True) 
				y_axis.append(time.time() - start_time)
			
				self.network = load_net(self.path)
			self.plot_data(x_axis,y_axis,"Dimension","Execution Time", "MAP")

		elif main_choice == '6':
			
			#MPE Evidences
			x_axis = []
			y_axis = []
			
			for i in range(0, len(self.network.nodes)):
				print("Iterazione numero ",i)
				for n in range(0,i):
					self.evidences[self.network.nodes[n].var.name] = self.network.nodes[n].var.domain[0]
				start_time = time.time()
				self.network.mpe(self.evidences,True)
				x_axis.append(len(self.evidences)) 
				y_axis.append(time.time() - start_time)

				self.network = load_net(self.path)
			self.plot_data(x_axis,y_axis,"Evidences","Execution Time", "MPE")
			
			
			#MAP Evidences
			x_axis = []
			y_axis = []
			self.evidences.clear()
			
			for i in range(0, len(self.network.nodes)):
				self.selected_map_vars = []
				print("Iterazione numero ",i)
				for n in range(0,i):
					self.evidences[self.network.nodes[n].var.name] = self.network.nodes[n].var.domain[0]
				for m in range(0,int(len(self.network.nodes)/2)):
					self.selected_map_vars.append(self.network.nodes[m].var.name)
				start_time = time.time()
				self.network.map(self.evidences,self.selected_map_vars,True)
				x_axis.append(len(self.evidences)) 
				y_axis.append(time.time() - start_time)

				self.network = load_net(self.path)
			self.plot_data(x_axis,y_axis,"Evidences","Execution Time", "MAP")
      
		elif main_choice == '7':
			#MAP Evidences
			x_axis = []
			y_axis = []
			self.evidences.clear()
      
			
			for i in range(2, len(self.network.nodes)):
				self.selected_map_vars = []
				print("Iterazione numero ",i)
				for m in range(1,i):
					self.selected_map_vars.append(self.network.nodes[m])
				start_time = time.time()
				self.network.map(self.evidences,self.selected_map_vars, True)
				x_axis.append(len(self.selected_map_vars)) 
				y_axis.append(time.time() - start_time)

				self.network = load_net(self.path)

			self.plot_data(x_axis,y_axis,"Map Vars","Execution Time","MAP VARS")




if __name__ == "__main__":
	Menu()