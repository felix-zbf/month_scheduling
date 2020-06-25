from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat

model3 = Block()

model3.SC = RangeSet(1,5)
model3.SC_1 = RangeSet(0,5)
model3.G = Set(initialize=['AIR','GOX','LOX','GAN','LIN','LAR','SLT','GAR'])
model3.S = Set(initialize=['LOX','LIN','LAR'])
model3.C = Set(initialize=['AIRC','GOXC','MPNC','LPNC'])
model3.R = Set(initialize=['M1', 'M2', 'M3'])
model3.TR = Set(initialize=[('M1','M2'), ('M2','M1'), ('M1','M3'), ('M3','M1'), ('M2','M3'), ('M3','M2')])

model3.F = Var(model3.G, model3.SC, within=Reals, bounds=(0,None), initialize=0)
model3.f = Var(model3.R, model3.G, model3.SC, within=Reals, bounds=(0,None), initialize=0)
model3.Y = Var(model3.SC_1, within=Binary, bounds=(0,1), initialize=0)
model3.y = Var(model3.R, model3.SC_1, within=Binary, bounds=(0,1), initialize=0)
model3.Y_GAR = Var(model3.SC, within=Binary, bounds=(0,1), initialize=0)
model3.y_GAR = Var(model3.R, model3.SC, within=Binary, bounds=(0,1), initialize=0)
model3.Q = Var(model3.C, model3.SC, within=Reals, bounds=(0,None), initialize=0)
model3.q = Var(model3.R, model3.C, model3.SC, within=Reals, bounds=(0,None), initialize=0)
model3.lamuda = Var(model3.R, model3.SC, within=Reals, bounds=(0, 1), initialize=0)
model3.Z = Var(model3.TR, model3.SC_1, within=Binary, bounds=(0, 1), initialize=0)
model3.ZZ = Var(model3.SC_1,within=Reals, bounds=(0,None), initialize=0)
model3.w = Var(model3.R, model3.SC_1,within=Reals, bounds=(0,None), initialize=0)
model3.v = Var(model3.R, model3.SC_1,within=Reals, bounds=(0,None), initialize=0)
model3.p = Var(model3.SC_1, within=Binary, bounds=(0, 1), initialize=0)

model3.time =  {0:0, 1:5, 2:5, 3:1, 4:4, 5:15}


def _ASU3_1(m, s):
    return m.F['GOX', s] == sum(m.f[r, 'GOX', s] for r in m.R)
model3.ASU3_1 = Constraint(model3.SC, rule=_ASU3_1)

def _ASU3_2(m, s):
    return m.F['LOX', s] == sum(m.f[r, 'LOX', s] for r in m.R)
model3.ASU3_2 = Constraint(model3.SC, rule=_ASU3_2)

def _ASU3_3(m, s):
    return m.F['GAN', s] == sum(m.f[r, 'GAN', s] for r in m.R)
model3.ASU3_3 = Constraint(model3.SC, rule=_ASU3_3)

def _ASU3_4(m, s):
    return m.F['LIN', s] == sum(m.f[r, 'LIN', s] for r in m.R)
model3.ASU3_4 = Constraint(model3.SC, rule=_ASU3_4)

def _ASU3_5(m, s):
    return m.F['GAR', s] == sum(m.f[r, 'GAR', s] for r in m.R)
model3.ASU3_5 = Constraint(model3.SC, rule=_ASU3_5)

def _ASU3_6(m, s):
    return m.F['LAR', s] == sum(m.f[r, 'LAR', s] for r in m.R)
model3.ASU3_6 = Constraint(model3.SC, rule=_ASU3_6)

def _ASU3_7(m, s):
    return m.F['AIR', s] == sum(m.f[r, 'AIR', s] for r in m.R)
model3.ASU3_7 = Constraint(model3.SC, rule=_ASU3_7)

def _ASU3_8(m, s):
    return m.Q['AIRC', s] == sum(m.q[r, 'AIRC', s] for r in m.R) 
model3.ASU3_8 = Constraint(model3.SC, rule=_ASU3_8)

def _ASU3_9(m, s):
    return sum(m.y[r, s] for r in m.R) == 1 
model3.ASU3_9 = Constraint(model3.SC, rule=_ASU3_9)

def _ASU3_10(m, s):
    return m.Y[s] == m.y['M2', s] + m.y['M3', s]
model3.ASU3_10 = Constraint(model3.SC, rule=_ASU3_10)

def _ASU3_11(m, s):
    return m.Y_GAR[s] == sum(m.y_GAR[r, s] for r in m.R)
model3.ASU3_11 = Constraint(model3.SC, rule=_ASU3_11)

def _ASU3_12(m, s):
    return m.ZZ[s] == sum(m.w[r, s] for r in m.R)
model3.ASU3_12 = Constraint(model3.SC_1, rule=_ASU3_12)

def _ASU3_13(m, s):
    return m.ZZ[s-1] == sum(m.v[r, s] for r in m.R)
model3.ASU3_13 = Constraint(model3.SC, rule=_ASU3_13)


#Mode1
def _Mode1(m, i, s):
    return m.f['M1', i, s] == 0 * m.y['M1', s]
model3.Mode1 = Constraint(model3.G, model3.SC, rule=_Mode1)

def _Mode2(m, s):
    return m.w['M1', s] == m.v['M1', s] + m.time[s] * m.y['M1', s]
model3.Mode2 = Constraint(model3.SC, rule=_Mode2)

def _Mode3(m, s):
    return m.w['M1', s] <= 100 * m.y['M1', s]
model3.Mode3 = Constraint(model3.SC, rule=_Mode3)

def _Mode4(m, s):
    return m.v['M1', s] <= 100 * m.y['M1', s]
model3.Mode4 = Constraint(model3.SC, rule=_Mode4)


#Mode2&Mode3
def _Mode_1(m, r, s):
    if r != 'M1':
        return m.f[r, 'AIR', s] == 4.384 * m.f[r, 'GOX', s] - 4.06 * m.f[r, 'LIN', s] + 13370 * m.y[r, s]
    return Constraint.Skip
model3.Mode_1 = Constraint(model3.R, model3.SC, rule=_Mode_1)

def _Mode_2(m, r, s):
    if r != 'M1':
        return 0.009 * m.f[r, 'AIR', s] + 1370 * m.y[r, s] == m.f[r, 'LOX', s] + m.f[r, 'LIN', s]
    return Constraint.Skip
model3.Mode_2 = Constraint(model3.R, model3.SC, rule=_Mode_2)

def _Mode_3(m, r, s):
    if r != 'M1':
        return 0.43 * m.f[r, 'AIR', s] - 2180 * m.y[r, s] == m.f[r, 'GAN', s] + m.f[r, 'LIN', s]
    return Constraint.Skip
model3.Mode_3 = Constraint(model3.R, model3.SC, rule=_Mode_3)

def _Mode_4(m, r, s):
    if r != 'M1':
        return 0.0073 * m.f[r, 'AIR', s] + 137 * m.y[r, s] == m.f[r, 'LAR', s]
    return Constraint.Skip
model3.Mode_4 = Constraint(model3.R, model3.SC, rule=_Mode_4)

def _Mode_5(m, r, s):
    if r != 'M1':
        return m.f[r, 'GAR', s] >= 500 * m.y_GAR[r, s]
    return Constraint.Skip
model3.Mode_5 = Constraint(model3.R, model3.SC, rule=_Mode_5)

def _Mode_6(m, r, s):
    if r != 'M1':
        return m.f[r, 'GAR', s] <= 900 * m.y_GAR[r, s]
    return Constraint.Skip
model3.Mode_6 = Constraint(model3.R, model3.SC, rule=_Mode_6)

def _Mode_7(m, r, s):
    if r != 'M1':
        return m.y_GAR[r, s] <= m.y[r, s]
    return Constraint.Skip
model3.Mode_7 = Constraint(model3.R, model3.SC, rule=_Mode_7)

def _Mode_8(m, r, s):
    if r != 'M1':
        return m.w[r, s] == 0
    return Constraint.Skip
model3.Mode_8 = Constraint(model3.R, model3.SC, rule=_Mode_8)

def _Mode_9(m, r, s):
    if r != 'M1':
        return m.v[r, s] <= 100 * m.y[r, s]
    return Constraint.Skip
model3.Mode_9 = Constraint(model3.R, model3.SC, rule=_Mode_9)

#Mode2
def _Mode2_1(m, s):
    return m.f['M2', 'LIN', s] >= 0 * m.y['M2', s]
model3.Mode2_1 = Constraint(model3.SC, rule=_Mode2_1)

def _Mode2_2(m, s):
    return m.f['M2', 'GOX', s] >= 16000 * m.y['M2', s]
model3.Mode2_2 = Constraint(model3.SC, rule=_Mode2_2)

def _Mode2_3(m, s):
    return m.f['M2', 'GOX', s] <= 19000 * m.y['M2', s]
model3.Mode2_3 = Constraint(model3.SC, rule=_Mode2_3)

def _Mode2_4(m, s):
    return m.f['M2', 'AIR', s] == m.lamuda['M2', s] * (80000 - 92282) + 92282 * m.y['M2', s]
model3.Mode2_4 = Constraint(model3.SC, rule=_Mode2_4)

def _Mode2_5(m, s):
    return m.q['M2', 'AIRC', s] == m.lamuda['M2', s] * (80000 * 0.455 * 1.1 - 92282 * 0.455 * 1.02) + 92282 * 0.455 * 1.03 * m.y['M2', s]
model3.Mode2_5 = Constraint(model3.SC, rule=_Mode2_5)

def _Mode2_6(m, s):
    return m.lamuda['M2', s] <= m.y['M2', s]
model3.Mode2_6 = Constraint(model3.SC, rule=_Mode2_6)

def _Mode2_7(m, s):
    return m.f['M2', 'LIN', s] <= 2400 * m.y['M2', s]
model3.Mode2_7 = Constraint(model3.SC, rule=_Mode2_7)

#Mode3
def _Mode3_1(m, s):
    return m.f['M3', 'LIN', s] >= 0 * m.y['M3', s]
model3.Mode3_1 = Constraint(model3.SC, rule=_Mode3_1)

def _Mode3_2(m, s):
    return m.f['M3', 'LIN', s] <= 2400 * m.y['M3', s]
model3.Mode3_2 = Constraint(model3.SC, rule=_Mode3_2)

def _Mode3_3(m, s):
    return m.f['M3', 'GOX', s] >= 19000 * m.y['M3', s]
model3.Mode3_3 = Constraint(model3.SC, rule=_Mode3_3)

def _Mode3_4(m, s):
    return m.f['M3', 'GOX', s] <= 24000 * m.y['M3', s]
model3.Mode3_4 = Constraint(model3.SC, rule=_Mode3_4)

model3.G_AIR = Set(initialize=['AIR'])
model3.V = Set(initialize=['V1', 'V2'])
model3.f_compressor = Var(model3.R, model3.V, model3.G_AIR, model3.SC, within=Reals, bounds=(0,None), initialize=0)
model3.q_compressor = Var(model3.R, model3.V, model3.G_AIR, model3.SC, within=Reals, bounds=(0,None), initialize=0)
model3.lamuda_compressor = Var(model3.R, model3.V, model3.SC, within=Reals, bounds=(0, 1), initialize=0)
model3.y_compressor = Var(model3.R, model3.V, model3.SC, within=Binary, bounds=(0, 1), initialize=0)

def _Mode3_5(m, s):
    return m.f['M3', 'AIR', s] == sum(m.f_compressor['M3', v, 'AIR', s] for v in m.V)
model3.Mode3_5 = Constraint(model3.SC, rule=_Mode3_5)

def _Mode3_5_1(m, s):
    return m.f_compressor['M3', 'V1', 'AIR', s] == m.lamuda_compressor['M3', 'V1', s] * (92282 - 101050) + 101050 * m.y_compressor['M3', 'V1', s]
model3.Mode3_5_1 = Constraint(model3.SC, rule=_Mode3_5_1)

def _Mode3_5_2(m, s):
    return m.f_compressor['M3', 'V2', 'AIR', s] == m.lamuda_compressor['M3', 'V2', s] * (101050 - 110000) + 110000 * m.y_compressor['M3', 'V2', s]
model3.Mode3_5_2 = Constraint(model3.SC, rule=_Mode3_5_2)

def _Mode3_6(m, s):
    return m.q['M3', 'AIRC', s] == sum(m.q_compressor['M3', v, 'AIR', s] for v in m.V)
model3.Mode3_6 = Constraint(model3.SC, rule=_Mode3_6)

def _Mode3_6_1(m, s):
    return m.q_compressor['M3', 'V1', 'AIR', s] == m.lamuda_compressor['M3', 'V1', s] * (92282 * 0.455 * 1.03 - 101050 * 0.455 * 1) + 101050 * 0.455 * 1 * m.y_compressor['M3', 'V1', s]
model3.Mode3_6_1 = Constraint(model3.SC, rule=_Mode3_6_1)

def _Mode3_6_2(m, s):
    return m.q_compressor['M3', 'V2', 'AIR', s] == m.lamuda_compressor['M3', 'V2', s] * (101050 * 0.455 * 1 - 110000 * 0.455 * 1.05) + 110000 * 0.455 * 1.05 * m.y_compressor['M3', 'V2', s]
model3.Mode3_6_2 = Constraint(model3.SC, rule=_Mode3_6_2)

def _Mode3_7(m, s):
    return m.lamuda['M3', s] == sum(m.lamuda_compressor['M3', v, s] for v in m.V)
model3.Mode3_7 = Constraint(model3.SC, rule=_Mode3_7)

def _Mode3_8(m, s):
    return m.y['M3', s] == sum(m.y_compressor['M3', v, s] for v in m.V)
model3.Mode3_8 = Constraint(model3.SC, rule=_Mode3_8)

def _Mode3_9(m, s):
    return m.lamuda['M3', s] <= m.y['M3', s]
model3.Mode3_9 = Constraint(model3.SC, rule=_Mode3_9)

def _Mode3_10(m, v, s):
    return m.lamuda_compressor['M3', v, s] <= m.y_compressor['M3', v, s]
model3.Mode3_10 = Constraint(model3.V, model3.SC, rule=_Mode3_10)

#switch
def _Switch1(m, s):
    return m.Z['M2', 'M1', s] + m.Z['M3', 'M1', s] - m.Z['M1', 'M2', s] - m.Z['M1', 'M3', s] == m.y['M1', s] - m.y['M1', s-1]
model3.Switch1 = Constraint(model3.SC, rule= _Switch1)

def _Switch2(m, s):
    return m.Z['M1', 'M2', s] + m.Z['M3', 'M2', s] - m.Z['M2', 'M1', s] - m.Z['M2', 'M3', s] == m.y['M2', s] - m.y['M2', s-1]
model3.Switch2 = Constraint(model3.SC, rule= _Switch2)

def _Switch3(m, s):
    return m.Z['M1', 'M3', s] + m.Z['M2', 'M3', s] - m.Z['M3', 'M1', s] - m.Z['M3', 'M2', s] == m.y['M3', s] - m.y['M3', s-1]
model3.Switch3 = Constraint(model3.SC, rule= _Switch3)

def _Switch4(m, s):
    return m.Z['M1', 'M3', s] == 0
model3.Switch4 = Constraint(model3.SC, rule= _Switch4)


model3.Startup = Var(model3.SC, within=Reals, bounds=(0,None), initialize=0)
model3.Trans = Var(model3.SC, within=Reals, bounds=(0,None), initialize=0)

#def _Switch6(m, s):
#    return m.Startup[s] == m.Z['M1', 'M2', s] * (20000 * 0.4499 + 2300 / 804 * 1.143 * 1400)
#model3.Switch6 = Constraint(model3.SC, rule= _Switch6)

def _Switch7(m, s):
    return m.Trans[s] == m.Z['M2', 'M3', s] * 200
model3.Switch7 = Constraint(model3.SC, rule= _Switch7)

def _init1(m):
    return m.y['M1', 0] == 0
model3.init1 = Constraint(rule= _init1)

def _init2(m):
    return m.y['M2', 0] == 1
model3.init2 = Constraint(rule= _init2)

def _init3(m):
    return m.y['M3', 0] == 0
model3.init3 = Constraint(rule= _init3)

#def _init4(m):
#    return m.zz['M1', 0] == 0
#model3.init4 = Constraint(rule= _init4)


def _Cost_1(m, s):
    return m.ZZ[s-1] >= 3 * m.p[s]  
model3.Cost_1 = Constraint(model3.SC, rule= _Cost_1)

def _Cost_2(m, s):
    return m.ZZ[s-1] <= 3 * (1 - m.p[s]) + 10000*  m.p[s-1] - 10e-5 * (1 - m.p[s])
model3.Cost_2 = Constraint(model3.SC, rule= _Cost_2)

model3.zp = Var(model3.SC_1, within=Reals, bounds=(0,None), initialize=0)

def _Cost_3(m, s):
    if s == 1:
        return m.Startup[s] == m.Z['M1', 'M2', s] * 133072
    return m.Startup[s] == m.zp[s] * (133072 - 2000) + m.Z['M1', 'M2', s] * 2000
model3.Cost_3 = Constraint(model3.SC, rule= _Cost_3)

def _Cost_4(m, s):
    return m.zp[s] - m.Z['M1', 'M2', s] <= 0
model3.Cost_4 = Constraint(model3.SC, rule= _Cost_4)

def _Cost_5(m, s):
    return m.zp[s] - m.p[s] <= 0
model3.Cost_5 = Constraint(model3.SC, rule= _Cost_5)

def _Cost_6(m, s):
    return m.p[s] + m.Z['M1', 'M2', s] - m.zp[s] <= 1
model3.Cost_6 = Constraint(model3.SC, rule= _Cost_6)





