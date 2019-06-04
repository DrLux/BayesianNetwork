package aima.gui.demo.agent;

import aima.core.agent.Agent;
import aima.core.agent.EnvironmentListener;
import aima.core.agent.impl.DynamicPercept;
import aima.core.agent.impl.SimpleEnvironmentView;
import aima.core.environment.map.*;
import aima.core.search.framework.SearchForActions;
import aima.core.search.framework.qsearch.GraphSearch;
import aima.core.search.informed.AStarSearch;

/**
 * Demonstrates how different kinds of search algorithms perform in a route finding scenario.
 * @author Ruediger Lunde
 */
public class MapAgentDemo {
    public static void main(String[] args) {
        ExtendableMap map = new ExtendableMap();
        SimplifiedRoadMapOfPartOfRomania.initMap(map);
        MapEnvironment env = new MapEnvironment(map);
        EnvironmentListener<Object, Object> envView = new SimpleEnvironmentView();
        env.addEnvironmentListener(envView);

        String agentLoc = SimplifiedRoadMapOfPartOfRomania.ARAD;
        String destination = SimplifiedRoadMapOfPartOfRomania.BUCHAREST;
        SearchForActions<String, MoveToAction> search = null;
        //search = new DepthFirstSearch<>(new GraphSearch<>());
        //search = new UniformCostSearch<>(new TreeSearch<>());
        //search = new UniformCostSearch<>(new GraphSearch<>());
        search = new AStarSearch<>(new GraphSearch<>(), MapFunctions.createSLDHeuristicFunction(destination, map));
        Agent<DynamicPercept, MoveToAction> agent;
        //agent = new SimpleMapAgent(map, search, destination);
        agent = new MapAgent(map, search, destination);

        env.addAgent(agent, agentLoc);
        env.stepUntilDone();
        envView.notify(search.getMetrics().toString());
    }
}
