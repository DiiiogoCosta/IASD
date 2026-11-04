from solutionCopy import CRSproblem

prob = CRSproblem()

#----------- exemplo 1
with open("ex1.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
assert prob.result(((10,0), None, None, None), (1, 11, 2)) == ((10,0), (11, 2), None, None)
assert prob.goal_test(((10,0),(11,2),(3,4),(0,0))) == True
assert prob.path_cost(3, ((10,0), None, None, None), (2, 3, 4), ((0,0), None, (3,4), None)) == 12
assert prob.cost(((10,0),(11,2),(3,4),(0,0))) == 20


#----------- exemplo 2
with open("ex2.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
assert prob.result(((3,0), None, None), (2, 0, 0)) == ((3,0), None, (0,0))
assert prob.goal_test(((3,0),(6,0),(0,0))) == True
path_cost_2 = prob.path_cost(3, ((3,0), None, None), (2, 0, 0), ((3,0), None, (0,0)))
assert path_cost_2 == 9, f"esperava 9, deu {path_cost_2}"
assert prob.cost([(3,0),(6,0),(0,0)]) == 21


#----------- exemplo 3
with open("ex3.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
assert prob.result(((0,0), None, None), (2, 5, 0)) == ((0,0), None, (5,0))
assert prob.goal_test(((0,0),(8,0),(5,0))) == True
assert prob.path_cost(3, ((0,0), None, None), (2, 5, 0), ((0,0), None, (5,0))) == 21
assert prob.cost(((0,0),(8,0),(5,0))) == 29

