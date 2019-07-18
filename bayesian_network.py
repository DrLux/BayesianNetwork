from bayesian_node import *

class BayesNet:
  def __init__(self, variables, nodes, dict_nodes):
    self.nodes = nodes # node
    self.variables = variables #string
    self.dict_nodes = dict_nodes # string -> node

  def remove_node(self, node):
    self.nodes.remove(node)
    self.variables.remove(node.var)
    del self.dict_nodes[node.var.name]

  def print(self):
    for node in self.nodes:
      node.print()

  def get_all_nodes_var(self):
    return list(self.dict_nodes.keys())


  def mpe(self,evidences,is_bench = False):
    factors = []
    for node in reversed(self.nodes):
      factors.append(self.make_factor(node.cpt,evidences))
      if node.var.name not in evidences: 
        factors = self.max_out_factor(node, factors)
        
    result = factors[0]
    for i in range (1, len(factors)):
      result = result.pointwise_product(factors[i])
    
    if not is_bench:
      self.retropropagate_assignments(result, evidences)



  def retropropagate_assignments(self,cpt_last_node, evidences):
    history = CPT()
    history.vars = [cpt_last_node.best_value()]
    parents_ass = []  
    
    for name,ass in evidences.items():
      history.cpt[name] = ass
    
    for i in range(0,len(self.nodes)):
      #print(self.nodes[i].print())
      if (i == 0):
        best_ass = self.nodes[i].cpt.best_ass_for_node_var(None,None,self.nodes[i].var.name)
        history.cpt[self.nodes[i].var.name] = best_ass
      else:
        if self.nodes[i].parents:
          for p in self.nodes[i].parents:
            parents_ass.append(history.cpt[p])
          best_ass = self.nodes[i].cpt.best_ass_for_node_var(self.nodes[i].parents, parents_ass,self.nodes[i].var.name)
        else:#se non ho i parent lo faccio sul nodo precedente
          best_ass = self.nodes[i].cpt.best_ass_for_node_var(self.nodes[i-1].var.name,history.cpt[self.nodes[i-1].var.name],self.nodes[i].var.name)
        history.cpt[self.nodes[i].var.name] = best_ass
        parents_ass.clear()
    
    print("Evidences: ", evidences)
    history.print("Best assignments")

  def map(self,evidences,mapvars, is_bench = False):
    map_vars = set()
    for mv in mapvars:
      if mv not in evidences:
        map_vars.add(mv) 

    factors = []
    for node in reversed(self.nodes):
      factors.append(self.make_factor(node.cpt,evidences))
      if node.var.name not in evidences and node.var.name not in map_vars:
        factors = self.sum_out_factor(node.var.name, factors) 
        
    for node in reversed(self.nodes):
      if node.var.name not in evidences and node.var.name in map_vars:
        factors = self.max_out_factor(node, factors)
      else:
        self.nodes.remove(node)
    
    result = factors[0]
    for i in range (1, len(factors)):
      result = result.pointwise_product(factors[i])

    if not is_bench:
      print("Map var: ",map_vars)
      self.retropropagate_assignments(result,evidences)
      

  def make_factor(self,cpt,evidences):
    factor = cpt
    ass_to_remove = set()
    for e in evidences:
      if e in cpt.vars:
        for ass,val in cpt.cpt.items():
          if ass[cpt.vars.index(e)] != evidences[e]:
            ass_to_remove.add(ass)
    for a in ass_to_remove:
      del factor.cpt[a]   
    return factor


  def sum_out_factor(self,var_to_remove, factors):
    result = []
    new_factor = None
    for f in factors:
      if var_to_remove in f.vars:
        if new_factor:
          new_factor = new_factor.pointwise_product(f)
        else:
          new_factor = f
      else:
        result.append(f)
    new_factor = new_factor.sum_out(var_to_remove)
    result.append(new_factor)
    return result


  def max_out_factor(self,node_to_remove, factors):
    result = []
    new_factor = None
    for f in factors:
      if node_to_remove.var.name in f.vars:
        if new_factor:
          new_factor = new_factor.pointwise_product(f)
        else:
          new_factor = f
      else:
        result.append(f)

    node_to_remove.cpt = new_factor
    new_factor = new_factor.max_out(node_to_remove.var.name)
    result.append(new_factor)
    node_to_remove.parents = new_factor.vars
    return result