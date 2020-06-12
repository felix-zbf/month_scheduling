from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat

model6 = Block()

model6.SC = RangeSet(1,5)
model6.Q = RangeSet(1,3)
model6.L = Set(initialize=['LGOX','LGAN'])
model6.V = Set(initialize=['VLOX','VLIN'])

model6.F_V = Var(model6.V, model6.SC, within=Reals, bounds=(0,None), initialize=0)
model6.F = Var(model6.V, model6.Q, model6.SC, within=Reals, bounds=(0,None), initialize=0)
model6.Y = Var(model6.V, model6.Q, model6.SC, within=Binary, bounds=(0,1), initialize=0)
model6.Z = Var(model6.SC, within=Binary, bounds=(0,1), initialize=0)

def _Vap_1(m, s):
    return m.F['VLOX', 1, s] ==  30000 * m.Y['VLOX', 1, s]
model6.Vap_1 = Constraint(model6.SC, rule=_Vap_1)

def _Vap_2(m, s):
    return m.F['VLOX', 2, s] ==  20000 * m.Y['VLOX', 2, s]
model6.Vap_2 = Constraint(model6.SC, rule=_Vap_2)

def _Vap_3(m, s):
    return m.F['VLOX', 3, s] ==  20000 * m.Y['VLOX', 3, s]
model6.Vap_3 = Constraint(model6.SC, rule=_Vap_3)

def _Vap_4(m, s):
    return m.F['VLIN', 1, s] ==  30000 * m.Y['VLIN', 1, s]
model6.Vap_4 = Constraint(model6.SC, rule=_Vap_4)

def _Vap_5(m, s):
    return m.F['VLIN', 2, s] ==  20000 * m.Y['VLIN', 2, s]
model6.Vap_5 = Constraint(model6.SC, rule=_Vap_5)

def _Vap_6(m, s):
    return m.F['VLIN', 3, s] == 0
model6.Vap_6 = Constraint(model6.SC, rule=_Vap_6)

def _Vap_7(m, s):
    return m.F_V['VLOX', s] == sum(m.F['VLOX', i, s] for i in model6.Q)
model6.Vap_7 = Constraint(model6.SC, rule=_Vap_7)

def _Vap_8(m, s):
    return m.F_V['VLIN', s] == sum(m.F['VLIN', i, s] for i in model6.Q)
model6.Vap_8 = Constraint(model6.SC, rule=_Vap_8)

def _Vap_9(m, s):
    return m.Y['VLIN', 3, s] == 0
model6.Vap_9 = Constraint(model6.SC, rule=_Vap_9)




