from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat

model1 = Block()

model1.SC = RangeSet(1,5)
model1.SC_1 = RangeSet(0,5)
model1.G = Set(initialize=['AIR','GOX','LOX','GAN','LIN','LAR','SLT','GAR'])
model1.S = Set(initialize=['LOX','LIN','LAR'])
model1.C = Set(initialize=['AIRC','GOXC','MPNC','LPNC'])
model1.R = Set(initialize=['M1', 'M2', 'M3'])
model1.TR = Set(initialize=[('M1','M2'), ('M2','M1'), ('M1','M3'), ('M3','M1'), ('M2','M3'), ('M3','M2')])

model1.F = Var(model1.G, model1.SC, within=Reals, bounds=(0,None), initialize=0)
model1.f = Var(model1.R, model1.G, model1.SC, within=Reals, bounds=(0,None), initialize=0)
model1.Y = Var(model1.SC_1, within=Binary, bounds=(0,1), initialize=0)
model1.y = Var(model1.R, model1.SC_1, within=Binary, bounds=(0,1), initialize=0)
model1.Y_GAR = Var(model1.SC, within=Binary, bounds=(0,1), initialize=0)
model1.y_GAR = Var(model1.R, model1.SC, within=Binary, bounds=(0,1), initialize=0)
model1.Q = Var(model1.C, model1.SC, within=Reals, bounds=(0,None), initialize=0)
model1.q = Var(model1.R, model1.C, model1.SC, within=Reals, bounds=(0,None), initialize=0)
model1.lamuda = Var(model1.R, model1.SC, within=Reals, bounds=(0, 1), initialize=0)
model1.Z = Var(model1.TR, model1.SC_1, within=Binary, bounds=(0, 1), initialize=0)
model1.ZZ = Var(model1.SC_1, within=Reals, bounds=(0,None), initialize=0)
model1.w = Var(model1.R, model1.SC_1, within=Reals, bounds=(0,None), initialize=0)
model1.v = Var(model1.R, model1.SC_1, within=Reals, bounds=(0,None), initialize=0)
model1.p = Var(model1.SC_1, within=Binary, bounds=(0, 1), initialize=0)

model1.time =  {0:0, 1:5, 2:5, 3:1, 4:4, 5:15}

def _ASU1_1(m, s):
    return m.F['GOX', s] == sum(m.f[r, 'GOX', s] for r in m.R)
model1.ASU1_1 = Constraint(model1.SC, rule=_ASU1_1)

def _ASU1_2(m, s):
    return m.F['LOX', s] == sum(m.f[r, 'LOX', s] for r in m.R)
model1.ASU1_2 = Constraint(model1.SC, rule=_ASU1_2)

def _ASU1_3(m, s):
    return m.F['GAN', s] == sum(m.f[r, 'GAN', s] for r in m.R)
model1.ASU1_3 = Constraint(model1.SC, rule=_ASU1_3)

def _ASU1_4(m, s):
    return m.F['LIN', s] == sum(m.f[r, 'LIN', s] for r in m.R)
model1.ASU1_4 = Constraint(model1.SC, rule=_ASU1_4)

def _ASU1_5(m, s):
    return m.F['GAR', s] == sum(m.f[r, 'GAR', s] for r in m.R)
model1.ASU1_5 = Constraint(model1.SC, rule=_ASU1_5)

def _ASU1_6(m, s):
    return m.F['LAR', s] == sum(m.f[r, 'LAR', s] for r in m.R)
model1.ASU1_6 = Constraint(model1.SC, rule=_ASU1_6)

def _ASU1_7(m, s):
    return m.F['AIR', s] == sum(m.f[r, 'AIR', s] for r in m.R)
model1.ASU1_7 = Constraint(model1.SC, rule=_ASU1_7)

def _ASU1_8(m, s):
    return m.Q['AIRC', s] == sum(m.q[r, 'AIRC', s] for r in m.R)
model1.ASU1_8 = Constraint(model1.SC, rule=_ASU1_8)

def _ASU1_9(m, s):
    return sum(m.y[r, s] for r in m.R) == 1
model1.ASU1_9 = Constraint(model1.SC, rule=_ASU1_9)

def _ASU1_10(m, s):
    return m.Y[s] == m.y['M2', s] + m.y['M3', s]
model1.ASU1_10 = Constraint(model1.SC, rule=_ASU1_10)

def _ASU1_11(m, s):
    return m.Y_GAR[s] == sum(m.y_GAR[r, s] for r in m.R)
model1.ASU1_11 = Constraint(model1.SC, rule=_ASU1_11)

def _ASU1_13(m, s):
    return m.Q['GOXC', s] == 0.187 * m.F['GOX', s]
model1.ASU1_13 = Constraint(model1.SC, rule=_ASU1_13)

def _ASU1_14(m, s):
    return m.ZZ[s] == sum(m.w[r, s] for r in m.R)
model1.ASU1_14 = Constraint(model1.SC_1, rule=_ASU1_14)

def _ASU1_15(m, s):
    return m.ZZ[s-1] == sum(m.v[r, s] for r in m.R)
model1.ASU1_15 = Constraint(model1.SC, rule=_ASU1_15)


#Mode1
def _Mode1(m, i, s):
    return m.f['M1', i, s] == 0 * m.y['M1', s]
model1.Mode1 = Constraint(model1.G, model1.SC, rule=_Mode1)

def _Mode2(m, s):
    return m.w['M1', s] == m.v['M1', s] + m.time[s] * m.y['M1', s]
model1.Mode2 = Constraint(model1.SC, rule=_Mode2)

def _Mode3(m, s):
    return m.w['M1', s] <= 100 * m.y['M1', s]
model1.Mode3 = Constraint(model1.SC, rule=_Mode3)

def _Mode4(m, s):
    return m.v['M1', s] <= 100 * m.y['M1', s]
model1.Mode4 = Constraint(model1.SC, rule=_Mode4)

#Mode2&Mode3
def _Mode_1(m, r, s):
    if r != 'M1':
        return m.f[r, 'AIR', s] == 4.45 * m.f[r, 'GOX', s] - 4.12 * m.f[r, 'LIN', s] + 19000 * m.y[r, s]
    return Constraint.Skip
model1.Mode_1 = Constraint(model1.R, model1.SC, rule=_Mode_1)

def _Mode_2(m, r, s):
    if r != 'M1':
        return 0.009 * m.f[r, 'AIR', s] + 420 * m.y[r, s] == m.f[r, 'LOX', s] + m.f[r, 'LIN', s]
    return Constraint.Skip
model1.Mode_2 = Constraint(model1.R, model1.SC, rule=_Mode_2)

def _Mode_3(m, r, s):
    if r != 'M1':
        return 0.4607 * m.f[r, 'AIR', s] - 5050 * m.y[r, s] == m.f[r, 'GAN', s] + m.f[r, 'LIN', s]
    return Constraint.Skip
model1.Mode_3 = Constraint(model1.R, model1.SC, rule=_Mode_3)

def _Mode_4(m, r, s):
    if r != 'M1':
        return 0.0074 * m.f[r, 'AIR', s] + 50 * m.y[r, s] == m.f[r, 'LAR', s]
    return Constraint.Skip
model1.Mode_4 = Constraint(model1.R, model1.SC, rule=_Mode_4)

def _Mode_5(m, r, s):
    if r != 'M1':
        return m.f[r, 'GAR', s] >= 500 * m.y_GAR[r, s]
    return Constraint.Skip
model1.Mode_5 = Constraint(model1.R, model1.SC, rule=_Mode_5)

def _Mode_6(m, r, s):
    if r != 'M1':
        return m.f[r, 'GAR', s] <= 900 * m.y_GAR[r, s]
    return Constraint.Skip
model1.Mode_6 = Constraint(model1.R, model1.SC, rule=_Mode_6)

def _Mode_7(m, r, s):
    if r != 'M1':
        return m.y_GAR[r, s] <= m.y[r, s]
    return Constraint.Skip
model1.Mode_7 = Constraint(model1.R, model1.SC, rule=_Mode_7)

def _Mode_8(m, r, s):
    if r != 'M1':
        return m.w[r, s] == 0
    return Constraint.Skip
model1.Mode_8 = Constraint(model1.R, model1.SC, rule=_Mode_8)

def _Mode_9(m, r, s):
    if r != 'M1':
        return m.v[r, s] <= 100 * m.y[r, s]
    return Constraint.Skip
model1.Mode_9 = Constraint(model1.R, model1.SC, rule=_Mode_9)


#Mode2
def _Mode2_1(m, s):
    return m.f['M2', 'LIN', s] >= 0 * m.y['M2', s]
model1.Mode2_1 = Constraint(model1.SC, rule=_Mode2_1)

def _Mode2_2(m, s):
    return m.f['M2', 'GOX', s] >= 17000 * m.y['M2', s]
model1.Mode2_2 = Constraint(model1.SC, rule=_Mode2_2)

def _Mode2_3(m, s):
    return m.f['M2', 'GOX', s] <= 22000 * m.y['M2', s]
model1.Mode2_3 = Constraint(model1.SC, rule=_Mode2_3)

def _Mode2_4(m, s):
    return m.f['M2', 'AIR', s] == m.lamuda['M2', s] * (90000 - 108000) + 108000 * m.y['M2', s]
model1.Mode2_4 = Constraint(model1.SC, rule=_Mode2_4)

def _Mode2_5(m, s):
    return m.q['M2', 'AIRC', s] == m.lamuda['M2', s] * (42990 - 46224) + 46224 * m.y['M2', s]
model1.Mode2_5 = Constraint(model1.SC, rule=_Mode2_5)

def _Mode2_6(m, s):
    return m.lamuda['M2', s] <= m.y['M2', s]
model1.Mode2_6 = Constraint(model1.SC, rule=_Mode2_6)

def _Mode2_7(m, s):
    return m.f['M2', 'LIN', s] <= 1250 * m.y['M2', s]
model1.Mode2_7 = Constraint(model1.SC, rule=_Mode2_7)



#Mode3
def _Mode3_1(m, s):
    return m.f['M3', 'LIN', s] >= 0 * m.y['M3', s]
model1.Mode3_1 = Constraint(model1.SC, rule=_Mode3_1)

def _Mode3_2(m, s):
    return m.f['M3', 'LIN', s] <= 1250 * m.y['M3', s]
model1.Mode3_2 = Constraint(model1.SC, rule=_Mode3_2)

def _Mode3_3(m, s):
    return m.f['M3', 'GOX', s] >= 17000 * m.y['M3', s]
model1.Mode3_3 = Constraint(model1.SC, rule=_Mode3_3)

def _Mode3_4(m, s):
    return m.f['M3', 'GOX', s] <= 22000 * m.y['M3', s]
model1.Mode3_4 = Constraint(model1.SC, rule=_Mode3_4)

model1.G_AIR = Set(initialize=['AIR'])
model1.V = Set(initialize=['V1', 'V2'])
model1.f_compressor = Var(model1.R, model1.V, model1.G_AIR, model1.SC, within=Reals, bounds=(0,None), initialize=0)
model1.q_compressor = Var(model1.R, model1.V, model1.G_AIR, model1.SC, within=Reals, bounds=(0,None), initialize=0)
model1.lamuda_compressor = Var(model1.R, model1.V, model1.SC, within=Reals, bounds=(0, 1), initialize=0)
model1.y_compressor = Var(model1.R, model1.V, model1.SC, within=Binary, bounds=(0, 1), initialize=0)

def _Mode3_5(m, s):
    return m.f['M3', 'AIR', s] == sum(m.f_compressor['M3', v, 'AIR', s] for v in m.V)
model1.Mode3_5 = Constraint(model1.SC, rule=_Mode3_5)

def _Mode3_5_1(m, s):
    return m.f_compressor['M3', 'V1', 'AIR', s] == m.lamuda_compressor['M3', 'V1', s] * (108000 - 112450) + 112450 * m.y_compressor['M3', 'V1', s]
model1.Mode3_5_1 = Constraint(model1.SC, rule=_Mode3_5_1)

def _Mode3_5_2(m, s):
    return m.f_compressor['M3', 'V2', 'AIR', s] == m.lamuda_compressor['M3', 'V2', s] * (112450 - 120000) + 120000 *  m.y_compressor['M3', 'V2', s]
model1.Mode3_5_2 = Constraint(model1.SC, rule=_Mode3_5_2)

def _Mode3_6(m, s):
    return m.q['M3', 'AIRC', s] == sum(m.q_compressor['M3', v, 'AIR', s] for v in m.V)
model1.Mode3_6 = Constraint(model1.SC, rule=_Mode3_6)

def _Mode3_6_1(m, s):
    return m.q_compressor['M3', 'V1', 'AIR', s] == m.lamuda_compressor['M3', 'V1', s] * (46224 - 50535) + 50535 * m.y_compressor['M3', 'V1', s]
model1.Mode3_6_1 = Constraint(model1.SC, rule=_Mode3_6_1)

def _Mode3_6_2(m, s):
    return m.q_compressor['M3', 'V2', 'AIR', s] == m.lamuda_compressor['M3', 'V2', s] * (50535 - 51033) + 51033 * m.y_compressor['M3', 'V2', s]
model1.Mode3_6_2 = Constraint(model1.SC, rule=_Mode3_6_2)

def _Mode3_7(m, s):
    return m.lamuda['M3', s] == sum(m.lamuda_compressor['M3', v, s] for v in m.V)
model1.Mode3_7 = Constraint(model1.SC, rule=_Mode3_7)

def _Mode3_8(m, s):
    return m.y['M3', s] == sum(m.y_compressor['M3', v, s] for v in m.V)
model1.Mode3_8 = Constraint(model1.SC, rule=_Mode3_8)

def _Mode3_9(m, s):
    return m.lamuda['M3', s] <= m.y['M3', s]
model1.Mode3_9 = Constraint(model1.SC, rule=_Mode3_9)

def _Mode3_10(m, v, s):
    return m.lamuda_compressor['M3', v, s] <= m.y_compressor['M3', v, s]
model1.Mode3_10 = Constraint(model1.V, model1.SC, rule=_Mode3_10)

#switch
def _Switch1(m, s):
    return m.Z['M2', 'M1', s] + m.Z['M3', 'M1', s] - m.Z['M1', 'M2', s] - m.Z['M1', 'M3', s] == m.y['M1', s] - m.y['M1', s-1]
model1.Switch1 = Constraint(model1.SC, rule= _Switch1)

def _Switch2(m, s):
    return m.Z['M1', 'M2', s] + m.Z['M3', 'M2', s] - m.Z['M2', 'M1', s] - m.Z['M2', 'M3', s] == m.y['M2', s] - m.y['M2', s-1]
model1.Switch2 = Constraint(model1.SC, rule= _Switch2)

def _Switch3(m, s):
    return m.Z['M1', 'M3', s] + m.Z['M2', 'M3', s] - m.Z['M3', 'M1', s] - m.Z['M3', 'M2', s] == m.y['M3', s] - m.y['M3', s-1]
model1.Switch3 = Constraint(model1.SC, rule= _Switch3)

def _Switch4(m, s):
    return m.Z['M1', 'M3', s] == 0
model1.Switch4 = Constraint(model1.SC, rule= _Switch4)


model1.Startup = Var(model1.SC, within=Reals, bounds=(0,None), initialize=0)
model1.Trans = Var(model1.SC, within=Reals, bounds=(0,None), initialize=0)

#def _Switch6(m, s):
#    return m.Startup[s] == m.Z['M1', 'M2', s] * (20000 * 0.4499 + 2300 / 804 * 1.143 * 1400)
#model1.Switch6 = Constraint(model1.SC, rule= _Switch6)

def _Switch7(m, s):
   return m.Trans[s] == m.Z['M2', 'M3', s] * 200
model1.Switch7 = Constraint(model1.SC, rule= _Switch7)

def _init1(m):
    return m.y['M1', 0] == 0
model1.init1 = Constraint(rule= _init1)

def _init2(m):
    return m.y['M2', 0] == 1
model1.init2 = Constraint(rule= _init2)

def _init3(m):
    return m.y['M3', 0] == 0
model1.init3 = Constraint(rule= _init3)

#def _init4(m):
#    return m.zz['M1', 0] == 0
#model1.init4 = Constraint(rule= _init4)


def _Cost_1(m, s):
    return m.ZZ[s-1] >= 3 * m.p[s]
model1.Cost_1 = Constraint(model1.SC, rule= _Cost_1)

def _Cost_2(m, s):
    return m.ZZ[s-1] <= 3 * (1 - m.p[s]) + 10000*  m.p[s] - 10e-5 * (1 - m.p[s])
model1.Cost_2 = Constraint(model1.SC, rule= _Cost_2)

model1.zp = Var(model1.SC_1, within=Reals, bounds=(0,None), initialize=0)

def _Cost_3(m, s):
    if s == 1:
        return m.Startup[s] == m.Z['M1', 'M2', s] * 133072
    return m.Startup[s] == m.zp[s] * (133072 - 2000) + m.Z['M1', 'M2', s] * 2000
model1.Cost_3 = Constraint(model1.SC, rule= _Cost_3)

def _Cost_4(m, s):
    return m.zp[s] - m.Z['M1', 'M2', s] <= 0
model1.Cost_4 = Constraint(model1.SC, rule= _Cost_4)

def _Cost_5(m, s):
    return m.zp[s] - m.p[s] <= 0
model1.Cost_5 = Constraint(model1.SC, rule= _Cost_5)

def _Cost_6(m, s):
    return m.p[s] + m.Z['M1', 'M2', s] - m.zp[s] <= 1
model1.Cost_6 = Constraint(model1.SC, rule= _Cost_6)
