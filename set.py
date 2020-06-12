from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat

model7 = Block()

model7.solver.options['mipgap'] = 0.01
