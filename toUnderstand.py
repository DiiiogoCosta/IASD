import search

p = search.InstrumentedProblem(
    search.GraphProblem('Arad', 'Bucharest', search.romania_map))

for alg in [search.breadth_first_graph_search, search.uniform_cost_search, 
            search.depth_first_graph_search, search.depth_limited_search, search.iterative_deepening_search]:
    node = alg(p)
    print(alg.__name__, node.solution(), node.path_cost)
    print(p.succs, p.goal_tests, p.states)

search.compare_graph_searchers()