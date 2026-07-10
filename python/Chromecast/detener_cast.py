import time
import pychromecast

def detener_transmisiones():
    # Buscar dispositivos Chromecast en la red local
    # Nota: pychromecast.get_chromecasts() devuelve una lista de dispositivos y un objeto de navegador
    servicios, navegador = pychromecast.get_chromecasts()
    
    if not servicios:
        return # No hay dispositivos en la red

    for cc in servicios:
        cc.wait() # Esperar a que el dispositivo esté listo para recibir comandos
        
        # cc.app_id nos dice si hay una aplicación activa (YouTube, Netflix, etc.)
        # Si hay un app_id y no es el de la pantalla de inicio (None), está transmitiendo
        if cc.app_id:
            print(f"Transmisión detectada en: {cc.name}. Deteniendo...")
            cc.quit_app() # Esta es la orden que detiene el Cast
            print(f"Transmisión detenida en {cc.name}.")

    # Detener la búsqueda en la red para liberar recursos
    pychromecast.discovery.stop_discovery(navegador)

if __name__ == "__main__":
    print("Iniciando el monitor de red para Chromecast...")
    print("Presiona Ctrl+C para salir.")
    
    try:
        while True:
            detener_transmisiones()
            time.sleep(10) # Espera 10 segundos antes de volver a escanear
    except KeyboardInterrupt:
        print("\nMonitor detenido por el usuario.")