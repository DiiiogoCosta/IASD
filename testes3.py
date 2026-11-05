import time, search
from solution import CRSproblem

exemplos = {"ex1.dat": 20, "ex2.dat": 21, "ex3.dat": 29, "ex4.dat": 28}
algoritmos =[search.breadth_first_tree_search,
           search.breadth_first_graph_search,
           search.depth_first_graph_search,
           search.uniform_cost_search,
           search.iterative_deepening_search,]

for alg in algoritmos:
    print()
    for ficheiro, otimo in exemplos.items():
        prob = CRSproblem()
        with open(ficheiro) as fh:
            prob.load(fh)

        ip = search.InstrumentedProblem(prob)
        t0 = time.time()
        node = alg(ip)
        dt = time.time() - t0

        sol = list(node.state)
        custo = prob.cost(sol)
        print(f"{ficheiro} {alg.__name__:30} estados={ip.states:6} "
              f"t={dt:.2f}s custo={custo} ótimo? {custo == otimo}")
