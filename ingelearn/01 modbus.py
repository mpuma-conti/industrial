#Bibliotecas
# Solo funciona con Python instalado en una PC
# Si les da error, yquieren instalar la biblioteca
#en una consola escriben el siguiente comando
# ---> pip install pymodbus

from pymodbus.client import ModbusTcpClient
import time

#Conexion
PLC = ModbusTcpClient("Dirección IP del PLC")
PLC.connect()

#Definicion sensores
sensor = 32 # "Posición" del sensor en la memoria.
maximo_sensor = 25222 # Lectura cuando el sensor está al 100%

#El try/except es una estrategia para cerrar el código / salir del bucle
#Cuando salimos (presionando CTRL+C), cierra la conexión.
try: 
    while True:
        # el bucle while repite estas instrucciones infinitamente
        lectura = PLC.read_input_registers(sensor,1) # leemos del PLC
        
        # y convertimos el valor a porcentaje
        valorEscalado = (lectura.registers[0]/maximo_sensor)*100
        # mostramos el valor
        print(f"El valor del sensor es {valorEscalado:.2f}%")
        time.sleep(0.1) #esperamos 0.1 segundos antes de continuar
        
except KeyboardInterrupt:
    # Cuando cerramos el programa, se asegura de desconectarse primero
    PLC.close()