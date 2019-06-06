package aima.core.probability;

import aima.core.probability.example.*;
import aima.core.probability.bayes.*;
import aima.core.probability.bayes.exact.*;
import aima.core.probability.bayes.impl.*;
import aima.core.probability.bayes.impl.*;
import aima.core.probability.bayes.model.*;
import aima.core.probability.proposition.*;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Luca Sorrentino & Daniele Pautasso
 */
public class IaLab {
    public static void main(String [ ] args){
        IaLab ialab = new IaLab();
        ialab.doStuff();
    }
    
    public RandomVariable getVariable(List<RandomVariable> nodes, String name){
        RandomVariable ret = null;
        for(RandomVariable node : nodes) {
            if(node.getName().equals(name))
                ret = node;
        }
        return ret;
    }
    

    /*/public BayesianNetwork loadNetwork(String name){
        URL pathFile = IaLab_Bayesian_network.class.getResource(name);
        File file = new File(pathFile.getFile());
        BifReader br = new BifReader();
        BayesianNetwork network = br.readBIF(file);
        return network;
    }*/
    
    public AssignmentProposition customAssignment(List<RandomVariable> nodes, String variableName, Object value){
        RandomVariable variable = getVariable(nodes, variableName);
        AssignmentProposition assignment = new AssignmentProposition(variable, true);
        return assignment;
    }
    
    /*
        Burglary
        Earthquake
        Alarm
        MaryCalls
        JohnCalls
    */
    public void doStuff(){
        BayesianNetwork earthyNet = BayesNetExampleFactory.constructBurglaryAlarmNetwork();
        List<RandomVariable> nodes = earthyNet.getVariablesInTopologicalOrder();
        MPE mpe = new MPE(earthyNet);
        
        AssignmentProposition jonhcall = customAssignment(nodes, "JohnCalls", true);
        AssignmentProposition marycall = customAssignment(nodes, "MaryCalls", true);
        AssignmentProposition burglary = customAssignment(nodes, "Burglary", true);
        
        List<AssignmentProposition> evidences = new ArrayList<>();;
        evidences.add(jonhcall);
        evidences.add(marycall);
        
        mpe.calculateMPE(evidences);
        
        //model.mpe(johnANDmary);
    }
}
