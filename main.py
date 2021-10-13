from pulp.pulp import lpSum
from scipy import linalg
from scipy.optimize import linprog

from pulp import LpMaximize,LpProblem,LpStatus,LpVariable

#SciPy
#---------------------------------------------
# linprog() решает только задачи минимизации (не максимизации) и не допускает ограничений-неравенств со знаком больше или равно (≥). Чтобы обойти эти проблемы, нам необходимо изменить описание задачи перед запуском оптимизации:(вместо максимизации мы
# всё минимизируем ( т.е домнажаем на -1) и вместо знака >= , ставим противоположный знак , домнажая на -1)


# оптимизация и поиск корней для линейного программирования
#-------------------------------------------
# z=x+2y
# 2x+y<=20
# -4x+5y<=10
# -x+2y>=-2
# -x+5y=15
# x>=0
# y>=0
# домножаем на -1 главную функцию и там где знак >=
#-z=-x-2y
# 2x+y<=20
# -4x+5y<=10
# x-2y<=2
#-x+5y=15
# x>=0
# y>=0
#----------------------------------------------
# obj=[-1,-2]

# left_ineq=[[2,1],[-4,5],[1,-2]]
# right_ineq=[20,10,2]
# left_eq=[[-1,5]]
# right_eq=[15]

# bnd=[(0,float("inf")),(0,float('inf'))] # границы

# opt=linprog(c=obj,A_ub=left_ineq,b_ub=right_ineq,
#             A_eq=left_eq,b_eq=right_eq,bounds=bnd,
#             method="revised simplex")

#--------------------------------------------------

# решение задача о производстве(о продуктах, раб. #силе силе,используемое сырьё)
#----------------------------------------
# 20x1 + 12x2 + 40x3 +25x4 - profit
# x1+x2+x3+x4<=50(раб сила)
# 3x1+2x2+x3<=100(сырьё А)
# x2+2x3+3x4<=90(материал В)
# x1,x2,x3,x4>=0

#-----------------------------------------

# obj=[-20,-12,-40,-25]
# left_ineq=[[1,1,1,1],[3,2,1,0],[0,1,2,3]]
# right_ineq=[50,100,90]
# opt=linprog(c=obj,A_ub=left_ineq,b_ub=right_ineq,
#     method="revised simplex")

# print(opt)

#-------------------------------------------------

#Pulp
#------------------------------------------------
#в pulp уже можно решать задачу максимизации без вмешательств , не надо умножать на -1

# условие :
#-----------------------------------------------
# z=x+2y
# 2x+y<=20
# -4x+5y<=10
# -x+2y>=-2
# -x+5y=15
# x>=0
# y>=0
#------------------------------------------------

# model=LpProblem(name="small-problem",sense=LpMaximize)

# x=LpVariable(name="x",lowBound=0)
# y=LpVariable(name="y",lowBound=0)



# model+=(2*x+y<=20,"red_constraint")
# model+=(4*x-5*y>=-10,"blue_constraint")
# model+=(-x+2*y>=-2,"yellow_constraint")
# model+=(-x+5*y==15,"green_constraint")

# #целевая функция
# obj_func=x+2*y
# model+=obj_func

# status=model.solve()

# print(f"status:{model.status}, {LpStatus[model.status]}")

# print(f"objective: {model.objective.value()}")

# for var in model.variables():
#     print(f"{var.name}: {var.value}")


# for name,constraint in model.constraints.items():
#     print(f"{name}: {constraint.value()}")

#------------------------------------------------

# решение о производстве
#---------------------------------------------------
# 20x1 + 12x2 + 40x3 +25x4 - profit
# x1+x2+x3+x4<=50(раб сила)
# 3x1+2x2+x3<=100(сырьё А)
# x2+2x3+3x4<=90(материал В)
# x1,x2,x3,x4>=0
#-------------------------------------------------
# model=LpProblem(name="resource-allocation",sense=LpMaximize)

# # описываем переменные
# # x1,x2,x3,x4
# x={i:LpVariable(name=f'x{i}',lowBound=0) for i in range(1,5)}

# #добавляем ограничения
# model+=(lpSum(x.values())<=50,"manpower")
# model+=(3*x[1]+2*x[2]+x[3]<=100,"matherial_a")
# model+=(x[2]+2*x[3]+3*x[4]<=90,"material_b")

# #описываем цель
# model+=20*x[1]+12*x[2]+40*x[3]+25*x[4]

# status=model.solve()

# print(f"status: {model.status}, {LpStatus[model.status]}")
# print(f"objective: {model.objective.value()}")

# for var in x.values():
#     print(f"{var.name}: {var.value()}")

# for name, constraint in model.constraints.items():
#     print(f"{name}: {constraint.value()}")
