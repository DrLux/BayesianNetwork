package aima.core.probability;

import aima.core.probability.example.*;
import aima.core.probability.bayes.*;
import aima.core.probability.bayes.exact.*;
import aima.core.probability.bayes.impl.*;
import aima.core.probability.bayes.impl.*;
import aima.core.probability.bayes.model.*;
import aima.core.probability.proposition.*;
import java.util.List;

/**
 *
 * @author Luca Sorrentino & Daniele Pautasso
 */
public class IaLab {
    public static void main(String [ ] args){
        System.out.println("hello world");
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
        FiniteBayesModel model = new FiniteBayesModel(earthyNet, new EliminationAsk());
        List<RandomVariable> nodes = earthyNet.getVariablesInTopologicalOrder();
        
        AssignmentProposition jonhcall = customAssignment(nodes, "JohnCalls", true);
        AssignmentProposition marycall = customAssignment(nodes, "MaryCalls", true);
        AssignmentProposition burglary = customAssignment(nodes, "Burglary", true);
        ConjunctiveProposition johnANDmary = new ConjunctiveProposition(marycall, jonhcall);
        
        System.out.println("The posterior distribution for Burglary given jonhcall and marycall is "+ model.posterior(burglary,johnANDmary));
    }
}
