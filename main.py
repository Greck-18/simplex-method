from pulp import LpMaximize,LpProblem,LpStatus,LpVariable,GLPK,GLPK_CMD,value
from pulp.constants import LpMinimize
from pulp.pulp import lpSum


N=4
M=3


xindex=[(range(1,M+1)[i],range(1,N+1)[j]) for j in range(N) for i in range(M)]


model=LpProblem("Transportation_LP_Problem",LpMinimize)

x=LpVariable.dicts("x",xindex,0,None)
# print(x)

# model+=2.0*x[1,1]+3.0*x[1,2]+4.0*x[1,3]+2.0*x[1,4]+8.0*x[2,1]+4.0*x[2,2]+1.0*x[2,3]+4.0*x[2,4]+9.0*x[3,1]+7.0*x[3,2]+3.0*x[3,3]+6.0*x[3,4]



# print(model)

# for i in range(1,4):
#     for j,k in enumerate(a[i-1]):
#         model+=lpSum(x[i,j+1])




# , "Transportation cost"


# for i in range(1,N+1):
#     model+=x[1,i]+x[2,i]+x[3,i]>=100

# print(model)

# for i in range(1,M+1):
#         if i==1:
#             value1=140
#         elif i==2:
#             value1=160
#         else:
#             value1=120
#         model+=x[i,1]+x[i,2]+x[i,3]+x[i,4]<=value1

# print(model)
# model+=x[1,1]+x[1,2]+x[1,3]+x[1,4] <=140.0
# model+=x[2,1]+x[2,2]+x[2,3]+x[2,4] <=160.0
# model+=x[3,1]+x[3,2]+x[3,3]+x[3,4] <=120.0

# print(model)



# model+=x[1,1]+x[2,1]+x[3,1] >=150.0
# model+=x[1,2]+x[2,2]+x[3,2] >=90.0
# model+=x[1,3]+x[2,3]+x[3,3] >=100.0
# model+=x[1,4]+x[2,4]+x[3,4] >=80.0

# model.solve()

# print("Status:",LpStatus[model.status])

# print('-'*10)

# for v in model.variables():
#     print(v.name,"=",v.varValue)

# print("Objective Function",value(model.objective))
