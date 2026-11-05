import search
from solution import CRSproblem

def carregar(nome):
    p = CRSproblem()
    with open(nome) as fh:
        p.load(fh)
    return p

problemas = [carregar(f) for f in ["ex1.dat", "ex2.dat", "ex3.dat", "ex4.dat"]]

search.compare_searchers(
    problems=problemas,
    header=["Algoritmo", "ex1", "ex2", "ex3", "ex4"],
    searchers=[
        search.breadth_first_tree_search,
        search.breadth_first_graph_search,
        search.depth_first_graph_search,
        search.uniform_cost_search,
        search.iterative_deepening_search,
    ],
)