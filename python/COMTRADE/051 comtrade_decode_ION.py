import matplotlib.pyplot as plt
import comtrade
import pandas as pd
import os

# 1. Obtener la ruta exacta de la carpeta donde está tu script (.py)
directorio_base = os.path.dirname(os.path.abspath(__file__))

# 2. Unir esa ruta con tu carpeta "COMTRADE" y los nombres de los archivos
cfg_path = os.path.join(directorio_base, "COMTRADE", "cmt01305.cfg")
dat_path = os.path.join(directorio_base, "COMTRADE", "cmt01305.dat")

# 3. Cargar los archivos (ahora Python sabe exactamente dónde están)
rec = comtrade.load(cfg_path, dat_path)

print("================ METADATOS DEL ARCHIVO ================")
print(f"Estación / Planta:       {rec.station_name}")
print(f"Frecuencia del Sistema:  {rec.frequency} Hz")
print(f"Fecha y Hora de Inicio:  {rec.start_timestamp}")
print(f"Fecha y Hora de Disparo: {rec.trigger_timestamp}")

print("=======================================================")


print("Trigger time = {}s".format(rec.trigger_time))

# Convertir a DataFrame y mostrar
df = rec.to_dataframe()

# Crear una nueva columna de fecha y hora exacta sumando el tiempo relativo
df['Fecha_Hora_Real'] = rec.start_timestamp + pd.to_timedelta(df.index, unit='s')

# Reordenar para que sea la primera columna
columnas = ['Fecha_Hora_Real'] + [col for col in df.columns if col != 'Fecha_Hora_Real']
df = df[columnas]

print(df.head())

# Guardar el CSV en la misma carpeta que el script
csv_path = os.path.join(directorio_base, 'cmt01305.csv')
df.to_csv(csv_path)
print(f"¡Listo! Archivo CSV guardado en: {csv_path}")