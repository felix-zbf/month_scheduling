from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat
from Tkinter import *
import math

m = ConcreteModel()


m.x = Var(bounds=(0,6),initialize=0)
m.y = Var(bounds=(0,4))
m.z = Var()

def _ASU1_start(m):
    return m.z == m.x + 5
m.ASU1_start = Constraint(rule=_ASU1_start)


def _ASU3_start(m):
    if m.z.value >= 3:
	return m.y == 0
    return m.y == 1
m.ASU3_start = Constraint(rule=_ASU3_start)

m.obj = Objective(expr= m.z + m.y, sense=maximize)


ss = SolverFactory('scipampl')
ss.solve(m, tee=True, keepfiles=False)

m.pprint()

print m.y.value
print m.z.value
