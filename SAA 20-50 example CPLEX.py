#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np
import sys
import cplex
from docplex.mp.model import Model
import pandas as pd
import time

#Iniciar parametros
#Tiempo
inicio = time.time()
#Replicas SAA
Iteraciones = 20
#Aquí se guardan valores de funcion objetivo
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
    #Nombre y sentido del porblema
    m = Model(name='SAA',log_output=True)

    #definir conjuntos
    plantas = range(I)
    clientes = range(J)
    escenarios = range(K)

    # agregar variables decision
    #de primer estado
    y = m.binary_var_dict([(i,k) for i in plantas for k in escenarios], name="abrir")

    #de segundo estado
    x = m.continuous_var_dict([(i,j,k) for i in plantas for j in clientes for k in escenarios], lb=0, name="enviar")
    rho = m.continuous_var_dict([(j,k) for j in clientes for k in escenarios], lb=0, name="penalidad")

    # Funcion objetivo
    m.minimize(m.sum(F[i]*y[i,k]*p[k] for i in plantas for k in escenarios) 
                + m.sum(c[i,j]*x[i,j,k]*p[k] for i in plantas for j in clientes for k in escenarios)
                + m.sum(Penalidad*rho[j,k]*p[k] for j in clientes for k in escenarios))


    #restricciones
    #satisfacer demanda para cada cliente en cada escenario
    m.add_constraints(rho[j,k]+m.sum(x[i,j,k] for i in plantas) >= d_j[j,k] for j in clientes for k in escenarios)
    #respetar capacidades para cada planta en cada escenario
    m.add_constraints(m.sum(x[i,j,k] for j in clientes) <= ki[i]*y[i,k] for i in plantas for k in escenarios)
    #restricciones de no anticipacion
    m.add_constraints(y[i,k]==y[i,k-1] for i in plantas for k in escenarios if k >= 1)

    #Aplicar descomposición de Benders
    m.parameters.benders.strategy = 3
    # Resolver
    m.solve()

    #Guardar soluciones objetivo y actualizar
    obj_sample = m.objVal
    obj_values.append(obj_sample)

# Valor esperado
print(f"Valor esperado es: {np.mean(obj_values)}")
#Desviacion estandar
print(f"Desviación estandar es: {np.std(obj_values)}")
fin = time.time()
t_total = fin-inicio
#Tiempo requerido solucion
print("Tiempo total:",t_total)




