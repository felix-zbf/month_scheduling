from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat

model4 = Block()

model4.SC = RangeSet(1,5)
model4.SC_1 = RangeSet(0,5)
model4.G = Set(initialize=['AIR','GOX','LOX','GAN','LIN','LAR','SLT','GAR'])
model4.S = Set(initialize=['LOX','LIN','LAR'])
model4.C = Set(initialize=['AIRC','GOXC','MPNC','LPNC'])
model4.R = Set(initialize=['M1', 'M2', 'M3'])
model4.TR = Set(initialize=[('M1','M2'), ('M2','M1'), ('M1','M3'), ('M3','M1'), ('M2','M3'), ('M3','M2')])

model4.F = Var(model4.G, model4.SC, within=Reals, bounds=(0,None), initialize=0)
model4.f = Var(model4.R, model4.G, model4.SC, within=Reals, bounds=(0,None), initialize=0)
model4.Y = Var(model4.SC_1, within=Binary, bounds=(0,1), initialize=0)
model4.y = Var(model4.R, model4.SC_1, within=Binary, bounds=(0,1), initialize=0)
model4.Y_GAR = Var(model4.SC, within=Binary, bounds=(0,1), initialize=0)
model4.y_GAR = Var(model4.R, model4.SC, within=Binary, bounds=(0,1), initialize=0)
model4.Q = Var(model4.C, model4.SC, within=Reals, bounds=(0,None), initialize=0)
model4.q = Var(model4.R, model4.C, model4.SC, within=Reals, bounds=(0,None), initialize=0)
model4.lamuda = Var(model4.R, model4.SC, within=Reals, bounds=(0, 1), initialize=0)
model4.Z = Var(model4.TR, model4.SC_1, within=Binary, bounds=(0, 1), initialize=0)
model4.ZZ = Var(model4.SC_1, within=Reals, bounds=(0,None), initialize=0)
model4.w = Var(model4.R, model4.SC_1, within=Reals, bounds=(0,None), initialize=0)
model4.v = Var(model4.R, model4.SC_1, within=Reals, bounds=(0,None), initialize=0)
model4.p = Var(model4.SC_1, within=Binary, bounds=(0, 1), initialize=0)

model4.time =  {0:0, 1:5, 2:5, 3:1, 4:4, 5:15}

def _ASU4_1(m, s):
    return m.F['GOX', s] == sum(m.f[r, 'GOX', s] for r in m.R)
model4.ASU4_1 = Constraint(model4.SC, rule=_ASU4_1)

def _ASU4_2(m, s):
    return m.F['LOX', s] == sum(m.f[r, 'LOX', s] for r in m.R)
model4.ASU4_2 = Constraint(model4.SC, rule=_ASU4_2)

def _ASU4_3(m, s):
    return m.F['GAN', s] == sum(m.f[r, 'GAN', s] for r in m.R)
model4.ASU4_3 = Constraint(model4.SC, rule=_ASU4_3)

def _ASU4_4(m, s):
    return m.F['LIN', s] == sum(m.f[r, 'LIN', s] for r in m.R)
model4.ASU4_4 = Constraint(model4.SC, rule=_ASU4_4)

def _ASU4_5(m, s):
    return m.F['GAR', s] == sum(m.f[r, 'GAR', s] for r in m.R)
model4.ASU4_5 = Constraint(model4.SC, rule=_ASU4_5)

def _ASU4_6(m, s):
    return m.F['LAR', s] == sum(m.f[r, 'LAR', s] for r in m.R)
model4.ASU4_6 = Constraint(model4.SC, rule=_ASU4_6)

def _ASU4_7(m, s):
    return m.F['AIR', s] == sum(m.f[r, 'AIR', s] for r in m.R)
model4.ASU4_7 = Constraint(model4.SC, rule=_ASU4_7)

def _ASU4_8(m, s):
    return m.Q['AIRC', s] == sum(m.q[r, 'AIRC', s] for r in m.R) 
model4.ASU4_8 = Constraint(model4.SC, rule=_ASU4_8)

def _ASU4_9(m, s):
    return sum(m.y[r, s] for r in m.R) == 1
model4.ASU4_9 = Constraint(model4.SC, rule=_ASU4_9)

def _ASU4_10(m, s):
    return m.Y[s] == m.y['M2', s] + m.y['M3', s]
model4.ASU4_10 = Constraint(model4.SC, rule=_ASU4_10)

def _ASU4_11(m, s):
    return m.Y_GAR[s] == sum(m.y_GAR[r, s] for r in m.R)
model4.ASU4_11 = Constraint(model4.SC, rule=_ASU4_11)

def _ASU4_13(m, s):
    return m.Q['GOXC', s] == 0.175 * m.F['GOX', s]
model4.ASU4_13 = Constraint(model4.SC, rule=_ASU4_13)

def _ASU4_14(m, s):
    return m.ZZ[s] == sum(m.w[r, s] for r in m.R)
model4.ASU4_14 = Constraint(model4.SC_1, rule=_ASU4_14)

def _ASU4_15(m, s):
    return m.ZZ[s-1] == sum(m.v[r, s] for r in m.R)
model4.ASU4_15 = Constraint(model4.SC, rule=_ASU4_15)


#Mode1
def _Mode1(m, i, s):
    return m.f['M1', i, s] == 0 * m.y['M1', s]
model4.Mode1 = Constraint(model4.G, model4.SC, rule=_Mode1)

def _Mode2(m, s):
    return m.w['M1', s] == m.v['M1', s] + m.time[s] * m.y['M1', s]
model4.Mode2 = Constraint(model4.SC, rule=_Mode2)

def _Mode3(m, s):
    return m.w['M1', s] <= 100 * m.y['M1', s]
model4.Mode3 = Constraint(model4.SC, rule=_Mode3)

def _Mode4(m, s):
    return m.v['M1', s] <= 100 * m.y['M1', s]
model4.Mode4 = Constraint(model4.SC, rule=_Mode4)

#Mode2&Mode3
def _Mode_1(m, r, s):
    if r != 'M1':
        return m.f[r, 'AIR', s] == 4.22 * m.f[r, 'GOX', s] - 3.9 * m.f[r, 'LIN', s] + 30500 * m.y[r, s]
    return Constraint.Skip
model4.Mode_1 = Constraint(model4.R, model4.SC, rule=_Mode_1)

def _Mode_2(m, r, s):
    if r != 'M1':
        return 0.0063 * m.f[r, 'AIR', s] + 425 * m.y[r, s] == m.f[r, 'LOX', s] + m.f[r, 'LIN', s]
    return Constraint.Skip
model4.Mode_2 = Constraint(model4.R, model4.SC, rule=_Mode_2)

def _Mode_3(m, r, s):
    if r != 'M1':
        return 0.6 * m.f[r, 'AIR', s] - 2689.57 * m.y[r, s] == m.f[r, 'GAN', s] + m.f[r, 'LIN', s]
    return Constraint.Skip
model4.Mode_3 = Constraint(model4.R, model4.SC, rule=_Mode_3)

def _Mode_4(m, r, s):
    if r != 'M1':
        return 0.009463 * m.f[r, 'AIR', s] + 294 * m.y[r, s] == m.f[r, 'LAR', s]
    return Constraint.Skip
model4.Mode_4 = Constraint(model4.R, model4.SC, rule=_Mode_4)

def _Mode_5(m, r, s):
    if r != 'M1':
        return m.f[r, 'GAR', s] >= 500 * m.y_GAR[r, s]
    return Constraint.Skip
model4.Mode_5 = Constraint(model4.R, model4.SC, rule=_Mode_5)

def _Mode_6(m, r, s):
    if r != 'M1':
        return m.f[r, 'GAR', s] <= 900 * m.y_GAR[r, s]
    return Constraint.Skip
model4.Mode_6 = Constraint(model4.R, model4.SC, rule=_Mode_6)

def _Mode_7(m, r, s):
    if r != 'M1':
        return m.y_GAR[r, s] <= m.y[r, s]
    return Constraint.Skip
model4.Mode_7 = Constraint(model4.R, model4.SC, rule=_Mode_7)

def _Mode_8(m, r, s):
    if r != 'M1':
        return m.w[r, s] == 0
    return Constraint.Skip
model4.Mode_8 = Constraint(model4.R, model4.SC, rule=_Mode_8)

def _Mode_9(m, r, s):
    if r != 'M1':
        return m.v[r, s] <= 100 * m.y[r, s]
    return Constraint.Skip
model4.Mode_9 = Constraint(model4.R, model4.SC, rule=_Mode_9)


#Mode2
def _Mode2_1(m, s):
    return m.f['M2', 'LIN', s] >= 0 * m.y['M2', s]
model4.Mode2_1 = Constraint(model4.SC, rule=_Mode2_1)

def _Mode2_2(m, s):
    return m.f['M2', 'GOX', s] >= 26000 * m.y['M2', s]
model4.Mode2_2 = Constraint(model4.SC, rule=_Mode2_2)

def _Mode2_3(m, s):
    return m.f['M2', 'GOX', s] <= 28000 * m.y['M2', s]
model4.Mode2_3 = Constraint(model4.SC, rule=_Mode2_3)

def _Mode2_4(m, s):
    return m.f['M2', 'AIR', s] == m.lamuda['M2', s] * (120000 - 148660) + 148660 * m.y['M2', s]
model4.Mode2_4 = Constraint(model4.SC, rule=_Mode2_4)

def _Mode2_5(m, s):
    return m.q['M2', 'AIRC', s] == m.lamuda['M2', s] * (120000 * 0.337 * 1.06 - 148660 * 0.337 * 1.02) + 148660 * 0.337 * 1.02 * m.y['M2', s]
model4.Mode2_5 = Constraint(model4.SC, rule=_Mode2_5)

def _Mode2_6(m, s):
    return m.lamuda['M2', s] <= m.y['M2', s]
model4.Mode2_6 = Constraint(model4.SC, rule=_Mode2_6)

def _Mode2_7(m, s):
    return m.f['M2', 'LIN', s] <= 1300 * m.y['M2', s]
model4.Mode2_7 = Constraint(model4.SC, rule=_Mode2_7)

#Mode3
def _Mode3_1(m, s):
    return m.f['M3', 'LIN', s] >= 0 * m.y['M3', s]
model4.Mode3_1 = Constraint(model4.SC, rule=_Mode3_1)

def _Mode3_2(m, s):
    return m.f['M3', 'LIN', s] <= 1300 * m.y['M3', s]
model4.Mode3_2 = Constraint(model4.SC, rule=_Mode3_2)

def _Mode3_3(m, s):
    return m.f['M3', 'GOX', s] >= 28000 * m.y['M3', s]
model4.Mode3_3 = Constraint(model4.SC, rule=_Mode3_3)

def _Mode3_4(m, s):
    return m.f['M3', 'GOX', s] <= 33000 * m.y['M3', s]
model4.Mode3_4 = Constraint(model4.SC, rule=_Mode3_4)

model4.G_AIR = Set(initialize=['AIR'])
model4.V = Set(initialize=['V1', 'V2'])
model4.f_compressor = Var(model4.R, model4.V, model4.G_AIR, model4.SC, within=Reals, bounds=(0,None), initialize=0)
model4.q_compressor = Var(model4.R, model4.V, model4.G_AIR, model4.SC, within=Reals, bounds=(0,None), initialize=0)
model4.lamuda_compressor = Var(model4.R, model4.V, model4.SC, within=Reals, bounds=(0, 1), initialize=0)
model4.y_compressor = Var(model4.R, model4.V, model4.SC, within=Binary, bounds=(0, 1), initialize=0)

def _Mode3_5(m, s):
    return m.f['M3', 'AIR', s] == sum(m.f_compressor['M3', v, 'AIR', s] for v in m.V)
model4.Mode3_5 = Constraint(model4.SC, rule=_Mode3_5)

def _Mode3_5_1(m, s):
    return m.f_compressor['M3', 'V1', 'AIR', s] == m.lamuda_compressor['M3', 'V1', s] * (148660 - 152030) + 152030 * m.y_compressor['M3', 'V1', s]
model4.Mode3_5_1 = Constraint(model4.SC, rule=_Mode3_5_1)

def _Mode3_5_2(m, s):
    return m.f_compressor['M3', 'V2', 'AIR', s] == m.lamuda_compressor['M3', 'V2', s] * (152030 - 170000) + 170000 * m.y_compressor['M3', 'V2', s]
model4.Mode3_5_2 = Constraint(model4.SC, rule=_Mode3_5_2)

def _Mode3_6(m, s):
    return m.q['M3', 'AIRC', s] == sum(m.q_compressor['M3', v, 'AIR', s] for v in m.V)
model4.Mode3_6 = Constraint(model4.SC, rule=_Mode3_6)

def _Mode3_6_1(m, s):
    return m.q_compressor['M3', 'V1', 'AIR', s] == m.lamuda_compressor['M3', 'V1', s] * (148660 * 0.337 * 1.02 - 152030 * 0.377 * 1) + 152030 * 0.377 * 1 * m.y_compressor['M3', 'V1', s]
model4.Mode3_6_1 = Constraint(model4.SC, rule=_Mode3_6_1)

def _Mode3_6_2(m, s):
    return m.q_compressor['M3', 'V2', 'AIR', s] == m.lamuda_compressor['M3', 'V2', s] * (152030 * 0.377 * 1 - 170000 * 0.377 * 1.05) + 170000 * 0.377 * 1.05 * m.y_compressor['M3', 'V2', s]
model4.Mode3_6_2 = Constraint(model4.SC, rule=_Mode3_6_2)

def _Mode3_7(m, s):
    return m.lamuda['M3', s] == sum(m.lamuda_compressor['M3', v, s] for v in m.V)
model4.Mode3_7 = Constraint(model4.SC, rule=_Mode3_7)

def _Mode3_8(m, s):
    return m.y['M3', s] == sum(m.y_compressor['M3', v, s] for v in m.V)
model4.Mode3_8 = Constraint(model4.SC, rule=_Mode3_8)

def _Mode3_9(m, s):
    return m.lamuda['M3', s] <= m.y['M3', s]
model4.Mode3_9 = Constraint(model4.SC, rule=_Mode3_9)

def _Mode3_10(m, v, s):
    return m.lamuda_compressor['M3', v, s] <= m.y_compressor['M3', v, s]
model4.Mode3_10 = Constraint(model4.V, model4.SC, rule=_Mode3_10)

#switch
def _Switch1(m, s):
    return m.Z['M2', 'M1', s] + m.Z['M3', 'M1', s] - m.Z['M1', 'M2', s] - m.Z['M1', 'M3', s] == m.y['M1', s] - m.y['M1', s-1]
model4.Switch1 = Constraint(model4.SC, rule= _Switch1)

def _Switch2(m, s):
    return m.Z['M1', 'M2', s] + m.Z['M3', 'M2', s] - m.Z['M2', 'M1', s] - m.Z['M2', 'M3', s] == m.y['M2', s] - m.y['M2', s-1]
model4.Switch2 = Constraint(model4.SC, rule= _Switch2)

def _Switch3(m, s):
    return m.Z['M1', 'M3', s] + m.Z['M2', 'M3', s] - m.Z['M3', 'M1', s] - m.Z['M3', 'M2', s] == m.y['M3', s] - m.y['M3', s-1]
model4.Switch3 = Constraint(model4.SC, rule= _Switch3)

def _Switch4(m, s):
    return m.Z['M1', 'M3', s] == 0
model4.Switch4 = Constraint(model4.SC, rule= _Switch4)


model4.Startup = Var(model4.SC, within=Reals, bounds=(0,None), initialize=0)
model4.Trans = Var(model4.SC, within=Reals, bounds=(0,None), initialize=0)

#def _Switch6(m, s):
#    return m.Startup[s] == m.Z['M1', 'M2', s] * (20000 * 0.4499 + 2300 / 804 * 1.143 * 1400)
#model4.Switch6 = Constraint(model4.SC, rule= _Switch6)

def _Switch7(m, s):
   return m.Trans[s] == m.Z['M2', 'M3', s] * 200
model4.Switch7 = Constraint(model4.SC, rule= _Switch7)

def _init1(m):
    return m.y['M1', 0] == 0
model4.init1 = Constraint(rule= _init1)

def _init2(m):
    return m.y['M2', 0] == 1
model4.init2 = Constraint(rule= _init2)

def _init3(m):
    return m.y['M3', 0] == 0
model4.init3 = Constraint(rule= _init3)

#def _init4(m):
#    return m.zz['M1', 0] == 0
#model4.init4 = Constraint(rule= _init4)


def _Cost_1(m, s):
    return m.ZZ[s-1] >= 3 * m.p[s] 
model4.Cost_1 = Constraint(model4.SC, rule= _Cost_1)

def _Cost_2(m, s):
    return m.ZZ[s-1] <= 3 * (1 - m.p[s]) + 10000*  m.p[s] - 10e-5 * (1 - m.p[s])
model4.Cost_2 = Constraint(model4.SC, rule= _Cost_2)

model4.zp = Var(model4.SC_1, within=Reals, bounds=(0,None), initialize=0)

def _Cost_3(m, s):
    if s == 1:
        return m.Startup[s] == m.Z['M1', 'M2', s] * 224037
    return m.Startup[s] == m.zp[s] * (224037 - 2000) + m.Z['M1', 'M2', s] * 2000
model4.Cost_3 = Constraint(model4.SC, rule= _Cost_3)

def _Cost_4(m, s):
    return m.zp[s] - m.Z['M1', 'M2', s] <= 0
model4.Cost_4 = Constraint(model4.SC, rule= _Cost_4)

def _Cost_5(m, s):
    return m.zp[s] - m.p[s] <= 0
model4.Cost_5 = Constraint(model4.SC, rule= _Cost_5)

def _Cost_6(m, s):
    return m.p[s] + m.Z['M1', 'M2', s] - m.zp[s] <= 1
model4.Cost_6 = Constraint(model4.SC, rule= _Cost_6)




