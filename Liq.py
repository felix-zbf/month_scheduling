from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat

model5 = Block()

model5.SC = RangeSet(1,5)
model5.Q = RangeSet(1,2)
model5.L = Set(initialize=['LGOX','LGAN'])
model5.V = Set(initialize=['VLOX','VLIN'])

model5.F_L = Var(model5.L, model5.SC, within=Reals, bounds=(0,None), initialize=0)
model5.F = Var(model5.L, model5.Q, model5.SC, within=Reals, bounds=(0,None), initialize=0)
model5.Y = Var(model5.L, model5.Q, model5.SC, within=Binary, bounds=(0,1), initialize=0)
model5.Z = Var(model5.SC, within=Binary, bounds=(0,1), initialize=0)
model5.cost = Var(model5.SC, within=Reals, bounds=(0,None), initialize=0)
model5.ToLIQ = Var(model5.SC, within=Reals, bounds=(0,None), initialize=0)

def _Liq_1(m, i, s):
    return m.F['LGOX', i, s] == 2400 * m.Y['LGOX', i, s]
model5.Liq_1 = Constraint(model5.Q, model5.SC, rule=_Liq_1)

def _Liq_2(m, i, s):
    return m.F['LGAN', i, s] == 2200 * m.Y['LGAN', i, s]
model5.Liq_2 = Constraint(model5.Q, model5.SC, rule=_Liq_2)

def _Liq_3(m, i, s):
    return sum(m.Y['LGAN', k, s] for k in model5.Q) <= 2 * (1 - m.Y['LGOX', i, s])
model5.Liq_3 = Constraint(model5.Q, model5.SC, rule=_Liq_3)

def _Liq_4(m, s):
    return m.F_L['LGOX', s] == sum(m.F['LGOX', i, s] for i in m.Q)
model5.Liq_4 = Constraint(model5.SC, rule=_Liq_4)

def _Liq_5(m, s):
    return m.F_L['LGAN', s] == sum(m.F['LGAN', i, s] for i in m.Q)
model5.Liq_5 = Constraint(model5.SC, rule=_Liq_5)

def _Liq_6(m, s):
    return m.ToLIQ[s] == 11000 * sum(m.Y['LGOX', i, s] for i in m.Q) + 11000 * sum(m.Y['LGAN', i, s] for i in m.Q)
model5.Liq_6 = Constraint(model5.SC, rule=_Liq_6)

def _pingjun1(m, s):
    return m.Y['LGOX', 1, s] >= m.Y['LGOX', 2, s]
model5.pingjun1 = Constraint(model5.SC, rule=_pingjun1)

def _pingjun2(m, s):
    return m.Y['LGAN', 1, s] >= m.Y['LGAN', 2, s]
model5.pingjun2 = Constraint(model5.SC, rule=_pingjun2)




