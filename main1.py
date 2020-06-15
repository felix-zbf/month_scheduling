from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat
# from Tkinter import *
from ASU1 import model1
from ASU2 import model2
from ASU3 import model3
from ASU4 import model4
from Liq import model5
from Vap import model6
from PSA1 import model7
from PSA2 import model8

import xlrd
import xlwt
import matplotlib.pyplot as plt
import math


m = ConcreteModel()

m.add_component('m1',model1)
m.add_component('m2',model2)
m.add_component('m3',model3)
m.add_component('m4',model4)
m.add_component('m5',model5)
m.add_component('m6',model6)
m.add_component('m7',model7)
m.add_component('m8',model8)


m.SC = RangeSet(1,5)

m.T5 = RangeSet(1,5)

m.G = Set(initialize=['GOX','MPGN','LPGN','GAR'])
m.G_GAN = Set(initialize=['MPGN','LPGN','SLT'])
m.S = Set(initialize=['LOX','LIN','LAR'])

m.F = Var(m.G, m.SC, within=Reals, bounds=(0,None), initialize=0)
m.F_GAN = Var(m.G_GAN, m.T5, m.SC, within=Reals, bounds=(0,None), initialize=0)
m.Y_GAN = Var(m.G_GAN, m.T5, m.SC, within=Binary, bounds=(0,1), initialize=0)
m.Q_GAN1 = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.Q_GAN2 = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.Vent = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.F_L = Var(m.S, m.SC, within=Reals, bounds=(0,None), initialize=0)


demand={}
demand[1,'GOX'] = 68000
demand[1,'MPGN'] = 50000
demand[1,'LPGN'] = 30000
demand[1,'GAR'] = 1300
demand[2,'GOX'] = 43000
demand[2,'MPGN'] = 60000
demand[2,'LPGN'] = 20000
demand[2,'GAR'] = 800
demand[3,'GOX'] = 26000
demand[3,'MPGN'] = 40000
demand[3,'LPGN'] = 10000
demand[3,'GAR'] = 700
demand[4,'GOX'] = 43000
demand[4,'MPGN'] = 60000
demand[4,'LPGN'] = 20000
demand[4,'GAR'] = 800
demand[5,'GOX'] = 68000
demand[5,'MPGN'] = 50000
demand[5,'LPGN'] = 30000
demand[5,'GAR'] = 1300
m.Demand = Param(m.SC, m.G, initialize=demand)
m.Sale = Var(m.S, m.SC, within=Reals, bounds=(0,None), initialize=0)

m.dT = Param(initialize=24)

m.rev_liq = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.rev_gas = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.rev_pipe = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.pro_liq = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.pro_vap = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.cost1 = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.cost2 = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.cost3 = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.cost4 = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.AIRchange = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.punish = Var(m.SC, within=Reals, bounds=(0,None), initialize=0)
m.profit = Var(m.SC, within=Reals, initialize=0)
m.price = Param(initialize=1)


#def _B(m, i, j):
#    return m.Sale[i, j] == m.d2[j, i]
#m.B = Constraint(m.S, m.T1, rule=_B)

def _B1(m, s):
    return m.Sale['LOX', s] <= 5000
m.B1 = Constraint(m.SC, rule=_B1)

def _B2(m, s):
    return m.Sale['LIN', s] <= 5000
m.B2 = Constraint(m.SC, rule=_B2)

def _B3(m, s):
    return m.Sale['LAR', s] <= 5000
m.B3 = Constraint(m.SC, rule=_B3)

#########################

def _GOX_GW1(m, s):
    return m.F['GOX', s] == m.m1.F['GOX', s] + m.m2.F['GOX', s] + m.m3.F['GOX', s] + m.m4.F['GOX', s] + m.m7.F['GOX',s] + m.m8.F['GOX',s]
m.GOX_GW1 = Constraint(m.SC, rule=_GOX_GW1)

def _GOX_GW2(m, s):
    return m.F['GOX', s]  + m.m6.F_V['VLOX', s] - m.m5.F_L['LGOX', s] - m.Vent[s] == m.Demand[s, 'GOX']
m.GOX_GW2 = Constraint(m.SC, rule=_GOX_GW2)

###################

def _GOX_CC1(m, s):
    return m.F_L['LOX', s] == m.m1.F['LOX', s] + m.m2.F['LOX', s] + m.m3.F['LOX', s] + m.m4.F['LOX', s] 
m.GOX_CC1 = Constraint(m.SC, rule=_GOX_CC1)

def _GOX_CC2(m, s):
    return m.F_L['LOX', s]  + m.m5.F_L['LGOX', s] - m.m6.F_V['VLOX', s] == m.Sale['LOX', s]
m.GOX_CC2 = Constraint(m.SC, rule=_GOX_CC2)

#####################

def _yiqu_1(m, s):
    return m.m1.F['GAN', s] + m.m4.F['GAN', s] +  m.m5.ToLIQ[s] == m.F_GAN['MPGN', 1, s]  + m.F_GAN['MPGN', 4, s] + m.F_GAN['MPGN', 5, s]  + m.F_GAN['LPGN', 1, s] + m.F_GAN['SLT', 1, s]
m.yiqu_1 = Constraint(m.SC, rule=_yiqu_1)

def _yiqu_2(m, s):
    return m.Q_GAN1[s] == 0.2 * m.F_GAN['MPGN', 1, s]  + 0.161 * (m.F_GAN['MPGN', 4, s] + m.F_GAN['MPGN', 5, s] ) + 0.108 * m.F_GAN['LPGN', 1, s] 
m.yiqu_2 = Constraint(m.SC, rule=_yiqu_2)

def _yiqu_3(m, i, s):
    return m.F_GAN['MPGN', i, s] >= 16000 * m.Y_GAN['MPGN', i, s]
m.yiqu_3 = Constraint(m.T5, m.SC, rule=_yiqu_3)

def _yiqu_4(m, i, s):
    return m.F_GAN['MPGN', i, s] <= 20000 * m.Y_GAN['MPGN', i, s]
m.yiqu_4 = Constraint(m.T5, m.SC, rule=_yiqu_4)

def _yiqu_5(m, i, s):
    return m.F_GAN['LPGN', i, s] >= 8000 * m.Y_GAN['LPGN', i, s]
m.yiqu_5 = Constraint(m.T5, m.SC, rule=_yiqu_5)

def _yiqu_6(m, i, s):
    return m.F_GAN['LPGN', i, s] <= 10000 * m.Y_GAN['LPGN', i, s]
m.yiqu_6 = Constraint(m.T5, m.SC, rule=_yiqu_6)

def _yiqu_7(m, s):
    return m.Y_GAN['MPGN', 4, s] >=  m.Y_GAN['MPGN', 1, s]
m.yiqu_7 = Constraint(m.SC, rule=_yiqu_7)

def _yiqu_8(m, s):
    return m.Y_GAN['MPGN', 5, s] >=  m.Y_GAN['MPGN', 1, s]
m.yiqu_8 = Constraint(m.SC, rule=_yiqu_8)

def _erqu_1(m, s):
    return m.m2.F['GAN', s] + m.m3.F['GAN', s]  == m.F_GAN['MPGN', 2, s]  + m.F_GAN['MPGN', 3, s]  + m.F_GAN['LPGN', 2, s]  + m.F_GAN['LPGN', 3, s]  + m.F_GAN['SLT', 2, s]
m.erqu_1 = Constraint(m.SC, rule=_erqu_1)

def _erqu_2(m, s):
    return m.Q_GAN2[s] == 0.178 * m.F_GAN['MPGN', 2, s]  + 0.161 * m.F_GAN['MPGN', 3, s]  + 0.111 * m.F_GAN['LPGN', 2, s]  + 0.107 * m.F_GAN['LPGN', 3, s] 
m.erqu_2 = Constraint(m.SC, rule=_erqu_2)

def _erqu_3(m, s):
    return m.Y_GAN['MPGN', 3, s] >= m.Y_GAN['MPGN', 2, s]
m.erqu_3 = Constraint(m.SC, rule=_erqu_3)

def _erqu_4(m, s):
    return m.Y_GAN['LPGN', 3, s] >= m.Y_GAN['LPGN', 2, s]
m.erqu_4 = Constraint(m.SC, rule=_erqu_4)



#####################

def _GAN_GW1(m, s):
    return sum(m.F_GAN['MPGN', j, s] for j in m.T5)  + m.m6.F_V['VLIN', s] - m.m5.F_L['LGAN', s] - m.m5.ToLIQ[s] == m.Demand[s, 'MPGN']
m.GAN_GW1 = Constraint(m.SC, rule=_GAN_GW1)

def _GAN_GW5(m, s):
    return m.F_GAN['LPGN', 1, s] + m.F_GAN['LPGN', 2, s] + m.F_GAN['LPGN', 3, s] == m.Demand[s, 'LPGN'] 
m.GAN_GW5 = Constraint(m.SC, rule=_GAN_GW5)

##########################

def _GAN_CC1(m, s):
    return m.F_L['LIN', s] == m.m1.F['LIN', s] + m.m2.F['LIN', s] + m.m3.F['LIN', s] + m.m4.F['LIN', s] 
m.GAN_CC1 = Constraint(m.SC, rule=_GAN_CC1)

def _GAN_CC2(m, s):
    return m.F_L['LIN', s]  + m.m5.F_L['LGAN', s] - m.m6.F_V['VLIN', s] == m.Sale['LIN', s]
m.GAN_CC2 = Constraint(m.SC, rule=_GAN_CC2)

##############################


def _GAR_GW1(m, s):
    return m.F['GAR', s]  == m.m1.F['GAR', s] + m.m2.F['GAR', s] + m.m3.F['GAR', s] + m.m4.F['GAR', s]
m.GAR_GW1 = Constraint(m.SC, rule=_GAR_GW1)

def _GAR_GW2(m, s):
    return m.F['GAR', s] == m.Demand[s, 'GAR'] 
m.GAR_GW2 = Constraint(m.SC, rule=_GAR_GW2)


def _GAR_CC1(m, s):
    return m.F_L['LAR', s] == m.m1.F['LAR', s] + m.m2.F['LAR', s] + m.m3.F['LAR', s] + m.m4.F['LAR', s]
m.GAR_CC1 = Constraint(m.SC, rule=_GAR_CC1)

def _GAR_CC2(m, s):
    return m.F_L['LAR', s] - m.F['GAR', s] == m.Sale['LAR', s]
m.GAR_CC2 = Constraint(m.SC, rule=_GAR_CC2)

##################################

def _OBJ1(m, s):
    return m.rev_liq[s] == m.F_L['LOX', s] * m.dT / 804 * 1.143 * 1400 + m.F_L['LIN', s] * m.dT / 646 * 0.8083 * 1100 + (m.F_L['LAR', s] - m.F['GAR', s]) * m.dT / 785 * 1.4 * 2000
m.OBJ1 = Constraint(m.SC, rule=_OBJ1)

def _OBJ2(m, s):
    return m.rev_gas[s] == (m.Demand[s, 'GOX'] * 0.4499 + (m.Demand[s, 'MPGN'] + m.Demand[s, 'LPGN']) * 0.1 + m.Demand[s, 'GAR'] * 1.2 ) * m.dT
m.OBJ2 = Constraint(m.SC, rule=_OBJ2)

def _OBJ4(m, s):
    return m.pro_liq[s] == m.m5.F_L['LGOX', s] * m.dT / 804 * 1.143 * 1400 + m.m5.F_L['LGAN', s] * m.dT / 646 * 0.8083 * 1100
m.OBJ4 = Constraint(m.SC, rule=_OBJ4)

def _OBJ5(m, s):
    return m.pro_vap[s] == -m.m6.F_V['VLOX', s] * m.dT / 804 * 1.143 * 1400 - m.m6.F_V['VLIN', s] * m.dT / 646 * 0.8083 * 1100
m.OBJ5 = Constraint(m.SC, rule=_OBJ5)

def _OBJ6(m, s):
    return m.cost1[s] == (m.m1.Q['AIRC', s] + m.m2.Q['AIRC', s] + m.m3.Q['AIRC', s] + m.m4.Q['AIRC', s]) * m.dT * m.price 
m.OBJ6 = Constraint(m.SC, rule=_OBJ6)

def _OBJ7(m, s):
    return m.cost2[s] == (m.m1.Q['GOXC', s] + m.m2.Q['GOXC', s] + m.m4.Q['GOXC', s]) * m.dT * m.price 
m.OBJ7 = Constraint(m.SC, rule=_OBJ7)

def _OBJ8(m, s):
    return m.cost3[s] == (m.Q_GAN1[s] + m.Q_GAN2[s]) * m.dT * m.price
m.OBJ8 = Constraint(m.SC, rule=_OBJ8)

def _OBJ9(m, s):
    return m.cost4[s] == (m.m1.Startup[s] + m.m2.Startup[s] + m.m3.Startup[s] + m.m4.Startup[s] + m.m1.Trans[s] + m.m2.Trans[s] + m.m3.Trans[s] + m.m4.Trans[s] + m.m7.Startup[s] + m.m8.Startup[s]) * m.dT * m.price
m.OBJ9 = Constraint(m.SC, rule=_OBJ9)

def _OBJ10(m, s):
    return m.profit[s] == m.rev_liq[s] + m.rev_gas[s] + m.pro_liq[s] + m.pro_vap[s] - m.cost1[s] - m.cost2[s] - m.cost3[s] - m.cost4[s]
m.OBJ10 = Constraint(m.SC, rule=_OBJ10)

#m.obj = Objective(expr=sum(m.Vent[i] for i in m.T1), sense=minimize)
#m.obj = Objective(expr=m.rev_liq + m.rev_gas + m.rev_pipe + m.pro_liq + m.pro_vap - m.cost1 - m.cost2 - m.cost3 - m.cost4 , sense=maximize)

time = {0:0, 1:1, 2:1, 3:1, 4:1, 5:1}

m.obj = Objective(expr= sum(m.profit[s] * time[s]for s in m.SC), sense=maximize)

ss = SolverFactory('cplex')
ss.solve(m, tee=True, keepfiles=False)
#m.solutions.load_from(results)

# m.display('/home/zqq/MonthlySchedule/display1.txt')
# m.pprint('/home/zqq/MonthlySchedule/main1.txt')

m.ASU = Set(initialize=['ASU1', 'ASU2', 'ASU3', 'ASU4'], ordered=True)
m.GAN = Set(initialize=['MPGN1', 'MPGN2', 'MPGN3', 'MPGN4_1', 'MPGN4_2', 'LPGN1', 'LPGN2', 'LPGN3'], ordered=True)
m.L = Set(initialize=['LOX', 'LIN'], ordered=True)
m.V = Set(initialize=['GOX', 'GAN'], ordered=True)
m.k=Param(mutable=True)
def write_excel():
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('GOX',cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('GAN Compressor',cell_overwrite_ok=True)
    sheet3 = workbook.add_sheet('LIQ',cell_overwrite_ok=True)
    sheet4 = workbook.add_sheet('VAP',cell_overwrite_ok=True)
    ind1 = m.SC
    ind2 = m.ASU
    ind3 = m.GAN
    ind4 = m.L
    ind5 = m.V
    for j in range(1,5):
        sheet1.write(0, j, m.ASU[j])
    for i in m.SC:
        sheet1.write(i, 0, m.SC[i])
        sheet1.write(i, 1, m.m1.F['GOX', i].value)
        sheet1.write(i, 2, m.m2.F['GOX', i].value)
        sheet1.write(i, 3, m.m3.F['GOX', i].value)
        sheet1.write(i, 4, m.m4.F['GOX', i].value)
    for j in range(1,9):
        sheet2.write(0, j, m.GAN[j])
    for i in m.SC:
        sheet2.write(i, 0, m.SC[i])
        for j in range(1,6):
            sheet2.write(i, j, m.F_GAN['MPGN', j, i].value)
        for j in range(6,9):
            sheet2.write(i, j, m.F_GAN['LPGN', j-5, i].value)
    for j in range(1,3):
        sheet3.write(0, j, m.L[j])
    for i in m.SC:
        sheet3.write(i, 0, m.SC[i])
        sheet3.write(i, 1, m.m5.F_L['LGOX', i].value)
        sheet3.write(i, 2, m.m5.F_L['LGAN', i].value)
    for j in range(1,3):
        sheet4.write(0, j, m.V[j])
    for i in m.SC:
        sheet4.write(i, 0, m.SC[i])
        sheet4.write(i, 1, m.m6.F_V['VLOX', i].value)
        sheet4.write(i, 2, m.m6.F_V['VLIN', i].value)
    workbook.save('solutionnew.xls')
write_excel()
