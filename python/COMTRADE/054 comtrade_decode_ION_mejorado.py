# crea una columna de fecha y hora real a partir del tiempo relativo, y guarda todo en un archivo CSV con metadatos incluidos. La columna de fecha y hora se formatea como texto para evitar que Excel la convierta automáticamente a su formato de fecha.
import matplotlib.pyplot as plt
import comtrade
import pandas as pd
import os

# 1. Cargar el archivo
directorio_base = os.path.dirname(os.path.abspath(__file__))
cfg_path = os.path.join(directorio_base, "COMTRADE", "cmt01303.cfg")
dat_path = os.path.join(directorio_base, "COMTRADE", "cmt01303.dat")

rec = comtrade.load(cfg_path, dat_path)

# 2. Crear el DataFrame
df = rec.to_dataframe()

# 3. Crear la columna de Fecha y Hora Real y forzarla a TEXTO
# Sumamos el tiempo relativo a la fecha de inicio
fecha_hora = rec.start_timestamp + pd.to_timedelta(df.index, unit='s')

# Convertimos a texto (string) con formato explícito: Año-Mes-Día Hora:Min:Seg.Microsegundos
# El '%f' al final asegura que se guarden los milisegundos/microsegundos.
df.insert(0, 'Fecha_Hora_Real', fecha_hora.strftime('="%Y-%m-%d %H:%M:%S.%f"'))

# 4. Guardar en CSV con metadatos incluidos
csv_path = os.path.join(directorio_base, 'cmt01303.csv')

# Paso A: Abrimos el archivo en modo escritura ('w') y escribimos los metadatos como texto
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("================ METADATOS DEL ARCHIVO ================\n")
    f.write(f"Estacion / Planta:       {rec.station_name}\n")
    f.write(f"Frecuencia del Sistema:  {rec.frequency} Hz\n")
    f.write(f"Fecha y Hora de Inicio:  {rec.start_timestamp}\n")
    f.write(f"Fecha y Hora de Disparo: {rec.trigger_timestamp}\n")
    f.write(f"Hora del Disparo: {rec.trigger_time}\n")
    f.write("=======================================================\n")
    f.write("\n") # Una línea en blanco para separar los metadatos de la tabla

# Paso B: Anexamos la tabla debajo usando mode='a' (append)
# index=True mantiene la columna 'time' original (los segundos desde el inicio)
df.to_csv(csv_path, mode='a', index=True)

print(f"¡Listo! Archivo CSV guardado con metadatos y fechas blindadas contra Excel en: {csv_path}")