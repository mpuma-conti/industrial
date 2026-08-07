from pylogix import PLC
import time
import csv

# ================= CONFIGURACIÓN =================
PLC_IP = '10.10.10.1'  # Reemplaza con la IP real de tu PLC
TIEMPO_MUESTREO = 1.0    # Tiempo entre lecturas en segundos
ARCHIVO_SALIDA = 'datos_lic203.csv'

# Tags a leer
TAGS = [
    "Program:MainProgram.LIC203.SP",
    "Program:MainProgram.LE203",
    "Program:MainProgram.LCV203"
]
# =================================================

def iniciar_captura():
    print(f"Intentando conectar al PLC en {PLC_IP}...")
    
    with PLC() as comm:
        comm.IPAddress = PLC_IP
        
        # Crear y abrir el archivo CSV para guardar los datos
        with open(ARCHIVO_SALIDA, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tiempo (s)', 'SP (LIC203)', 'PV (LE203)', 'CV (LCV203)'])
            
            print("Conexión establecida. Iniciando captura de datos...")
            print("Presiona Ctrl+C en la consola para detener.\n")
            
            tiempo_inicio = time.time()
            
            try:
                while True:
                    tiempo_actual = time.time() - tiempo_inicio
                    
                    # Leer todos los tags de una sola vez
                    respuestas = comm.Read(TAGS)
                    
                    # Verificar que la lectura fue exitosa para los 3 tags
                    if all(r.Status == 'Success' for r in respuestas):
                        sp = respuestas[0].Value
                        pv = respuestas[1].Value
                        cv = respuestas[2].Value
                        
                        # Guardar en el CSV
                        writer.writerow([round(tiempo_actual, 2), sp, pv, cv])
                        
                        # Mostrar en pantalla
                        print(f"T: {tiempo_actual:.1f}s | SP: {sp:.2f} | Nivel (PV): {pv:.2f} | Válvula (CV): {cv:.2f}")
                    else:
                        print(f"T: {tiempo_actual:.1f}s | Error de lectura: revisa los nombres de los tags o la conexión.")
                    
                    # Esperar hasta la siguiente muestra
                    time.sleep(TIEMPO_MUESTREO)
                    
            except KeyboardInterrupt:
                print("\nCaptura detenida. Los datos se han guardado en", ARCHIVO_SALIDA)

if __name__ == '__main__':
    iniciar_captura()