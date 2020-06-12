from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat
from Tkinter import *

import xlrd
import matplotlib.pyplot as plt
import math

scenarios = RangeSet(1,4)

def CreateModel(I):
        from ASU1 import model1
	from ASU2 import model2
	from ASU3 import model3
	from ASU4 import model4
	from Liq import model5
	from Vap import model6

        m = ConcreteModel()

	m.add_component('m1',model1)
	m.add_component('m2',model2)
	m.add_component('m3',model3)
	m.add_component('m4',model4)
	m.add_component('m5',model5)
	m.add_component('m6',model6)

	m.T5 = RangeSet(1,5)

	m.G = Set(initialize=['GOX','MPGN','LPGN','GAR'])
	m.G_GAN = Set(initialize=['MPGN','LPGN','SLT'])
	m.S = Set(initialize=['LOX','LIN','LAR'])

	m.F = Var(m.G, within=Reals, bounds=(0,None), initialize=0)
	m.F_GAN = Var(m.G_GAN, m.T5, within=Reals, bounds=(0,None), initialize=0)
	m.Y_GAN = Var(m.G_GAN, m.T5, within=Binary, bounds=(0,1), initialize=0)
	m.Q_GAN1 = Var(within=Reals, bounds=(0,None), initialize=0)
	m.Q_GAN2 = Var(within=Reals, bounds=(0,None), initialize=0)
	m.Vent = Var(within=Reals, bounds=(0,None), initialize=0)
	m.F_L = Var(m.S, within=Reals, bounds=(0,None), initialize=0)

	#m.d2 = Param(m.T1, m.S, initialize=b)
	demand={}
	demand[1] = {'GOX': 68000, 'MPGN': 50000, 'LPGN': 30000, 'GAR': 1300}
	demand[2] = {'GOX': 70000, 'MPGN': 60000, 'LPGN': 20000, 'GAR': 800}
	demand[3] = {'GOX': 80000, 'MPGN': 90000, 'LPGN': 10000, 'GAR': 700}

	m.Demand = Param(m.G, initialize=demand[I])
	m.Sale = Var(m.S, within=Reals, bounds=(0,None), initialize=0)

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

	#def _B(m, i, j):
	#    return m.Sale[i, j] == m.d2[j, i]
	#m.B = Constraint(m.S, m.T1, rule=_B)

	def _B1(m):
	    return m.Sale['LOX'] <= 5000
	m.B1 = Constraint(rule=_B1)

	def _B2(m):
	    return m.Sale['LIN'] <= 5000
	m.B2 = Constraint(rule=_B2)

	def _B3(m):
	    return m.Sale['LAR'] <= 5000
	m.B3 = Constraint(rule=_B3)

	#########################

	def _GOX_GW1(m):
	    return m.F['GOX'] == m.m1.F['GOX'] + m.m2.F['GOX'] + m.m3.F['GOX'] + m.m4.F['GOX']
	m.GOX_GW1 = Constraint(rule=_GOX_GW1)

	def _GOX_GW2(m):
	    return m.F['GOX']  + m.m6.F_V['VLOX'] - m.m5.F_L['LGOX'] - m.Vent == m.Demand['GOX']
	m.GOX_GW2 = Constraint(rule=_GOX_GW2)

	###################

	def _GOX_CC1(m):
	    return m.F_L['LOX'] == m.m1.F['LOX'] + m.m2.F['LOX'] + m.m3.F['LOX'] + m.m4.F['LOX'] 
	m.GOX_CC1 = Constraint(rule=_GOX_CC1)

	def _GOX_CC2(m):
	    return m.F_L['LOX']  + m.m5.F_L['LGOX'] - m.m6.F_V['VLOX'] == m.Sale['LOX']
	m.GOX_CC2 = Constraint(rule=_GOX_CC2)

	#####################

	def _yiqu_1(m):
	    return m.m1.F['GAN'] + m.m4.F['GAN'] +  m.m5.ToLIQ == m.F_GAN['MPGN', 1]  + m.F_GAN['MPGN', 4] + m.F_GAN['MPGN', 5]  + m.F_GAN['LPGN', 1] + m.F_GAN['SLT', 1]
	m.yiqu_1 = Constraint(rule=_yiqu_1)

	def _yiqu_2(m):
	    return m.Q_GAN1 == 0.2 * m.F_GAN['MPGN', 1]  + 0.161 * (m.F_GAN['MPGN', 4] + m.F_GAN['MPGN', 5] ) + 0.108 * m.F_GAN['LPGN', 1] 
	m.yiqu_2 = Constraint(rule=_yiqu_2)

	def _yiqu_3(m, i):
	    return m.F_GAN['MPGN', i] >= 16000 * m.Y_GAN['MPGN', i]
	m.yiqu_3 = Constraint(m.T5, rule=_yiqu_3)

	def _yiqu_4(m, i):
	    return m.F_GAN['MPGN', i] <= 20000 * m.Y_GAN['MPGN', i]
	m.yiqu_4 = Constraint(m.T5, rule=_yiqu_4)

	def _yiqu_5(m, i):
	    return m.F_GAN['LPGN', i] >= 8000 * m.Y_GAN['LPGN', i]
	m.yiqu_5 = Constraint(m.T5, rule=_yiqu_5)

	def _yiqu_6(m, i):
	    return m.F_GAN['LPGN', i] <= 10000 * m.Y_GAN['LPGN', i]
	m.yiqu_6 = Constraint(m.T5, rule=_yiqu_6)

	def _yiqu_7(m):
	    return m.Y_GAN['MPGN', 4] >=  m.Y_GAN['MPGN', 1]
	m.yiqu_7 = Constraint(rule=_yiqu_7)

	def _yiqu_8(m):
	    return m.Y_GAN['MPGN', 5] >=  m.Y_GAN['MPGN', 1]
	m.yiqu_8 = Constraint(rule=_yiqu_8)

	def _erqu_1(m):
	    return m.m2.F['GAN'] + m.m3.F['GAN']  == m.F_GAN['MPGN', 2]  + m.F_GAN['MPGN', 3]  + m.F_GAN['LPGN', 2]  + m.F_GAN['LPGN', 3]  + m.F_GAN['SLT', 2]
	m.erqu_1 = Constraint(rule=_erqu_1)

	def _erqu_2(m):
	    return m.Q_GAN2 == 0.178 * m.F_GAN['MPGN', 2]  + 0.161 * m.F_GAN['MPGN', 3]  + 0.111 * m.F_GAN['LPGN', 2]  + 0.107 * m.F_GAN['LPGN', 3] 
	m.erqu_2 = Constraint(rule=_erqu_2)

	def _erqu_3(m):
	    return m.Y_GAN['MPGN', 3] >= m.Y_GAN['MPGN', 2]
	m.erqu_3 = Constraint(rule=_erqu_3)

	def _erqu_4(m):
	    return m.Y_GAN['LPGN', 3] >= m.Y_GAN['LPGN', 2]
	m.erqu_4 = Constraint(rule=_erqu_4)



	#####################

	def _GAN_GW1(m):
	    return sum(m.F_GAN['MPGN', j] for j in m.T5)  + m.m6.F_V['VLIN'] - m.m5.F_L['LGAN'] - m.m5.ToLIQ == m.Demand['MPGN']
	m.GAN_GW1 = Constraint(rule=_GAN_GW1)

	def _GAN_GW5(m):
	    return m.F_GAN['LPGN', 1] + m.F_GAN['LPGN', 2] + m.F_GAN['LPGN', 3] == m.Demand['LPGN'] 
	m.GAN_GW5 = Constraint(rule=_GAN_GW5)

	##########################

	def _GAN_CC1(m):
	    return m.F_L['LIN'] == m.m1.F['LIN'] + m.m2.F['LIN'] + m.m3.F['LIN'] + m.m4.F['LIN'] 
	m.GAN_CC1 = Constraint(rule=_GAN_CC1)

	def _GAN_CC2(m):
	    return m.F_L['LIN']  + m.m5.F_L['LGAN'] - m.m6.F_V['VLIN'] == m.Sale['LIN']
	m.GAN_CC2 = Constraint(rule=_GAN_CC2)

	##############################


	def _GAR_GW1(m):
	    return m.F['GAR']  == m.m1.F['GAR'] + m.m2.F['GAR'] + m.m3.F['GAR'] + m.m4.F['GAR']
	m.GAR_GW1 = Constraint(rule=_GAR_GW1)

	def _GAR_GW2(m):
	    return m.F['GAR'] == m.Demand['GAR'] 
	m.GAR_GW2 = Constraint(rule=_GAR_GW2)


	def _GAR_CC1(m):
	    return m.F_L['LAR'] == m.m1.F['LAR'] + m.m2.F['LAR'] + m.m3.F['LAR'] + m.m4.F['LAR']
	m.GAR_CC1 = Constraint(rule=_GAR_CC1)

	def _GAR_CC2(m):
	    return m.F_L['LAR'] - m.F['GAR'] == m.Sale['LAR']
	m.GAR_CC2 = Constraint(rule=_GAR_CC2)

	##################################

	def _OBJ1(m):
	    return m.rev_liq == m.F_L['LOX'] * m.dT / 804 * 1.143 * 1400 + m.F_L['LIN'] * m.dT / 646 * 0.8083 * 1100 + (m.F_L['LAR'] - m.F['GAR']) * m.dT / 785 * 1.4 * 2000
	m.OBJ1 = Constraint(rule=_OBJ1)

	def _OBJ2(m):
	    return m.rev_gas == (m.Demand['GOX'] * 0.4499 + (m.Demand['MPGN'] + m.Demand['LPGN']) * 0.1 + m.Demand['GAR'] * 1.2 ) * m.dT
	m.OBJ2 = Constraint(rule=_OBJ2)

	def _OBJ4(m):
	    return m.pro_liq == m.m5.F_L['LGOX'] * m.dT / 804 * 1.143 * 1400 + m.m5.F_L['LGAN'] * m.dT / 646 * 0.8083 * 1100
	m.OBJ4 = Constraint(rule=_OBJ4)

	def _OBJ5(m):
	    return m.pro_vap == -m.m6.F_V['VLOX'] * m.dT / 804 * 1.143 * 1400 - m.m6.F_V['VLIN'] * m.dT / 646 * 0.8083 * 1100
	m.OBJ5 = Constraint(rule=_OBJ5)

	def _OBJ6(m):
	    return m.cost1 == (m.m1.Q['AIRC'] + m.m2.Q['AIRC'] + m.m3.Q['AIRC'] + m.m4.Q['AIRC']) * m.dT * m.price 
	m.OBJ6 = Constraint(rule=_OBJ6)

	def _OBJ7(m):
	    return m.cost2 == (m.m1.Q['GOXC'] + m.m2.Q['GOXC'] + m.m4.Q['GOXC']) * m.dT * m.price 
	m.OBJ7 = Constraint(rule=_OBJ7)

	def _OBJ8(m):
	    return m.cost3 == (m.Q_GAN1 + m.Q_GAN2) * m.dT * m.price
	m.OBJ8 = Constraint(rule=_OBJ8)

	m.obj = Objective(expr= m.rev_liq + m.rev_gas + m.pro_liq + m.pro_vap - m.cost1 - m.cost2 - m.cost3 , sense=maximize)


	#m.solutions.load_from(results)
	return m
	
instance1 = CreateModel(1)
ss = SolverFactory('scipampl')
ss.solve(instance1, tee=True, keepfiles=False)
instance1.display('/home/zqq/MonthlySchedule/display2_1.txt')
instance1.pprint('/home/zqq/MonthlySchedule/main2_1.txt')





