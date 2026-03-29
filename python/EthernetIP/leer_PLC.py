"""
Lectura de variables por EtherNet/IP
Lee la instancia de ensamblaje (Assembly Instance) 46
IP del dispositivo: 10.10.10.206

Requiere: pip install pycomm3
"""

from pycomm3 import CIPDriver
from pycomm3.cip import Services, ClassCode
import struct
import time
import sys


# ── Configuración ──────────────────────────────────────────────
PLC_IP = "10.10.10.206"
ASSEMBLY_INSTANCE = 100          # Instancia de ensamblaje a leer
INTERVALO_LECTURA = 1.0         # Segundos entre lecturas
CANTIDAD_BYTES = 64             # Bytes esperados en la respuesta (ajustar según tu dispositivo)


def leer_instancia_ensamblaje(driver: CIPDriver, instancia: int) -> bytes | None:
    """
    Envía un mensaje CIP genérico para leer una instancia de ensamblaje.

    Servicio:  Get Attribute Single (0x0E) o Get Attributes All (0x01)
    Clase:     Assembly (0x04)
    Instancia: la indicada por parámetro
    """
    try:
        respuesta = driver.generic_message(
            service=Services.get_attributes_all,   # 0x01
            class_code=ClassCode.assembly,          # 0x04
            instance=instancia,
            data_format=None,                       # datos crudos
            connected=False,
            unconnected_send=True,
        )

        if respuesta.error is None and respuesta.value is not None:
            return bytes(respuesta.value)
        else:
            print(f"  ⚠  Error en respuesta CIP: {respuesta.error}")
            return None

    except Exception as e:
        print(f"  ✖  Excepción al leer instancia {instancia}: {e}")
        return None


def interpretar_datos(datos: bytes):
    """
    Interpreta los bytes recibidos de la instancia de ensamblaje.
    Ajusta los formatos según la estructura real de tu dispositivo.
    """
    print(f"\n{'═' * 60}")
    print(f"  Datos crudos ({len(datos)} bytes):")
    print(f"  HEX: {datos.hex(' ')}")
    print(f"{'─' * 60}")

    # ── Ejemplo: interpretar como enteros de 16 bits (SINT/INT) ──
    n_int16 = len(datos) // 2
    if n_int16 > 0:
        valores_int16 = struct.unpack_from(f"<{n_int16}h", datos)
        print(f"  Como INT16 (little-endian):")
        for i, val in enumerate(valores_int16):
            print(f"    [{i:3d}] = {val}")

    # ── Ejemplo: interpretar como enteros de 32 bits (DINT) ──
    n_int32 = len(datos) // 4
    if n_int32 > 0:
        valores_int32 = struct.unpack_from(f"<{n_int32}i", datos)
        print(f"\n  Como INT32 (little-endian):")
        for i, val in enumerate(valores_int32):
            print(f"    [{i:3d}] = {val}")

    # ── Ejemplo: interpretar como flotantes de 32 bits (REAL) ──
    n_float = len(datos) // 4
    if n_float > 0:
        valores_float = struct.unpack_from(f"<{n_float}f", datos)
        print(f"\n  Como REAL/FLOAT32 (little-endian):")
        for i, val in enumerate(valores_float):
            print(f"    [{i:3d}] = {val:.4f}")

    # ── Ejemplo: interpretar como bits individuales (BOOL) ──
    print(f"\n  Primer byte como bits (BOOL):")
    if len(datos) >= 1:
        byte0 = datos[0]
        for bit in range(8):
            estado = bool(byte0 & (1 << bit))
            print(f"    Bit {bit} = {estado}")

    print(f"{'═' * 60}\n")


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Lector EtherNet/IP  –  Instancia de Ensamblaje       ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║   IP:        {PLC_IP:<43}║")
    print(f"║   Instancia: {ASSEMBLY_INSTANCE:<43}║")
    print("╚══════════════════════════════════════════════════════════╝\n")

    try:
        with CIPDriver(PLC_IP) as driver:
            print(f"  ✔  Conectado a {PLC_IP}\n")

            while True:
                datos = leer_instancia_ensamblaje(driver, ASSEMBLY_INSTANCE)

                if datos is not None:
                    interpretar_datos(datos)
                else:
                    print("  ✖  No se recibieron datos.\n")

                time.sleep(INTERVALO_LECTURA)

    except KeyboardInterrupt:
        print("\n  ■  Lectura detenida por el usuario.")
        sys.exit(0)

    except Exception as e:
        print(f"\n  ✖  Error de conexión: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
