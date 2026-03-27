import datetime

# Obtener la fecha y hora actual
now = datetime.datetime.now()
# Redondear los minutos al múltiplo de 5 más cercano
rounded_minutes = (now.minute // 5) * 5
# Crear una nueva fecha y hora con los minutos redondeados
rounded_time = now.replace(minute=rounded_minutes)
# Formatear la fecha y hora en el formato deseado
formatted_time = rounded_time.strftime('%d-%b-%Y %I:%M %p')
print("Datos obtenidos el " + formatted_time)
