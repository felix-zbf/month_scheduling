from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat
from Tkinter import *
from ASU1 import model1
from ASU2 import model2
from ASU3 import model3
from ASU4 import model4
from Liq import model5
from Vap import model6

import xlrd
import matplotlib.pyplot as plt
import math


m = ConcreteModel()

m.add_component('m1',model1)
m.add_component('m2',model2)
m.add_component('m3',model3)
m.add_component('m4',model4)
m.add_component('m5',model5)
m.add_component('m6',model6)

m.T1 = RangeSet(1,30)
m.T2 = RangeSet(0,30)
m.T3 = RangeSet(1,3)
m.T4 = RangeSet(2,30)
m.T5 = RangeSet(1,5)

m.G = Set(initialize=['GOX','MPGN','LPGN','GAR'])
m.G_GAN = Set(initialize=['MPGN','LPGN','SLT'])
m.S = Set(initialize=['LOX','LIN','LAR'])

m.F = Var(m.G, m.T1, within=Reals, bounds=(0,None), initialize=0)
m.F_GAN = Var(m.G_GAN, m.T5, m.T1, within=Reals, bounds=(0,None), initialize=0)
m.Y_GAN = Var(m.G_GAN, m.T5, m.T1, within=Binary, bounds=(0,1), initialize=0)
m.Q_GAN1 = Var(m.T1, within=Reals, bounds=(0,None), initialize=0)
m.Q_GAN2 = Var(m.T1, within=Reals, bounds=(0,None), initialize=0)
m.D = Var(m.G, m.T2, within=Reals, bounds=(0,None), initialize=0)
m.P = Var(m.G, m.T2, within=Reals, bounds=(0,None), initialize=0)
m.W = Var(m.G, m.T2, within=Reals, bounds=(0,None), initialize=0)
m.Vent = Var(m.T1, within=Reals, bounds=(0,None), initialize=0)
m.Tank = Var(m.S, m.T2, within=Reals, bounds=(0,None), initialize=0)
m.F_L = Var(m.S, m.T1, within=Reals, bounds=(0,None), initialize=0)
m.ToLP = Var(m.T1, within=Reals, bounds=(0,None), initialize=0)
m.lamuda = Var(m.G, m.T2, within=Reals, bounds=(0,None), initialize=0)

list1={}
a={}
b={}
for i in range(1,31):
    #list1[i] = i*math.pi/15
    a[i, 'GOX'] = 50000+250*i#+2000*sin(list1[i])
    a[i, 'MPGN'] = 80000#+4000*sin(list1[i])
    a[i, 'LPGN'] = 20000#+1000*sin(list1[i])
    a[i, 'GAR'] = 800#+100*sin(list1[i])
    #b[i, 'LOX'] = 3720
    #b[i, 'LIN'] = 0
    #b[i, 'LAR'] = 2690


m.d1 = Param(m.T1, m.G, initialize=a)
#m.d2 = Param(m.T1, m.S, initialize=b)
m.Demand = Var(m.G, m.T1, within=Reals, bounds=(0,None), initialize=0)
m.Sale = Var(m.S, m.T1, within=Reals, bounds=(0,None), initialize=0)

m.dT = Param(initialize=24)

m.rev_liq = Var(within=Reals, bounds=(0,None), initialize=0)
m.rev_gas = Var(within=Reals, bounds=(0,None), initialize=0)
m.rev_pipe = Var(within=Reals, bounds=(0,None), initialize=0)
m.pro_liq = Var(within=Reals, bounds=(0,None), initialize=0)
m.pro_vap = Var(within=Reals, bounds=(0,None), initialize=0)
m.cost1 = Var(within=Reals, bounds=(0,None), initialize=0)
m.cost2 = Var(within=Reals, bounds=(0,None), initialize=0)
m.cost3 = Var(within=Reals, bounds=(0,None), initialize=0)
m.cost4 = Var(within=Reals, bounds=(0,None), initialize=0)
m.AIRchange = Var(within=Reals, bounds=(0,None), initialize=0)
m.punish = Var(within=Reals, bounds=(0,None), initialize=0)
m.profit = Var(within=Reals, initialize=0)
m.price = Param(initialize=1)


def _A(m, i, j):
    return m.Demand[i, j] == m.d1[j, i]
m.A = Constraint(m.G, m.T1, rule=_A)

#def _B(m, i, j):
#    return m.Sale[i, j] == m.d2[j, i]
#m.B = Constraint(m.S, m.T1, rule=_B)

def _B1(m, j):
    return m.Sale['LOX', j] <= 3000
m.B1 = Constraint(m.T1, rule=_B1)

def _B2(m, j):
    return m.Sale['LIN', j] <= 3500
m.B2 = Constraint(m.T1, rule=_B2)

def _B3(m, j):
    return m.Sale['LAR', j] <= 1500
m.B3 = Constraint(m.T1, rule=_B3)

def _P_ini1(m):
    return m.P['GOX', 0] == 2100000
m.P_ini1 = Constraint(rule=_P_ini1)

def _P_ini2(m):
    return m.P['MPGN', 0] == 1850000
m.P_ini2 = Constraint(rule=_P_ini2)

#def _P_ini3(m):
#    return m.P['LPGN', 0] == 750000
#m.P_ini3 = Constraint(rule=_P_ini3)

def _Tank_ini1(m):
    return m.Tank['LOX', 0] == 3883.5 * 804
m.Tank_ini1 = Constraint(rule=_Tank_ini1)

def _Tank_ini2(m):
    return m.Tank['LIN', 0] == 1334.5 * 646
m.Tank_ini2 = Constraint(rule=_Tank_ini2)

def _Tank_ini3(m):
    return m.Tank['LAR', 0] == 1555 * 785
m.Tank_ini3 = Constraint(rule=_Tank_ini3)

#########################

def _GOX_GW1(m, i):
    return m.F['GOX', i] == m.m1.F['GOX', i] + m.m2.F['GOX', i] + m.m3.F['GOX', i] + m.m4.F['GOX', i]
m.GOX_GW1 = Constraint(m.T1, rule=_GOX_GW1)

def _GOX_GW2(m, i):
    return m.D['GOX', i] - m.D['GOX', i-1] == (m.F['GOX', i]  + m.m6.F_V['VLOX', i] - m.m5.F_L['LGOX', i]  - m.Demand['GOX', i] - m.Vent[i]) * m.dT
m.GOX_GW2 = Constraint(m.T1, rule=_GOX_GW2)

def _GOX_GW3(m, i):
    return m.D['GOX', i] == (m.P['GOX', i] - 1200000) * 7000 * 22.4 * 0.001 / (8.314 * 273.15)
m.GOX_GW3 = Constraint(m.T2, rule=_GOX_GW3)

def _GOX_GW4(m, i):
    return m.P['GOX', i] >= 1600000
m.GOX_GW4 = Constraint(m.T2, rule=_GOX_GW4)

def _GOX_GW5(m, i):
    return m.P['GOX', i] <= 2600000
m.GOX_GW5 = Constraint(m.T2, rule=_GOX_GW5)

def _GOX_GW6(m, i):
    if value(m.P['GOX', i]) <= 2500000:
         return m.Vent[i] == 0
m.GOX_GW6 = Constraint(m.T1, rule=_GOX_GW6)

###################

def _GOX_CC1(m, i):
    return m.F_L['LOX', i] == m.m1.F['LOX', i] + m.m2.F['LOX', i] + m.m3.F['LOX', i] + m.m4.F['LOX', i] 
m.GOX_CC1 = Constraint(m.T1, rule=_GOX_CC1)

def _GOX_CC2(m, i):
    return m.Tank['LOX', i] - m.Tank['LOX', i-1] == (m.F_L['LOX', i]  + m.m5.F_L['LGOX', i] - m.m6.F_V['VLOX', i] - m.Sale['LOX', i]) * m.dT
m.GOX_CC2 = Constraint(m.T1, rule=_GOX_CC2)

def _GOX_CC3(m, i):
    return m.Tank['LOX', i] >= 2834 * 804
m.GOX_CC3 = Constraint(m.T2, rule=_GOX_CC3)

def _GOX_CC4(m, i):
    return m.Tank['LOX', i] <= 4933 * 804
m.GOX_CC4 = Constraint(m.T2, rule=_GOX_CC4)


#####################

def _yiqu_1(m, i):
    return m.m1.F['GAN', i] + m.m4.F['GAN', i] +  m.m5.ToLIQ[i] == m.F_GAN['MPGN', 1, i]  + m.F_GAN['MPGN', 4, i] + m.F_GAN['MPGN', 5, i]  + m.F_GAN['LPGN', 1, i] + m.F_GAN['SLT', 1, i]
m.yiqu_1 = Constraint(m.T1, rule=_yiqu_1)

def _yiqu_2(m, i):
    return m.Q_GAN1[i] == 0.2 * m.F_GAN['MPGN', 1, i]  + 0.161 * (m.F_GAN['MPGN', 4, i] + m.F_GAN['MPGN', 5, i] ) + 0.108 * m.F_GAN['LPGN', 1, i] 
m.yiqu_2 = Constraint(m.T1, rule=_yiqu_2)

def _yiqu_3(m, i, j):
    return m.F_GAN['MPGN', i, j] >= 16000 * m.Y_GAN['MPGN', i, j]
m.yiqu_3 = Constraint(m.T5, m.T1, rule=_yiqu_3)

def _yiqu_4(m, i, j):
    return m.F_GAN['MPGN', i, j] <= 20000 * m.Y_GAN['MPGN', i, j]
m.yiqu_4 = Constraint(m.T5, m.T1, rule=_yiqu_4)

def _yiqu_5(m, i, j):
    return m.F_GAN['LPGN', i, j] >= 8000 * m.Y_GAN['LPGN', i, j]
m.yiqu_5 = Constraint(m.T5, m.T1, rule=_yiqu_5)

def _yiqu_6(m, i, j):
    return m.F_GAN['LPGN', i, j] <= 10000 * m.Y_GAN['LPGN', i, j]
m.yiqu_6 = Constraint(m.T5, m.T1, rule=_yiqu_6)

def _yiqu_7(m, j):
    return m.Y_GAN['MPGN', 4, j] >=  m.Y_GAN['MPGN', 1, j]
m.yiqu_7 = Constraint(m.T1, rule=_yiqu_7)

def _yiqu_8(m, j):
    return m.Y_GAN['MPGN', 5, j] >=  m.Y_GAN['MPGN', 1, j]
m.yiqu_8 = Constraint(m.T1, rule=_yiqu_8)

def _yiqu_9(m, j):
    if m.Y_GAN['MPGN', 4, j] == m.Y_GAN['MPGN', 5, j]: 
        return m.F_GAN['MPGN', 4, j] == m.F_GAN['MPGN', 5, j]
    return Constraint.Skip
m.yiqu_9 = Constraint(m.T1, rule=_yiqu_9)

def _erqu_1(m, i):
    return m.m2.F['GAN', i] + m.m3.F['GAN', i]  == m.F_GAN['MPGN', 2, i] * m.Y_GAN['MPGN', 2, i] + m.F_GAN['MPGN', 3, i]  + m.F_GAN['LPGN', 2, i]  + m.F_GAN['LPGN', 3, i]  + m.F_GAN['SLT', 2, i]
m.erqu_1 = Constraint(m.T1, rule=_erqu_1)

def _erqu_2(m, i):
    return m.Q_GAN2[i] == 0.178 * m.F_GAN['MPGN', 2, i]  + 0.161 * m.F_GAN['MPGN', 3, i]  + 0.111 * m.F_GAN['LPGN', 2, i]  + 0.107 * m.F_GAN['LPGN', 3, i] 
m.erqu_2 = Constraint(m.T1, rule=_erqu_2)

def _erqu_3(m, i):
    return m.Y_GAN['MPGN', 3, i] >= m.F_GAN['MPGN', 2, i]
m.erqu_3 = Constraint(m.T1, rule=_erqu_3)

def _erqu_4(m, i):
    return m.Y_GAN['LPGN', 3, i] >= m.F_GAN['LPGN', 2, i]
m.erqu_4 = Constraint(m.T1, rule=_erqu_4)



#####################

def _GAN_GW1(m, i):
    return m.D['MPGN', i] - m.D['MPGN', i-1] == (sum(m.F_GAN['MPGN', j, i] for j in m.T5)  + m.m6.F_V['VLIN', i] - m.m5.F_L['LGAN', i] - m.ToLP[i] - m.m5.ToLIQ[i] - m.Demand['MPGN', i]) * m.dT
m.GAN_GW1 = Constraint(m.T1, rule=_GAN_GW1)

def _GAN_GW2(m, i):
    return m.D['MPGN', i] == (m.P['MPGN', i] - 1200000) * 2072 * 22.4 * 0.001 / (8.314 * 273.15)
m.GAN_GW2 = Constraint(m.T2, rule=_GAN_GW2)

def _GAN_GW3(m, i):
    return m.P['MPGN', i] >= 1600000
m.GAN_GW3 = Constraint(m.T2, rule=_GAN_GW3)

def _GAN_GW4(m, i):
    return m.P['MPGN', i] <= 2300000
m.GAN_GW4 = Constraint(m.T2, rule=_GAN_GW4)



def _GAN_GW5(m, i):
    return (m.F_GAN['LPGN', 1, i] + m.F_GAN['LPGN', 2, i] + m.F_GAN['LPGN', 3, i] + m.ToLP[i]) * m.dT == m.Demand['LPGN', i] * m.dT
m.GAN_GW5 = Constraint(m.T1, rule=_GAN_GW5)


#punish
m.GAN = Set(initialize=['MPGN', 'LPGN'])
m.U = Var(m.GAN, m.T5, m.T1, within=Reals, bounds=(0,None), initialize=0)

def _punish1(m, i, j, k):
    return m.F_GAN[i, j, k] - m.F_GAN[i, j, k-1] >= -m.U[i, j, k]
m.punish1 = Constraint(m.GAN, m.T5, m.T4, rule=_punish1)

def _punish2(m, i, j, k):
    return m.F_GAN[i, j, k] - m.F_GAN[i, j, k-1] <= m.U[i, j, k]
m.punish2 = Constraint(m.GAN, m.T5, m.T4, rule=_punish2)
##########################

def _GAN_CC1(m, i):
    return m.F_L['LIN', i] == m.m1.F['LIN', i] + m.m2.F['LIN', i] + m.m3.F['LIN', i] + m.m4.F['LIN', i] 
m.GAN_CC1 = Constraint(m.T1, rule=_GAN_CC1)

def _GAN_CC2(m, i):
    return m.Tank['LIN', i] - m.Tank['LIN', i-1] == (m.F_L['LIN', i]  + m.m5.F_L['LGAN', i] - m.m6.F_V['VLIN', i]  - m.Sale['LIN', i]) * m.dT
m.GAN_CC2 = Constraint(m.T1, rule=_GAN_CC2)

def _GAN_CC3(m, i):
    return m.Tank['LIN', i] >= 942 * 646
m.GAN_CC3 = Constraint(m.T2, rule=_GAN_CC3)

def _GAN_CC4(m, i):
    return m.Tank['LIN', i] <= 1727 * 646
m.GAN_CC4 = Constraint(m.T2, rule=_GAN_CC4)

##############################


def _GAR_GW1(m, i):
    return m.F['GAR', i]  == m.m1.F['GAR', i] + m.m2.F['GAR', i] + m.m3.F['GAR', i] + m.m4.F['GAR', i]
m.GAR_GW1 = Constraint(m.T1, rule=_GAR_GW1)

def _GAR_GW2(m, i):
    return m.F['GAR', i] * m.dT == m.Demand['GAR', i] * m.dT
m.GAR_GW2 = Constraint(m.T1, rule=_GAR_GW2)


def _GAR_CC1(m, i):
    return m.F_L['LAR', i] == m.m1.F['LAR', i] + m.m2.F['LAR', i] + m.m3.F['LAR', i] + m.m4.F['LAR', i]
m.GAR_CC1 = Constraint(m.T1, rule=_GAR_CC1)

def _GAR_CC2(m, i):
    return m.Tank['LAR', i] - m.Tank['LAR', i-1] == (m.F_L['LAR', i] - m.F['GAR', i] - m.Sale['LAR', i]) * m.dT
m.GAR_CC2 = Constraint(m.T1, rule=_GAR_CC2)

def _GAR_CC3(m, i):
    return m.Tank['LAR', i] >= 785 * 785
m.GAR_CC3 = Constraint(m.T2, rule=_GAR_CC3)

def _GAR_CC4(m, i):
    return m.Tank['LAR', i] <= 2325 * 785
m.GAR_CC4 = Constraint(m.T2, rule=_GAR_CC4)

#################################

def _GOX_CF1(m, i):
    return m.P['GOX', i] >= 1900000 - m.lamuda['GOX', i]
m.GOX_CF1 = Constraint(m.T1, rule=_GOX_CF1)

def _GOX_CF2(m, i):
    return m.P['GOX', i] <= 2300000 + m.lamuda['GOX', i]
m.GOX_CF2 = Constraint(m.T1, rule=_GOX_CF2)

def _GAN_CF1(m, i):
    return m.P['MPGN', i] >= 1700000 - m.lamuda['MPGN', i]
m.GAN_CF1 = Constraint(m.T1, rule=_GAN_CF1)

def _GAN_CF2(m, i):
    return m.P['MPGN', i] <= 2100000 + m.lamuda['MPGN', i]
m.GAN_CF2 = Constraint(m.T1, rule=_GAN_CF2)

##################################

def _OBJ1(m):
    return m.rev_liq == sum(m.F_L['LOX', i] * m.dT for i in m.T1) / 804 * 1.143 * 1400 + sum(m.F_L['LIN', i] * m.dT for i in m.T1) / 646 * 0.8083 * 1100 + sum((m.F_L['LAR', i] - m.F['GAR', i]) * m.dT for i in m.T1) / 785 * 1.4 * 2000
m.OBJ1 = Constraint(rule=_OBJ1)

def _OBJ2(m):
    return m.rev_gas == sum((m.Demand['GOX', i] * 0.4499 + (m.Demand['MPGN', i] + m.Demand['LPGN', i]) * 0.1 + m.Demand['GAR', i] * 1.2 ) for i in m.T1) * m.dT
m.OBJ2 = Constraint(rule=_OBJ2)

def _OBJ3(m):
    return m.rev_pipe == (m.D['GOX', 30] - m.D['GOX', 0]) * 0.4499  + (m.D['MPGN', 30] - m.D['MPGN', 0]) * 0.1 
m.OBJ3 = Constraint(rule=_OBJ3)

def _OBJ4(m):
    return m.pro_liq == sum(m.m5.F_L['LGOX', i] * m.dT for i in m.T1) / 804 * 1.143 * 1400 + sum(m.m5.F_L['LGAN', i] * m.dT for i in m.T1) / 646 * 0.8083 * 1100
m.OBJ4 = Constraint(rule=_OBJ4)

def _OBJ5(m):
    return m.pro_vap == -sum(m.m6.F_V['VLOX', i] * m.dT for i in m.T1) / 804 * 1.143 * 1400 - sum(m.m6.F_V['VLIN', i] * m.dT for i in m.T1) / 646 * 0.8083 * 1100
m.OBJ5 = Constraint(rule=_OBJ5)

def _OBJ6(m):
    return m.cost1 == sum((m.m1.Q['AIRC', i] + m.m2.Q['AIRC', i] + m.m3.Q['AIRC', i] + m.m4.Q['AIRC', i]) * m.dT for i in m.T1) * m.price 
m.OBJ6 = Constraint(rule=_OBJ6)

def _OBJ7(m):
    return m.cost2 == sum((m.m1.Q['GOXC', i] + m.m2.Q['GOXC', i] + m.m4.Q['GOXC', i]) * m.dT for i in m.T1) * m.price 
m.OBJ7 = Constraint(rule=_OBJ7)

def _OBJ8(m):
    return m.cost3 == sum((m.Q_GAN1[i] + m.Q_GAN2[i]) for i in m.T1) * m.dT * m.price
m.OBJ8 = Constraint(rule=_OBJ8)

def _OBJ9(m):
    return m.cost4 == sum((m.lamuda['GOX', i] + m.lamuda['MPGN', i]) * m.dT for i in m.T1) * m.price * 1e-4
m.OBJ9 = Constraint(rule=_OBJ9)

def _OBJ10(m):
    return m.AIRchange == sum((m.m3.U[i] + m.m4.U[i]) for i in m.T1) * 0.01 + sum((m.m3.Z_GAR[i] + m.m4.Z_GAR[i]) for i in m.T1)
m.OBJ10 = Constraint(rule=_OBJ10)

def _OBJ11(m):
    return m.punish == sum(m.U[i, j, k] for i in m.GAN for j in m.T5 for k in m.T4)
m.OBJ11 = Constraint(rule=_OBJ11)



#m.obj = Objective(expr=sum(m.Vent[i] for i in m.T1), sense=minimize)
#m.obj = Objective(expr=m.rev_liq + m.rev_gas + m.rev_pipe + m.pro_liq + m.pro_vap - m.cost1 - m.cost2 - m.cost3 - m.cost4 , sense=maximize)
m.obj = Objective(expr= m.rev_liq + m.rev_gas + m.rev_pipe + m.pro_liq + m.pro_vap - m.cost1 - m.cost2 - m.cost3 - m.cost4 - m.AIRchange - m.punish, sense=maximize)

ss = SolverFactory('scipampl')

ss.solve(m, tee=True, keepfiles=False)
#m.solutions.load_from(results)

m.display('/home/zqq/uncertain/compare2/display3.txt')
#m.pprint('/home/zqq/uncertain/compare2/main1.txt')

plt.figure(1)
a1 = []
a2 = []
a3 = []
a4 = []
for i in range(1,31):
    a1.append(value(m.m1.F['GAR', i]))
    a2.append(value(m.m2.F['GAR', i]))
    a3.append(value(m.m3.F['GAR', i]))
    a4.append(value(m.m4.F['GAR', i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('GAR')
plt.title('1#ASU')
plt.ylim(-0.04,0.04)
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('GAR')
plt.title('2#ASU')
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('GAR')
plt.title('3#ASU')
#plt.ylim(15000,25000)
plt.subplot(2,2,4)
plt.plot(x, y4)
plt.xlabel('Time')
plt.ylabel('GAR')
plt.title('4#ASU')
#plt.ylim(25000,34000)
plt.legend()
plt.show()

plt.figure(2)
a1 = []
a2 = []
for i in range(1,31):
    a1.append(value(m.P['GOX', i]))
    a2.append(value(m.P['MPGN', i]))
x = range(1,31)
y1 = a1
y2 = a2
plt.subplot(2,1,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('Pipe Network pressure')
plt.ylim(1600000, 2600000)
plt.subplot(2,1,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('GAN')
plt.title('Pipe Network pressure')
plt.ylim(1600000, 2300000)
plt.legend()
plt.show()

plt.figure(3)
a1 = []
a2 = []
a3 = []
a4 = []
for i in range(1,31):
    a1.append(value(m.m1.F['GOX', i]))
    a2.append(value(m.m2.F['GOX', i]))
    a3.append(value(m.m3.F['GOX', i]))
    a4.append(value(m.m4.F['GOX', i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('1#ASU')
plt.ylim(-0.04,0.04)
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('2#ASU')
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('3#ASU')
plt.ylim(15000,25000)
plt.subplot(2,2,4)
plt.plot(x, y4)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('4#ASU')
plt.ylim(25000,34000)
plt.legend()
plt.show()

plt.figure(4)
a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
for i in range(1,31):
    a1.append(value(m.F_GAN['MPGN', 1, i]))
    a2.append(value(m.F_GAN['MPGN', 2, i]))
    a3.append(value(m.F_GAN['MPGN', 3, i]))
    a4.append(value(m.F_GAN['MPGN', 4, i]))
    a5.append(value(m.F_GAN['MPGN', 5, i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
y5 = a5
plt.subplot(2,3,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('Medium Pressure GAN')
plt.title('1#MPGN')
#plt.ylim(15000,17000)
plt.subplot(2,3,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('Medium Pressure GAN')
plt.title('2#MPGN')
#plt.ylim(-0.04,0.04)
plt.subplot(2,3,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('Medium Pressure GAN')
plt.title('3#MPGN')
#plt.ylim(15000,17000)
plt.subplot(2,3,4)
plt.plot(x, y4)
plt.xlabel('Time')
plt.ylabel('Medium Pressure GAN')
plt.title('4#MPGN_1')
#plt.ylim(19000,21000)
plt.subplot(2,3,5)
plt.plot(x, y5)
plt.xlabel('Time')
plt.ylabel('Medium Pressure GAN')
plt.title('4#MPGN_2')
#plt.ylim(19000,21000)
plt.legend()
plt.show()

plt.figure(5)
a1 = []
a2 = []
a3 = []
a4 = []
for i in range(1,31):
    a1.append(value(m.F_GAN['LPGN', 1, i]))
    a2.append(value(m.F_GAN['LPGN', 2, i]))
    a3.append(value(m.F_GAN['LPGN', 3, i]))
    a4.append(value(m.F_GAN['LPGN', 4, i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('Low Pressure GAN')
plt.title('1#LPGN')
plt.ylim(9000,11000)
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('Low Pressure GAN')
plt.title('2#LPGN')
#plt.ylim(-0.04,0.04)
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('Low Pressure GAN')
plt.title('3#LPGN')
plt.ylim(9000,11000)
plt.show()

plt.figure(6)
a1 = []
a2 = []
a3 = []
a4 = []
for i in range(1,31):
    a1.append(value(m.m1.F['LOX', i]))
    a2.append(value(m.m2.F['LOX', i]))
    a3.append(value(m.m3.F['LOX', i]))
    a4.append(value(m.m4.F['LOX', i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('1#ASU')
#plt.ylim(-0.04,0.04)
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('2#ASU')
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('3#ASU')
plt.subplot(2,2,4)
plt.plot(x, y4)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('4#ASU')
plt.legend()
plt.show()

plt.figure(7)
a1 = []
a2 = []
a3 = []
a4 = []
for i in range(1,31):
    a1.append(value(m.m1.F['LIN', i]))
    a2.append(value(m.m2.F['LIN', i]))
    a3.append(value(m.m3.F['LIN', i]))
    a4.append(value(m.m4.F['LIN', i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('1#ASU')
plt.ylim(-0.04,0.04)
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('2#ASU')
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('3#ASU')
plt.ylim(2200,2600)
plt.subplot(2,2,4)
plt.plot(x, y4)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('4#ASU')
plt.ylim(1200,1400)
plt.legend()
plt.show()

plt.figure(8)
a1 = []
a2 = []
a3 = []
a4 = []
for i in range(1,31):
    a1.append(value(m.m1.F['LAR', i]))
    a2.append(value(m.m2.F['LAR', i]))
    a3.append(value(m.m3.F['LAR', i]))
    a4.append(value(m.m4.F['LAR', i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('LAR')
plt.ylim(-0.04,0.04)
plt.title('1#ASU')
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('LAR')
plt.title('2#ASU')
#plt.ylim(-0.04,0.04)
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('LAR')
plt.title('3#ASU')
plt.ylim(600,1100)
plt.subplot(2,2,4)
plt.plot(x, y4)
plt.xlabel('Time')
plt.ylabel('LAR')
plt.title('4#ASU')
plt.ylim(1500,2000)
plt.legend()
plt.show()

plt.figure(9)
a1 = []
a2 = []
for i in range(1,31):
    a1.append(value(m.Tank['LOX', i]))
    a2.append(value(m.Sale['LOX', i]))
x = range(1,31)
y1 = a1
y2 = a2
plt.subplot(2,1,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('LOX Tank Capacity')
plt.ylim(2834 * 804, 4933 * 804)
plt.subplot(2,1,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('LOX Sale')
plt.legend()
plt.show()

plt.figure(10)
a1 = []
a2 = []
for i in range(1,31):
    a1.append(value(m.Tank['LIN', i]))
    a2.append(value(m.Sale['LIN', i]))
x = range(1,31)
y1 = a1
y2 = a2
plt.subplot(2,1,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('LIN Tank Capacity')
plt.ylim(942 * 646, 1727 * 646)
plt.subplot(2,1,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('LIN Sale')
#plt.ylim(2300,4500)
plt.legend()
plt.show()

plt.figure(11)
a1 = []
a2 = []
for i in range(1,31):
    a1.append(value(m.Tank['LAR', i]))
    a2.append(value(m.Sale['LAR', i]))
x = range(1,31)
y1 = a1
y2 = a2
plt.subplot(2,1,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('LAR')
plt.title('LAR Tank Capacity')
plt.ylim(785 * 785, 2325 * 785)
plt.subplot(2,1,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('LAR')
plt.title('LAR Sale')
#plt.ylim(1000,2000)
plt.legend()
plt.show()

plt.figure(12)
a1 = []
a2 = []
a3 = []
a4 = []
for i in range(1,31):
    a1.append(value(m.m5.F['LGOX', 1, i]))
    a2.append(value(m.m5.F['LGOX', 2, i]))
    a3.append(value(m.m5.F['LGAN', 1, i]))
    a4.append(value(m.m5.F['LGAN', 2, i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
y4 = a4
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('Liq1 LOX')
plt.ylim(-0.04,0.04)
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('LOX')
plt.title('Liq2 LOX')
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('Liq1 LIN')
plt.ylim(-0.04,0.04)
plt.subplot(2,2,4)
plt.plot(x, y4)
plt.xlabel('Time')
plt.ylabel('LIN')
plt.title('Liq2 LIN')
plt.ylim(-0.04,0.04)
plt.legend()
plt.show()

plt.figure(13)
a1 = []
a2 = []
a3 = []
for i in range(1,31):
    a1.append(value(m.m6.F['VLOX', 1, i]))
    a2.append(value(m.m6.F['VLOX', 2, i]))
    a3.append(value(m.m6.F['VLOX', 3, i]))
x = range(1,31)
y1 = a1
y2 = a2
y3 = a3
plt.subplot(2,2,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('Vap1 GOX')
plt.subplot(2,2,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('Vap2 GOX')
plt.subplot(2,2,3)
plt.plot(x, y3)
plt.xlabel('Time')
plt.ylabel('GOX')
plt.title('Vap3 GOX')
plt.legend()
plt.show()

plt.figure(15)
a1 = []
a2 = []
for i in range(1,31):
    a1.append(value(m.m6.F['VLIN', 1, i]))
    a2.append(value(m.m6.F['VLIN', 2, i]))
x = range(1,31)
y1 = a1
y2 = a2
plt.subplot(2,1,1)
plt.plot(x, y1)
plt.xlabel('Time')
plt.ylabel('GAN')
plt.title('Vap1 GAN')
plt.subplot(2,1,2)
plt.plot(x, y2)
plt.xlabel('Time')
plt.ylabel('GAN')
plt.title('Vap2 GAN')
plt.legend()
plt.show()


