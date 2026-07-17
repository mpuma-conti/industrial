import time
import pychromecast

# Coloca aquí la IP del televisor
IP_TV = "10.0.0.170"

def detener_transmision_directa():
    navegador = None
    try:
        servicios, navegador = pychromecast.get_chromecasts(known_hosts=[IP_TV])
        
        if not servicios:
            print(f"No se detectó el TV en {IP_TV}. Puede estar en reposo o apagado.")
            return

        cc = servicios[0] # Seleccionamos el dispositivo encontrado
        
        # 1. PRIMERO esperamos a que la conexión se establezca
        cc.wait(timeout=5.0) 
        
        # 2. LUEGO verificamos si hay alguna aplicación activa
        if cc.app_id:
            print(f"Transmisión detectada en: {cc.name}. Deteniendo...")
            cc.quit_app()
            print("Transmisión detenida con éxito.")
            
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    finally:
        # 3. AL FINAL detenemos el escáner de red, pase lo que pase
        if navegador:
            navegador.stop_discovery()

if __name__ == "__main__":
    print(f"Iniciando monitor directo para la IP {IP_TV}...")
    print("Presiona Ctrl+C para salir.")
    
    try:
        while True:
            detener_transmision_directa()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitor detenido por el usuario.")