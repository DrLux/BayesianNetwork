from bn_parser import *

# sito dove scaricare le reti: http://www.bnlearn.com/bnrepository/


network = load_net('survey.bif')

#network.print()

evidences = dict()
evidences['A'] = 'adult' 
#evidences['S'] = 'M' 
evidences['E'] = 'high' 
#evidences['O'] = 'emp' 
#evidences['R'] = 'big' 
evidences['T'] = 'train' 

network.mpe(evidences)
