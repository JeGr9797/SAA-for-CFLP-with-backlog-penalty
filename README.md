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
El segundo modelo consiste en la relajación de un problema multi-etapas a uno de dos
etapas para planeación de producción (Lot-sizing), las variables de primer etapa son los recursos a
usar previo al inicio de la producción.
Se usa Gurubi y CPLEX.
