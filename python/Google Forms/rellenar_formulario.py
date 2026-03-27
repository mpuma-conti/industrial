"""
Script para rellenar automáticamente el formulario de Diagnóstico Situacional - INKABOR
https://docs.google.com/forms/d/e/1FAIpQLScaWvd7y5wFQ33Mua85H6O4REul9twEjfzJRJkxo-3z8rOzQw/viewform

Uso:
    1. Edita el array EMPLEADOS con los datos de cada persona
    2. Edita PUESTO_DE_TRABAJO con el puesto
    3. Ejecuta: python rellenar_formulario.py
"""

import requests
import time
import random

# ============================================================
# ========== CONFIGURACIÓN - EDITA ESTOS VALORES =============
# ============================================================

# Lista de empleados: cada entrada es (Nombre y apellidos, Edad)
EMPLEADOS = [
    ("E V N H", "58"),
    ("Y G R M", "63"),
    # Agrega más empleados aquí...
]

# Puesto de trabajo (se aplica a todos los empleados)
PUESTO_DE_TRABAJO = "Técnico"

# Área (no modificar - siempre "Operativa" según requerimiento)
AREA = "Operativa"

# ============================================================
# ======= RESPUESTAS POR DEFECTO PARA LAS ESCALAS ===========
# ============================================================
# Puedes cambiar las respuestas por defecto para cada escala.
# Opciones para EAMD y EAA:
#   "Nunca o casi nunca"
#   "A veces"
#   "Con bastante frecuencia"
#   "Siempre o casi siempre"
#
# Opciones para PSS:
#   "Nunca"
#   "Casi nunca"
#   "De vez en cuando"
#   "A menudo"
#   "Muy a menudo"

RESPUESTA_EAMD = "Nunca o casi nunca"  # Respuesta para Escala de Depresión
RESPUESTA_EAA  = "Con bastante frecuencia"  # Respuesta para Escala de Ansiedad
RESPUESTA_PSS  = "A menudo"               # Respuesta para Escala de Estrés

# ============================================================
# ============= NO MODIFICAR DEBAJO DE ESTA LÍNEA ============
# ============================================================

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScaWvd7y5wFQ33Mua85H6O4REul9twEjfzJRJkxo-3z8rOzQw/formResponse"

# Entry IDs del formulario
ENTRY_NOMBRE       = "entry.568987592"
ENTRY_EDAD         = "entry.1104962388"
ENTRY_PUESTO       = "entry.1774388143"
ENTRY_AREA         = "entry.90614253"

# Escala de Automedición de Depresión (EAMD) - 20 preguntas
ENTRIES_EAMD = [
    "entry.1386631214",   # 1. Me siento triste y decaído
    "entry.769143692",    # 2. Por las mañanas me siento mejor
    "entry.500312744",    # 3. Tengo accesos de llanto o deseos de llorar
    "entry.2026972829",   # 4. Tengo problemas para dormir por la noche
    "entry.921694993",    # 5. Tengo tanto apetito como antes
    "entry.1070950698",   # 6. Aún tengo deseos sexuales
    "entry.195391198",    # 7. Noto que estoy perdiendo peso
    "entry.1000345293",   # 8. Tengo trastornos intestinales (estreñimiento)
    "entry.1967555377",   # 9. Me late el corazón más a prisa que de costumbre
    "entry.1821535271",   # 10. Me canso sin motivo
    "entry.1613043866",   # 11. Tengo la mente tan clara como antes
    "entry.379651321",    # 12. Hago las cosas con la misma facilidad que antes
    "entry.1049448605",   # 13. Me siento nervioso y no puedo estar quieto
    "entry.1223998476",   # 14. Tengo esperanza en el futuro
    "entry.1939042470",   # 15. Estoy más irritable que antes
    "entry.2108300940",   # 16. Me es fácil tomar decisiones
    "entry.20273643",     # 17. Me siento útil y necesario
    "entry.1278257706",   # 18. Me satisface mi vida actual
    "entry.444146401",    # 19. Creo que los demás estarían mejor si yo muriera
    "entry.209562016",    # 20. Disfruto de las mismas cosas que antes
]

# Escala de Autoevaluación de Ansiedad (EAA) - 20 preguntas
ENTRIES_EAA = [
    "entry.616349369",    # 1. Me siento más nervioso y ansioso que de costumbre
    "entry.11542165",     # 2. Me siento con temor sin razón
    "entry.1942959440",   # 3. Despierto con facilidad o siento pánico
    "entry.270949879",    # 4. Me siento como si fuera a reventar y partirme en pedazos
    "entry.1564045371",   # 5. Siento que todo está bien y que nada malo puede suceder
    "entry.870893591",    # 6. Me tiemblan los brazos y las piernas
    "entry.1053237044",   # 7. Me mortifican dolores de cabeza, cuello o cintura
    "entry.1673058899",   # 8. Me siento débil y me canso fácilmente
    "entry.1896002602",   # 9. Me siento tranquilo y puedo permanecer en calma
    "entry.196083300",    # 10. Puedo sentir que me late muy rápido el corazón
    "entry.641514",       # 11. Sufro de mareos
    "entry.1514562409",   # 12. Sufro de desmayos o siento que me voy a desmayar
    "entry.441050847",    # 13. Puedo inspirar y expirar fácilmente
    "entry.1657361089",   # 14. Se me adormecen o me hincan los dedos de manos y pies
    "entry.1195037389",   # 15. Sufro de molestias estomacales o indigestión
    "entry.482813011",    # 16. Orino con mucha frecuencia
    "entry.416296821",    # 17. Generalmente mis manos están secas y calientes
    "entry.702626457",    # 18. Siento bochornos
    "entry.1662145480",   # 19. Me quedo dormido con facilidad y descanso bien
    "entry.390917577",    # 20. Tengo pesadillas
]

# Escala de Estrés Percibido (PSS) - 14 preguntas
ENTRIES_PSS = [
    "entry.1011052750",   # 1. ¿Ha estado afectado por algo que ha ocurrido inesperadamente?
    "entry.325107787",    # 2. ¿Se ha sentido incapaz de controlar las cosas importantes?
    "entry.1386887253",   # 3. ¿Se ha sentido nervioso o estresado?
    "entry.757707099",    # 4. ¿Ha manejado con éxito los pequeños problemas irritantes?
    "entry.955116344",    # 5. ¿Ha sentido que ha afrontado efectivamente los cambios importantes?
    "entry.2053023121",   # 6. ¿Se ha sentido seguro sobre su capacidad para manejar problemas?
    "entry.702626457",    # 7. ¿Ha sentido que las cosas le van bien?
    "entry.623718740",    # 8. ¿Ha sentido que no podía afrontar todas las cosas que tenía que hacer?
    "entry.1090390392",   # 9. ¿Ha podido controlar las dificultades de su vida?
    "entry.521989929",    # 10. ¿Ha sentido que tenía todo bajo control?
    "entry.1097110866",   # 11. ¿Se ha enfadado porque las cosas estaban fuera de su control?
    "entry.1144968731",   # 12. ¿Ha pensado sobre las cosas que le quedan por hacer?
    "entry.1662145480",   # 13. ¿Ha podido controlar la forma de pasar el tiempo?
    "entry.390917577",    # 14. ¿Ha sentido que las dificultades se acumulan tanto que no puede superarlas?
]


def enviar_formulario(nombre, edad, puesto, area, resp_eamd, resp_eaa, resp_pss):
    """Envía una respuesta completa al formulario de Google."""
    
    data = {
        ENTRY_NOMBRE: nombre,
        ENTRY_EDAD: edad,
        ENTRY_PUESTO: puesto,
        ENTRY_AREA: area,
    }
    
    # Rellenar escala EAMD (Depresión)
    for entry_id in ENTRIES_EAMD:
        data[entry_id] = resp_eamd
    
    # Rellenar escala EAA (Ansiedad)
    for entry_id in ENTRIES_EAA:
        data[entry_id] = resp_eaa
    
    # Rellenar escala PSS (Estrés)
    for entry_id in ENTRIES_PSS:
        data[entry_id] = resp_pss
    
    try:
        response = requests.post(FORM_URL, data=data)
        if response.status_code == 200:
            return True, "✅ Enviado correctamente"
        else:
            return False, f"❌ Error HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"❌ Error de conexión: {e}"


def main():
    print("=" * 60)
    print("  INKABOR - Rellenado Automático de Formulario")
    print("  Diagnóstico Situacional de Salud Mental")
    print("=" * 60)
    print(f"\n  Puesto de trabajo: {PUESTO_DE_TRABAJO}")
    print(f"  Área: {AREA}")
    print(f"  Total empleados: {len(EMPLEADOS)}")
    print(f"\n  Respuestas por defecto:")
    print(f"    EAMD (Depresión): {RESPUESTA_EAMD}")
    print(f"    EAA  (Ansiedad):  {RESPUESTA_EAA}")
    print(f"    PSS  (Estrés):    {RESPUESTA_PSS}")
    print("=" * 60)
    
    exitosos = 0
    fallidos = 0
    
    for i, (nombre, edad) in enumerate(EMPLEADOS, 1):
        print(f"\n[{i}/{len(EMPLEADOS)}] Enviando: {nombre} (Edad: {edad})...", end=" ")
        
        exito, mensaje = enviar_formulario(
            nombre=nombre,
            edad=edad,
            puesto=PUESTO_DE_TRABAJO,
            area=AREA,
            resp_eamd=RESPUESTA_EAMD,
            resp_eaa=RESPUESTA_EAA,
            resp_pss=RESPUESTA_PSS,
        )
        
        print(mensaje)
        
        if exito:
            exitosos += 1
        else:
            fallidos += 1
        
        # Pausa entre envíos para no saturar el servidor
        if i < len(EMPLEADOS):
            pausa = random.uniform(1, 3)
            print(f"    ⏳ Esperando {pausa:.1f}s...")
            time.sleep(pausa)
    
    print("\n" + "=" * 60)
    print(f"  RESUMEN: {exitosos} exitosos, {fallidos} fallidos de {len(EMPLEADOS)} total")
    print("=" * 60)


if __name__ == "__main__":
    main()
