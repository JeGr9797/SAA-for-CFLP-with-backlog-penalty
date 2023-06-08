# SAA-for-CFLP-with-backlog-penalty-and-Lot-sizing
Hola, en este repositorio vienen los códigos que se usaron para resolver los modelos 
de optimización correspondientes a mi tesis de maestría en Tecnológico de Monterrey,
consisten en una serie de modelos base que pueden modificarse a gusto de quien 
quiera utilizarlos.
Consiste en dos modelos de optimización, siendo el primero de ellos el CFLP (Capacitated
Facility Location Problem) con demandas aleatorias y penalización por no entregas, el
modelo es formulado como uno de programnación estocástica de dos etapas, donde las 
variables de decisión de primer etapa son que plantas abrir (variables binarias), las 
de segundo etapa corresponden a los envíos y las no entregas.

El problema a resolver es el siguiente:\
$\min \sum_{i \in I}F_iy_i+P^s\left[ \sum_{i \in  I}\sum_{j \in J}c_{ij}x_{ij}^s+ \sum_{j \in J}BP\rho_j^s\right]$\
Sujeto a:\
$\rho_j^s \geq D_{j}^s- \sum_{i \in I}x_{ij}^s \ \forall j \in J, s\in S$\
$\sum_{j \in J}x_{ij}^s\leq k_iy_i \ \forall i \in I, s\in S$\
$y_i \in \{0,1\}, \rho_j^s \geq 0\ \forall\  j \in J, s\in S, x_{ij} \geq 0\ \forall\ i \in I, j \in J, s\in S $\

El segundo modelo consiste en la relajación de un problema multi-etapas a uno de dos
etapas para planeación de producción (Lot-sizing), las variables de primer etapa son los recursos a
usar previo al inicio de la producción.
Se usa Gurubi y CPLEX.



## Referencia
Goméz-Rocha, José E. (2023). Un enfoque de solución a la integración del problema de plantas capacitadas con la planeación agregada de la producción bajo incertidumbre usando programación estocástica [Tesis para obtar al grado de Maestro en Ciencias de la Ingeniería]. Instituto Tecnológico y de Estudios Superiores de Monterrey.
