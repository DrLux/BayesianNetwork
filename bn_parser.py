from bayesian_network import *

#data una variabile e una lista di variabili restituisce l' index-esimo valore del dominio nella var trovata nella lista delle var
def get_var_domain_in_index(target_var,index,netVariables):
	for var in netVariables:
		if target_var[0] == var.name:
			return [var.domain[index]]

def get_var_from_name(target_var,netVariables):
	for var in netVariables:
		if target_var == var.name:
			return var

def load_net(path):
	with open(path, 'r') as file:
		lineList = file.readlines()
		netVariables = []
		netNodes = []
		for i in range(len(lineList)): #itera sulle righe del file
			if 'variable' in lineList[i]:

				#parsing del nome della variabile
				name_var = lineList[i].split()[1] #la seconda parola della riga contenente "variable" è il nome della variabile
				
				next_line = lineList[i+1] 
				domain = next_line[next_line.index('{')+1:next_line.index('}')]
				domain = domain.replace(',', '').split()
				assert(len(domain) == int(next_line.split()[3]))
				
				#creazione oggetto
				netVariables.append(BayesVar(name_var,domain))
			if 'probability' in lineList[i]:
				
				#inizializzazione .split(',')
				line = lineList[i].replace(',', '').split()

				#parsing del nome della variabile
				name_var = [line[2]] #la 3 parola contiene il nome della variabile
				parents_name = line[4:line.index(')')] #se ci sono parents le trovo dal 4 token fino alla chiusura parentesi

				#parsing della CPT
				cpt = CPT()
				vars_Ass = name_var + parents_name
				new_i = i + 1
				next_line = lineList[new_i]
				while next_line[0] != "}":
					if (next_line[2] == 't'): # se la riga inizia con "table" si tratta di una variabile singola
						next_line = next_line.replace(',', '')
						next_line = next_line.replace(';', '').split()
						for new_j in range(1,len(next_line)): #per ogni parola nella riga
							ass = get_var_domain_in_index(name_var,new_j-1,netVariables)
							cpt.add(Assignment(vars_Ass,ass,float(next_line[new_j])))
					else: #cpt_eas.add(Assignment(['e','a','s'],['high','young','m'],0.75))
						next_line = next_line.replace(',', '')
						next_line = next_line.replace(';', '')
						ass = next_line[next_line.index('(')+1:next_line.index(')')].split()
						val = next_line[next_line.index(')')+1:].split() 
						val = list(map(float, val)) #cast da string a float
						for x in range(len(val)):
							cpt.add(Assignment(vars_Ass,get_var_domain_in_index(name_var,x,netVariables) + ass,val[x]))

					new_i += 1
					next_line = lineList[new_i]
				netNodes.append(BayesNode(get_var_from_name(name_var[0],netVariables),parents_name,cpt))
										
		bn = BayesNet(netVariables,netNodes)
		file.close()
	return bn
