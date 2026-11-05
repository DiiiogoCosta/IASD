from solution import CRSproblem

prob = CRSproblem()

#----------- exemplo 1
with open("ex1.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
sol = prob.solve()
assert prob.check(sol) == True
assert sol == [(10,0),(11,2),(3,4),(0,0)]
assert prob.result(((10,0), None, None, None), (1, 11, 2)) == ((10,0), (11, 2), None, None)
assert prob.goal_test(((10,0),(11,2),(3,4),(0,0))) == True
assert prob.path_cost(3, ((10,0), None, None, None), (2, 3, 4), ((0,0), None, (3,4), None)) == 12
assert prob.cost(sol) == 20


#----------- exemplo 2
with open("ex2.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
sol = prob.solve()
assert prob.check(sol) == True
assert sol == [(3,0),(6,0),(0,0)]
assert prob.result(((3,0), None, None), (2, 0, 0)) == ((3,0), None, (0,0))
assert prob.goal_test(((3,0),(6,0),(0,0))) == True
assert prob.goal_test(((3,0),None,(0,0))) == False
path_cost_2 = prob.path_cost(3, ((3,0), None, None), (2, 0, 0), ((3,0), None, (0,0)))
assert path_cost_2 == 9, f"esperava 9, deu {path_cost_2}"
assert prob.cost([(3,0),(6,0),(0,0)]) == 21


#----------- exemplo 3
with open("ex3.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
sol = prob.solve()
assert prob.check(sol) == True
assert sol == [(0,0),(8,0),(5,0)]
assert prob.result(((0,0), None, None), (2, 5, 0)) == ((0,0), None, (5,0))
assert prob.goal_test(((0,0),(8,0),(5,0))) == True
assert prob.path_cost(3, ((0,0), None, None), (2, 5, 0), ((0,0), None, (5,0))) == 21
assert prob.cost(((0,0),(8,0),(5,0))) == 29


#----------- exemplo 4
with open("ex4.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
sol = prob.solve()
assert prob.check(sol) == True
assert prob.cost(sol) == 28
#assert sol == [(0,0),(0,2),(2,2),(5,0),(0,5)], f"expected [(0,0),(0,2),(2,2),(5,0),(0,5)] got {sol}"
assert prob.result(((0,0), None, None, None, None), (2, 2, 2)) == ((0,0), None, (2,2), None, None)
assert prob.goal_test(((0,0),(0,2),(2,2),(5,0),(0,5))) == True
assert prob.path_cost(4, ((0,0), None, None, None, None), (2, 2, 2), ((0,0), None, (2,2), None, None)) == 12



#----------- exemplo 5
with open("ex5.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
sol = prob.solve()
assert prob.check(sol) == True
#assert sol == [(6,0),(1,0),(1,4),(4,0),(7,5),(6,5)]
assert prob.result(((6,0), None, None, None, None, None), (2, 1, 4)) == ((6,0), None, (1,4), None, None, None)
assert prob.goal_test(((6,0),(1,0),(1,4),(4,0),(7,5),(6,5))) == True
assert prob.path_cost(12, ((6,0), None, None, None, None, None), (2, 1, 4), ((6,0), None, (1,4), None, None, None)) == 18
assert prob.cost(sol) == 63


#----------- exemplo 6
with open("ex6.dat") as fh:
    prob.load(fh)

print("tasks:", prob.tasks)
sol = prob.solve()
assert prob.check(sol) == True
#assert sol == [(0,0),(11,0),(1,4),(7,0),(3,0),(4,0),(5,2)]
assert prob.result(((0,0), None, None, None, None, None, None), (2, 1, 4)) == ((0,0), None, (1,4), None, None, None, None)
assert prob.goal_test(((0,0),(11,0),(1,4),(7,0),(3,0),(4,0),(5,2))) == True
assert prob.path_cost(6, ((0,0), None, None, None, None, None, None), (2, 1, 4), ((0,0), None, (1,4), None, None, None, None)) == 12
assert prob.cost(sol) == 59

