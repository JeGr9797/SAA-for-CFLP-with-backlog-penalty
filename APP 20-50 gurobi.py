import gurobipy as gp
from gurobipy import GRB
import numpy as np
import time

inicio = time.time()
Iteraciones = 20
obj_values = []
for h in range(Iteraciones):
    
    #Conjunto y notacion
    Periodos = range(3)
    S = 100
    Escenarios = range(S)
    Plantas = range(4)
    MU1 = 12
    SIGMA1 = 1.1547
    MU2 = 12
    SIGMA2 = 1.732
    MU3 = 15
    SIGMA3 = 2.8867
    Recursos = range(3)

    #Parametros
    Demanda = np.array([[3473,3473,3473],
            [20220, 20220, 20220],
            [53895, 53895, 53895],
            [48092, 48092, 48092]])

    Capacidad_produccion = {}
    for t in Periodos:
        for r in Recursos:
            for s in Escenarios:
                if r == 0:
                    Capacidad_produccion[t,r,s] = max((np.random.normal(MU1, SIGMA1),0))
                elif r == 1: 
                    Capacidad_produccion[t,r,s] = max((np.random.normal(MU2, SIGMA2),0))
                else:
                    Capacidad_produccion[t,r,s] = max((np.random.normal(MU3, SIGMA3),0))
           
    
    p = np.array([1.0/S]*S) 
    Costo_Inventario = [1.1, 1.2, 0.8, 1.0]
    Costo_producir = [11, 12, 8, 10]
    Costo_recurso = [24000, 30000, 42000]

    #Declarar e iniciar modelo optimizacion
    m = gp.Model("Lot_sizing_tesis")

    #Variables de decision
    I = m.addVars(Plantas, Periodos, Escenarios, vtype=GRB.INTEGER, name="Inventario")
    X = m.addVars(Plantas, Periodos, Escenarios, name="Produccion")
    W = m.addVars(Plantas, Recursos, Escenarios, vtype=GRB.INTEGER,name="Trabajadores")

    #Funcion objetivo
    #Sentido modelo
    m.ModelSense = GRB.MINIMIZE
    #Costos independientes
    Costo_total_inventario = gp.quicksum(Costo_Inventario[j]*I[j,t,s]*p[s] for j in Plantas for t in Periodos for s in Escenarios )
    Costo_total_produccion = gp.quicksum(Costo_producir[j]*X[j,t,s]*p[s] for j in Plantas for t in Periodos for s in Escenarios )
    Costo_total_recursos = gp.quicksum(Costo_recurso[r]*W[j,r,s]*p[s] for j in Plantas for r in Recursos for s in Escenarios )
    #Costo total
    Costo_total = Costo_total_inventario + Costo_total_produccion + Costo_total_recursos 
    #definir modelo
    m.setObjective(Costo_total)
 
    #Ecuaciones balanceo

    m.addConstrs((X[j,t,s] == Demanda[j,t] + I[j,t,s]) 
                for j in Plantas for t in Periodos if t==0 for s in Escenarios )

    m.addConstrs((I[j,t-1,s] + X[j,t,s] == Demanda[j,t] + I[j,t,s] ) 
                 for j in Plantas for t in Periodos if t>=1 for s in Escenarios )

    #Restriccion set-up
    m.addConstrs((X[j,t,s]<= W[j,r,s]*Capacidad_produccion[t,r,s] ) 
                 for j in Plantas for t in Periodos for r in Recursos for s in Escenarios )

    #restricciones de no anticipacion
    m.addConstrs(W[j,r,s]==W[j,r,s-1] for j in Plantas for r in Recursos for s in Escenarios if s >= 1)
    
    m.setParam('MIPGap', 0.0)
    #optimizar
    m.optimize()
    #Guardar soluciones objetivo y actualizar
    obj_sample = m.objVal
    obj_values.append(obj_sample)

# Valor esperado
print(f"Valor esperado es: {np.mean(obj_values)}")
print(f"Desviación estandar es: {np.std(obj_values)}")
fin = time.time()
t_total = fin-inicio 
print("Tiempo total:",t_total)
