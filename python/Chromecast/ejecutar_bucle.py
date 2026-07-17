import subprocess
import time
import sys

# Usamos una ruta "raw" (r"...") para evitar problemas con la "U" de Users en Windows
script_path = r"C:\Users\mantto2\Desktop\industrial\python\Chromecast\detener_cast.py"

print("Programador iniciado. Ejecutando script cada 3 minutos...")
print("Para detener este bucle, presiona Ctrl + C en esta ventana.")

while True:
    try:
        # Ejecuta el script usando el mismo intérprete de Python activo
        subprocess.run([sys.executable, script_path], check=True)
        print(f"[{time.strftime('%H:%M:%S')}] Script ejecutado con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"[{time.strftime('%H:%M:%S')}] El script falló con error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    
    # Espera 180 segundos (3 minutos)
    time.sleep(180)