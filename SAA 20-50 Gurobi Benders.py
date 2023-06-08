import numpy as np
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import time

#Iniciar parametros
inicio = time.time()
#Replicas
Iteraciones = 20
#Iniciar donde se guardan valores funcion objetivo
obj_values = []
for h in range(Iteraciones):
    #Leer informacion de costos c_ij
    #Aqui el path cambia donde se guarde el archivo excel
    df1 = pd.read_excel(r"C:\Users\jegr9\OneDrive\Escritorio\MCI\Tesis\Test SCFLP\20-50 Benders\20­50a.xlsx", sheet_name=1,usecols="A:AX",nrows=20)

    # Definir constantes del modelo
    #Penalidad faltante
    Penalidad = 11
    #capacidad planta
    ki = np.array([357016,211253,157026,10859,63231,239170,43467,184093,345475,281392,9386,287485,168540,182659,
                   69124,59713,150395,16801,187491,306606])
    #costo fijo
    F = np.array([1520379,710022,688431,35652,211210,980029,170606,771422,1538322,1147290,35587
    ,967293,413915,815213,300130,261438,396651,67744,623570,1316033])
    #costo transporte
    c = df1.values
    # numero de escenarios
    K = 100
    # numero plantas
    I = 20
    # numero clientes
    J = 50
    #demanda aleatoria
    #demanda
    mu = np.array([6973, 8823, 5089, 5208, 5662, 7295, 7625, 7544, 9161, 6498,
                         8755, 7918, 7738, 7627, 7789, 7606, 7364, 5662, 9163, 5699,
                         7628, 9538, 8462, 8968, 9895, 8877, 5158, 8823, 8635, 7536,
                         7499, 5478, 6668, 9028, 7869, 8277, 6364, 8176, 5875, 6275,
                         7508, 8951, 7167, 5865, 9535, 6542, 8794, 7859, 6140, 6793,
                         5252])

    sigma = np.array([1381, 1883, 844, 1384, 1278, 1067, 2175, 941, 1017, 1062,
                        1949, 2251, 1550, 1012, 2092, 1613, 1503, 1278, 1414, 984,
                        784, 2337, 943, 1793, 1079, 1441, 1231, 2364, 1201, 1669,
                        1151, 677, 1321, 1113, 884, 1357, 747, 850, 637, 1382,
                        925, 975, 1866, 934, 2613, 1040, 1613, 883, 1281, 1257,
                        600])

    d_j = np.array([np.random.normal(mu[i], sigma[i], K) for i in range(mu.shape[0])])


    #probabilidad escenario
    p = np.array([1.0/K]*K) 

    #definir conjuntos
    plantas = range(I)
    clientes = range(J)
    escenarios = range(K)

    def MybendersCallback(master, where):
      # Cada vez que se encuentre una nueva solucion entera, usar el callback
        if where == GRB.callback.MIPSOL:

            # extraer informacion del problema maestro
            y_bar = {}
            y_bar = master.cbGetSolution(y)

            # Iniciar los subproblemas duales
            sub = gp.Model('subproblem')

            # Variables duales
            u = sub.addVars(plantas, name='u')
            # UB es 10, ver tesis, debido a que maximo posible valor de v es max c_ij
            v = sub.addVars(clientes, ub = 10, name='v')
            
            #Actualizar subproblema
            #Solo si se usa el CFLP tradicional
            #sub.update()

            # Restricciones del problema dual
            sub.addConstrs((v[j] - u[i] <= c[i,j] for i in plantas for j in clientes))
            # No es necesaria ya que UB de v es 10
            #sub.addConstrs((v[j]  <= Penalidad for i in plantas for j in clientes))


            # Indicarlo como objetivo a optimizar
            sub.setObjective(gp.quicksum(d_j[j,k]*v[j]*p[k] for j in clientes for k in escenarios)-gp.quicksum(ki[i]*y_bar[i,k]*u[i]*p[k] for i in plantas for k in escenarios))

            # Parametros de Gurobi no deseados
            #No generar el log en cada iteracion de Benders para el MIP
            sub.setParam('LogToConsole', 0)
            #Con este se obtienen las rayas extremas que son requeridas en la descomposicion de Benders
            sub.setParam('InfUnbdInfo', 1)
            sub.setParam('DualReductions', 0)
            #Sentido del modelo
            sub.ModelSense=GRB.MAXIMIZE

            # Optimizar subproblema dual
            sub.optimize()

            # Si no es factible extraer rayas extremas del poliedro
            # Esto no es necesario a menos que sea el CFLP tradicional
            if sub.status == 5:
                u_bar = np.zeros((I))
                #for i in plantas:
                    #u_bar[i] = u[i].UnbdRay

                v_bar = np.zeros((J))
                #for j in clientes:
                    #v_bar[j] = v[j].UnbdRay

              # Agregar corte de factibilidad
                #expr =  gp.quicksum(d_j[j,k]*v_bar[j]*p[k] for j in clientes for k in escenarios)-gp.quicksum(ki[i]*y[i,k]*u_bar[i]*p[k] for i in plantas for k in escenarios)
                #for k in escenarios:
                    #master.cbLazy(expr <= 0)

            #Si es factible extraer puntos extremos del problema
            else: 
                u_bar =  np.zeros((I))
                for i in plantas:
                    u_bar[i] = u[i].X

                v_bar = np.zeros((J))
                for j in clientes:
                    v_bar[j] = v[j].X

              #Agregar corte de factibilidad
                expr =  gp.quicksum(d_j[j,k]*v_bar[j]*p[k] for j in clientes for k in escenarios)-gp.quicksum(ki[i]*y[i,k]*u_bar[i]*p[k] for i in plantas for k in escenarios)
                for k in escenarios:
                    master.cbLazy(z[k] >= expr)
            
    # Iniciar problema maestro
    master = gp.Model('master_problem')

    # Agregar variables binarias
    z = master.addVars(escenarios, name='z')
    y = master.addVars(plantas, escenarios, vtype=GRB.BINARY, name='y')

    # Definir objetivo y sentido del modelo
    master.ModelSense=GRB.MINIMIZE
    master.setObjective(gp.quicksum(F[i]*y[i,k]*p[k] for i in plantas for k in escenarios) + gp.quicksum(z[k]*p[k] for k in escenarios))

    #restricciones de no anticipacion
    master.addConstrs(y[i,k]==y[i,k-1] for i in plantas for k in escenarios if k >= 1)
    #master.addConstrs(gp.quicksum(y[i,k]*p[k] for k in escenarios) == y[i,k] for i in plantas for k in escenarios)

    # Indicar el uso de lazy constraints
    master.setParam('LazyConstraints', 1)

    # Resolver el maestro con el uso del callback para el subproblema
    master.optimize(MybendersCallback)
    
    #Actualizar maestro
    #Solamente si se usa el CFLP tradicional
    master.update()
    #Gap y tiempo
    master.setParam('MIPGap', 0.0)
    master.setParam("TimeLimit",7200)

    # Resolver
    #Guardar soluciones objetivo y actualizar
    obj_sample = master.objVal
    obj_values.append(obj_sample)

# Valor esperado
print(f"Valor esperado es: {np.mean(obj_values)}")
#Desviacion estandar
print(f"Desviación estandar es: {np.std(obj_values)}")
fin = time.time()
t_total = fin-inicio
#Tiempo total SAA
print("Tiempo total:",t_total)

