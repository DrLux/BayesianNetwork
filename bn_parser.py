from bayesian_network import *


'''a = BayesVar('a',['young','adult','old'])
s = BayesVar('s',['m','f']) 
e = BayesVar('e',['high','uni'])
o = BayesVar('o',['emp','self']) 
r = BayesVar('r',['small','big']) 
t = BayesVar('t',['car','train','other']) 

netVariables = [a,s,e,o,r,t]

cpt_a = dict()
cpt_a['young'] = 0.3
cpt_a['adult'] = 0.5
cpt_a['old'] = 0.2
node_a = BayesNode(a,[],cpt_a)

cpt_s = dict()
cpt_s['m'] = 0.6
cpt_s['f'] = 0.4
node_s = BayesNode(s,[],cpt_s)

cpt_eas = dict()
cpt_eas['high','young','m'] = 0.75
cpt_eas['high','adult','m'] = 0.72
cpt_eas['high','old','m'] = 0.88
cpt_eas['high','young','f'] = 0.64
cpt_eas['high','adult','f'] = 0.7
cpt_eas['high','old','f'] = 0.9
cpt_eas['uni','young','m'] = 0.25
cpt_eas['uni','adult','m'] = 0.28
cpt_eas['uni','old','m'] = 0.12
cpt_eas['uni','young','f'] = 0.36
cpt_eas['uni','adult','f'] = 0.3
cpt_eas['uni','old','f'] = 0.1
eas = BayesNode(e,[a,s],cpt_eas)

cpt_oe = dict()
cpt_oe['emp','high'] = 0.96
cpt_oe['emp','uni'] = 0.92
cpt_oe['self','high'] = 0.04
cpt_oe['self','uni'] = 0.08
oe = BayesNode(o,[e],cpt_oe)

cpt_re = dict()
cpt_re['small','high'] = 0.25
cpt_re['small','uni'] = 0.2
cpt_re['big','high'] = 0.75
cpt_re['big','uni'] = 0.08
re = BayesNode(r,[e],cpt_re)


cpt_tor = dict()
cpt_tor['car','emp','small'] = 0.48
cpt_tor['car','self','small'] = 0.56
cpt_tor['car','emp','big'] = 0.58
cpt_tor['car','self','big'] = 0.70

cpt_tor['train','emp','small'] = 0.42
cpt_tor['train','self','small'] = 0.36
cpt_tor['train','emp','big'] = 0.24
cpt_tor['train','self','big'] = 0.21

cpt_tor['other','emp','small'] = 0.10
cpt_tor['other','self','small'] = 0.08
cpt_tor['other','emp','big'] = 0.18
cpt_tor['other','self','big'] = 0.09
tor = BayesNode(t,[o,r],cpt_tor)

netNodes = [node_a, node_s, eas, oe, re, tor]

bn = BayesNet(netVariables,netNodes)'''

'''
b = BayesVar('b',['t','f'])
e = BayesVar('e',['t','f']) 
a = BayesVar('a',['t','f'])
j = BayesVar('j',['t','f']) 
m = BayesVar('m',['t','f']) 

netVariables = [b,e,a,j,m]

cpt_b = dict()
#cpt_b[b] = []
cpt_b['t'] = 0.01
cpt_b['f'] = 0.99
node_b = BayesNode(b,[],cpt_b)

cpt_e = dict()
#cpt_e[e] = []
cpt_e['t'] = 0.02
cpt_e['f'] = 0.98
node_e = BayesNode(e,[],cpt_e)

cpt_aeb = dict()
#cpt_aeb[a] = [e,b]
cpt_aeb['t','t','t'] = 0.95
cpt_aeb['t','t','f'] = 0.94
cpt_aeb['t','f','t'] = 0.29
cpt_aeb['t','f','f'] = 0.001
cpt_aeb['f','t','t'] = 0.05
cpt_aeb['f','t','f'] = 0.06
cpt_aeb['f','f','t'] = 0.71
cpt_aeb['f','f','f'] = 0.999
aeb = BayesNode(a,[e,b],cpt_aeb)


cpt_ja = dict()
#cpt_ja[j] = [a]
cpt_ja['t','t'] = 0.9
cpt_ja['t','f'] = 0.05
cpt_ja['f','t'] = 0.1
cpt_ja['f','f'] = 0.95
ja = BayesNode(j,[a],cpt_ja)

cpt_ma = dict()
#cpt_ma[m] = [a]
cpt_ma['t','t'] = 0.7
cpt_ma['t','f'] = 0.01
cpt_ma['f','t'] = 0.3
cpt_ma['f','f'] = 0.99
ma = BayesNode(m,[a],cpt_ma)



netNodes = [node_b, node_e, aeb, ja, ma]

bn = BayesNet(netVariables,netNodes)
'''

b = BayesVar('b',['t','f'])
e = BayesVar('e',['t','f']) 
a = BayesVar('a',['t','f'])
j = BayesVar('j',['t','f']) 
m = BayesVar('m',['t','f']) 

netVariables = [b,e,a,j,m]

cpt_b = CPT()
cpt_b.add(Assignment(['b'],['t'],0.01))
cpt_b.add(Assignment(['b'],['f'],0.99))
node_b = BayesNode(b,[],cpt_b)

cpt_e = CPT()
cpt_e.add(Assignment(['e'],['t'],0.02))
cpt_e.add(Assignment(['e'],['f'],0.98))
node_e = BayesNode(e,[],cpt_e)


cpt_aeb = CPT()
cpt_aeb.add(Assignment(['a','b','e'],['t','t','t'],0.95))
cpt_aeb.add(Assignment(['a','b','e'],['t','t','f'],0.94))
cpt_aeb.add(Assignment(['a','b','e'],['t','f','t'],0.29))
cpt_aeb.add(Assignment(['a','b','e'],['t','f','f'],0.001))
cpt_aeb.add(Assignment(['a','b','e'],['f','t','t'],0.05))
cpt_aeb.add(Assignment(['a','b','e'],['f','t','f'],0.06))
cpt_aeb.add(Assignment(['a','b','e'],['f','f','t'],0.71))
cpt_aeb.add(Assignment(['a','b','e'],['f','f','f'],0.999))
aeb = BayesNode(a,['e','b'],cpt_aeb)


cpt_ja = CPT()
cpt_ja.add(Assignment(['j','a'],['t','t'],0.9))
cpt_ja.add(Assignment(['j','a'],['t','f'],0.05))
cpt_ja.add(Assignment(['j','a'],['f','t'],0.1))
cpt_ja.add(Assignment(['j','a'],['f','f'],0.95))
ja = BayesNode(j,['a'],cpt_ja)

cpt_ma = CPT()
cpt_ma.add(Assignment(['m','a'],['t','t'],0.7))
cpt_ma.add(Assignment(['m','a'],['t','f'],0.01))
cpt_ma.add(Assignment(['m','a'],['f','t'],0.3))
cpt_ma.add(Assignment(['m','a'],['f','f'],0.99))
ma = BayesNode(m,['a'],cpt_ma)

netNodes = [node_b, node_e, aeb, ja, ma]

bn = BayesNet(netVariables,netNodes)