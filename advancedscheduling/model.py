from pyomo.environ import *

model = AbstractModel()

model.BigM = 1000

model.I = Set()
model.K = Set()
model.T = Set()
model.J = Set()

model.p = Param(model.I)
model.s = Param(model.K, model.T)
model.q = Param(model.I, model.J)
model.tau = Param(model.K, model.T, model.J)

model.x = Var(model.I, model.K, model.T, domain=Binary)


##F OBBIETTIVO

def obj_exp(model):
    return sum(sum(sum(model.p[i] * model.x[i,k,t] for i in model.I)for k in model.K)for t in model.T)


model.obj = Objective(rule=obj_exp, sense=maximize)


## VINCOLO 1
def const_1(model, i):
    return sum(
        sum(model.x[i, k, t] for t in model.T)
        for k in model.K) <= 1


model.const_1 = Constraint(model.I, rule=const_1)


##VINCOLO 2

def const_2(model, k, t):
    return sum(model.p[i] * model.x[i,k,t] for i in model.I) <= model.s[k, t]


model.const_2 = Constraint(model.K, model.T, rule=const_2)


##VINCOLO 3
def const_3(model, j, k, t):
    return sum(model.q[i,j]*model.x[i,k,t] for i in model.I) <= model.BigM * model.tau[k, t, j]


model.const_3 = Constraint(model.J, model.K, model.T, rule=const_3)
