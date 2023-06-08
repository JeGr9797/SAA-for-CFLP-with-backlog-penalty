# SAA-for-CFLP-with-backlog-penalty-and-Lot-sizing
Hola, en este repositorio vienen los códigos que se usaron para resolver los modelos 
de optimización correspondientes a mi tesis de maestría en Tecnológico de Monterrey,
consisten en una serie de modelos base que pueden modificarse a gusto de quien 
quiera utilizarlos.
Consiste en dos modelos de optimización, siendo el primero de ellos el CFLP (Capacitated
Facility Location Problem) con demandas aleatorias y penalización por no entregas, el
modelo es formulado como uno de programación estocástica de dos etapas, donde las 
variables de decisión de primer etapa son que plantas abrir (variables binarias), las 
de segundo etapa corresponden a los envíos y las no entregas.

índices:  $i \in I$ el conjunto de plantas que se pueden abrir, $j \in J$ el conjunto de mercados que deben ser satisfechos, $s \in S$ el conjunto de los escenarios de las posibles realizaciones.\
 Parámetros: $P^s$ es la probabilidad de que ocurra el escenario $s$, $C_{ij}$ el costo de enviar una unidad de una planta $i$ a un mercado $j$, la demanda $D_{j}^s)$  (variable aleatoria) en cada escenario $s$, cada planta tiene una capacidad $K_i$, con un costo operativo $F_i$ y $BP$ una penalidad por unidad no entregada al cliente $j$.\
Variables de decisión: $x_{ij}^s$ la cantidad de productos a enviar de la planta $i$ al mercado $j$ en escenario $s$, $\rho_j^s$ unidades no entregadas al cliente $j$ en escenario $s$, $y_{i}^s$ tomando valor 1 si se abre una planta en escenario $s$.


El problema a resolver es el siguiente:\
$\min P^s\sum_{s \in S}\left[ \sum_{i \in I}F_iy_{i}^s + \sum_{i \in  I}\sum_{j \in J}C_{ij}x_{ij}^s+ \sum_{j \in J}BP\rho_j^s\right]$\
Sujeto a:\
$\rho_j^s \geq D_{j}^s- \sum_{i \in I}x_{ij}^s \ \forall j \in J, s\in S$\
$\sum_{j \in J}x_{ij}^s\leq k_iy_{i}^s \ \forall i \in I, s\in S$\
$y_{i}^s \in \{0,1\}, \rho_j^s \geq 0\ \forall\  j \in J, s\in S, x_{ij} \geq 0\ \forall\ i \in I, j \in J, s\in S $

Las restricciones de no anticipación se pueden formular como:

$y_{i}^s = y_{i}^{s-1}\ ∀\ i \in I, s \geq 2$\
$y_{i}^s = \sum_{s \in S}P^sy_{i}^s ∀\ i \in I$

Se hace una implementación basada en la descomposición de Benders en Gurobi, la formulación matemática es la siguiente.\
El problema maestro es:\
$\min \sum_{s \in S}\sum_{i \in I}F_iy_{i}^s+\sum_{s \in S}P^s\theta^s$\
$\theta^s \geq - \sum_{s \in  S}\left[ \sum_{i \in I}k_i\overline{y_{i}^s}\pi_{i,O'}- \sum_{j \in J}D_{j}^s\pi_{j,O'}\right] \ \forall\ O' \in O, s \in S$\
$y_{i}^s \in \{0,1\}$\
Donde $\theta^s$ es un valor de corte para cada escenario $s$, $\overline{y_{i}^s}$ es el valor que se obtiene al resolver el problema maestro en cada iteración, $\pi_{i,O'}^s$ y $\pi_{j,O'}^s$ son los valores de la solución del subproblema obteniendo los puntos extremos del poliedro definidos como $O' \in O$\
Los subproblemas se definen como:\
    $\max\ - \sum_{s \in  S}\left[ \sum_{i \in I}k_i\overline{y_{i}^s}\pi_{i,O'}- \sum_{j \in J}D_{j}^s\pi_{j,O'}\right]$\
    $\pi_{i,O'}-\pi_{j,O'} \leq C_{ij} \ \forall\ i \in I, j \in J, O' \in O$\ 
    $\pi_{j,O'} \leq BP \ \forall\ j \in J, O' \in O$\
    $\pi_{j,O'}, \pi_{i,O'} \geq 0 \ \forall i \in I, j \in J, O' \in O$\ 


El segundo modelo consiste en la relajación de un problema multi-etapas a uno de dos
etapas para planeación de producción (Lot-sizing), las variables de primer etapa son los recursos a
usar previo al inicio de la producción.
Se usa Gurubi y CPLEX.\
Para el modelo multi-etapas se utiliza Lingo 20.0, la formulación del modelo multi-etapas es la siguiente:\

$\min \sum_{s \in S}P^s\sum_{i \in \ I^{ci}}\sum_{r \in R}W_{i,r}^sC_r |T|+\sum_{s \in S}P^s\sum_{i \in \ I^{ci}}\sum_{t \in T}(X_{i,t}^sC_x+Inv_{i,t}^sC_{Inv})$\
$X_{i,t}^s+Inv_{i,0}=d_{i,t}+Inv_{i,t}^s \ \forall t = 1, i \in I^{ci}, s\in S$\
$X_{i,t}^s+Inv_{i,t-1}^s=d_{i,t}+Inv_{i,t}^s \ \forall t \geq 2, i \in I^{ci}, s\in S$\
$X_{i,t}^{s}\le W_{i,r}^s\alpha_r^{s} \ \forall t \in T, i \in I^{ci},  s\in S$\
$X_{t}^{s} = \sum_{s \in S \setminus N_{s(t)}}P^sX_{i,t}^s/P(n_{s(t)})  \ \forall t \in T, i \in  I^{ci}, s\in N_{s(t)}$\
$Inv_{i,t}^s = \sum_{s \in S \setminus N_{s(t)}}P^sInv_{i,t}^s/P(n_{s(t)})  \ \forall t \in T, i \in  I^{ci}, s\in N_{s(t)}$\
$W_{i,r}^s = \sum_{s \in S \setminus N_{s(t)}}P^sW_{i,r}^s/P(n_{s(t)})  \ \forall r \in R, i \in  I^{ci}, s\in N_{s(t)}$\
$X_{t}^{s}, Inv_{i,t}^s, W_{i,r}^s \in \mathbb{Z}^+$






## Referencia
Goméz-Rocha, José E. (2023). Un enfoque de solución a la integración del problema de plantas capacitadas con la planeación agregada de la producción bajo incertidumbre usando programación estocástica [Tesis para obtar al grado de Maestro en Ciencias de la Ingeniería]. Instituto Tecnológico y de Estudios Superiores de Monterrey.
