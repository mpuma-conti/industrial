import casadi as ca
import numpy as np
import matplotlib.pyplot as plt

# Definición del modelo de tanque de nivel
def tank_model(x, u):
    A = 1.0    # Área de la sección transversal del tanque
    a = 0.1    # Área de la válvula de entrada
    h = x[0]   # Nivel del tanque

    # Ecuación del modelo
    dh_dt = (a/u) * ca.sqrt(h)

    return ca.vertcat(dh_dt)

# Parámetros del sistema
h0 = 0.5  # Nivel inicial del tanque
u_max = 1.0  # Flujo máximo de entrada

# Crear variables simbólicas
h = ca.MX.sym('h')   # Nivel del tanque
u = ca.MX.sym('u')   # Flujo de entrada

# Definir el modelo de tanque de nivel
model = tank_model([h], u)

# Definir las restricciones del problema de optimización
g = ca.vertcat(h, u - u_max)

# Configurar el problema de optimización MPC
nlp = {'x': ca.vertcat(h, u), 'f': model, 'g': g}
opts = {'ipopt.print_level': 0, 'print_time': 0, 'ipopt.tol': 1e-3}

solver = ca.nlpsol('solver', 'ipopt', nlp, opts)

# Configurar parámetros iniciales y horizonte de predicción
x0 = [h0, 0.5]  # Condiciones iniciales
N = 20           # Horizonte de predicción

# Lista para almacenar resultados
h_values = [h0]
u_values = []

# Implementación del control MPC
for _ in range(50):
    # Resolver el problema de optimización MPC
    sol = solver(x0=x0)

    # Obtener la solución óptima
    u_opt = sol['x'][-1]

    # Aplicar el primer valor de control
    h0 = tank_model(x0, u_opt)[0]

    # Almacenar resultados
    h_values.append(h0)
    u_values.append(u_opt)

# Visualizar resultados
plt.plot(h_values, label='Nivel del Tanque')
plt.xlabel('Iteración')
plt.ylabel('Nivel del Tanque')
plt.legend()
plt.show()
