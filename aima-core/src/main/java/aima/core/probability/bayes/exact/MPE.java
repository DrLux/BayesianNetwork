package aima.core.probability.bayes.exact;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import aima.core.probability.CategoricalDistribution;
import aima.core.probability.Factor;
import aima.core.probability.RandomVariable;
import aima.core.probability.bayes.BayesInference;
import aima.core.probability.bayes.BayesianNetwork;
import aima.core.probability.bayes.ConditionalProbabilityDistribution;
import aima.core.probability.bayes.FiniteNode;
import aima.core.probability.bayes.Node;
import aima.core.probability.domain.Domain;
import aima.core.probability.proposition.AssignmentProposition;
import aima.core.probability.proposition.ConjunctiveProposition;
import aima.core.probability.proposition.Proposition;
import aima.core.probability.util.ProbUtil;
import aima.core.probability.util.ProbabilityTable;
import java.lang.reflect.Array;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 *
 * @author sorre
 */

public class MPE{
    BayesianNetwork network = null;
    
    public MPE(final BayesianNetwork network) {
        this.network = network;
    }
    
    public void calculateMPE(List<AssignmentProposition> evidences){
        evidences.get(0).getValue();
        Map<RandomVariable, Object> evidencesVar = new HashMap<>();
        for (AssignmentProposition prop : evidences){
            evidencesVar.put(prop.getTermVariable(), prop.getValue());
        }

        List<RandomVariable> topoligicalVar = new ArrayList<RandomVariable>(this.network.getVariablesInTopologicalOrder());
        Collections.reverse(topoligicalVar); //processo le variabili dal basso verso l' alto
        for (RandomVariable var : topoligicalVar){
            processNode(var, evidencesVar);//processNode(var, evidencesVar);
        }
        
    }
         
    //la cpt è implementata in CPT.java
    public void processNode(RandomVariable var, Map<RandomVariable, Object> evidencesVar){
        System.out.println("var: "+ var.getName());
        ConditionalProbabilityDistribution cpt = this.network.getNode(var).getCPD(); //get cpt from variable
        List<RandomVariable> factors = new ArrayList(cpt.getFor());
        
        for (RandomVariable factor : factors) {
            //fare tutti gli esperimentini su che metodi puoi chiamare da qui in poi
            System.out.println("factor: "+factor+" "+this.network.getNode(var).getCPD().getData().);
        }       
        
        //if (evidencesVar.containsKey(var))
    }
         
}

