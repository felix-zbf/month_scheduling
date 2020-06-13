from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition, ProblemFormat

model7 = Block()

# 变压吸附装置1，从空气到氧气只生产氧气

model7.T = RangeSet(1,5)
model7.T2 = RangeSet(0, 5)
model7.G = Set(initialize=['GOX']) # 生产原料以及产品类型定义
model7.R = Set(initialize=['M1','M2']) # 模态定义
model7.TR = Set(initialize=[('M1','M2'),('M2','M1')]) # 模态切换定义
model7.C = Set(initialize=['AIRC','GOXC']) # 流程级平衡参数定义(氧气)

model7.F = Var(model7.G, model7.T, within=Reals, bounds=(0,None), initialize=0) # 每个优化时域点上的产品产量
model7.f = Var(model7.R, model7.G, model7.T, bounds=(0,None), within=Reals, initialize=0) # 不同模态下的产量
model7.Y = Var(model7.T, within=Binary, bounds=(0,1), initialize=0) #
model7.y = Var(model7.R, model7.T2, within=Binary, bounds=(0,1), initialize=0)# 前一时刻的模态定义
model7.Z = Var(model7.TR, model7.T, within=Binary, bounds=(0,1), initialize=0)# 模态允许切换定义
model7.Startup = Var(model7.T, within=Reals, bounds=(0,None), initialize=0)# 启动的单耗
model7.Q = Var(model7.C, model7.T, within=Reals, bounds=(0,None), initialize=0)# 每个时刻的产量定义
model7.q = Var(model7.R, model7.C, model7.T, within=Reals, bounds=(0,None), initialize=0) # 不同模态下产量的定义

def _PSA_1(m, g, i):
    return m.F[g, i] == sum(m.f[r, g, i] for r in m.R)
model7.PSA_1 = Constraint(model7.G, model7.T, rule=_PSA_1) # 产量加和

def _PSA_2(m, i):
    return m.Q['AIRC', i] == sum(m.q[r, 'AIRC', i] for r in m.R) # 空气消耗量
model7.PSA_2 = Constraint(model7.T, rule=_PSA_2)

def _PSA_3(m, i):
    return sum(m.y[r, i] for r in m.R) == 1
model7.PSA_3 = Constraint(model7.T, rule=_PSA_3)

# 变压吸附装置除了正常的启停消耗是否存在由氮压机和氧压机等的消耗。


#Mode1 模态1下无任何损耗
def _Mode1(m, g, i):
    return m.f['M1', g, i] == 0 * m.y['M1', i]
model7.Mode1 = Constraint(model7.G, model7.T, rule=_Mode1)


#Mode2
# 模态2（正常生产模态）下的各个产品产量
# def _Mode2_1(m, i):
#     return m.f['M2', 'AIR', i] == 10000 * m.y['M2', i]
# model7.Mode2_1 = Constraint(model7.T, rule=_Mode2_1)

def _Mode2_2(m, i):
    return m.f['M2', 'GOX', i] == 5000 * m.y['M2', i]
model7.Mode2_2 = Constraint(model7.T, rule=_Mode2_2)

#switch 切换的操作是否允许以及开机的耗损
def _Switch1(m, i):
    return m.Z['M2', 'M1', i] - m.Z['M1', 'M2', i]  == m.y['M1', i] - m.y['M1', i-1]
model7.Switch1 = Constraint(model7.T, rule= _Switch1)

def _Switch2(m, i):
    return m.Z['M1', 'M2', i] - m.Z['M2', 'M1', i]  == m.y['M2', i] - m.y['M2', i-1]
model7.Switch2 = Constraint(model7.T, rule= _Switch2)

def _Switch3(m, i):
    return m.Startup[i] == m.Z['M1', 'M2', i] * 5000
model7.Switch3 = Constraint(model7.T, rule= _Switch3)

#initialize
def _init1(m):
    return m.y['M1', 0] == 0
model7.init1 = Constraint(rule=_init1)

def _init2(m):
    return m.y['M2', 0] == 1
model7.init2 = Constraint(rule=_init2)
