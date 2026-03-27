import pyodbc
import mysql.connector

# Configuración de la conexión a SQL Server
sql_server_conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=APP-SRV-01;"
    "DATABASE=DB_SERVICIOS;"
    "UID=Erwin;"
    "PWD=kabor999;"
)

# Configuración de la conexión a MySQL
mysql_conn = mysql.connector.connect(
    host="www.db4free.net",
    user="",
    password="",
    database=""
)

# Crear cursores para ambas conexiones
sql_server_cursor = sql_server_conn.cursor()
mysql_cursor = mysql_conn.cursor()

# Consulta para leer datos desde SQL Server con filtro WHERE
sql_query = "SELECT TOP (2) DateAndTime, TagIndex, Val FROM FloatTable WHERE TagIndex IN ('38', '118') ORDER BY DateAndTime DESC"

# Ejecutar consulta en SQL Server
sql_server_cursor.execute(sql_query)

# Obtener los datos
data_from_sql_server = sql_server_cursor.fetchall()
print(data_from_sql_server)

# Iterar sobre los datos y escribir en MySQL
for row in data_from_sql_server:
    insert_query = "INSERT INTO DB_SERVICIOS (FechaHora, TagIndex, Valor) VALUES (%s, %s, %s)"
    values = tuple(row)  # Asegurarse de que el orden coincida con las columnas en la tabla MySQL
    mysql_cursor.execute(insert_query, values)
    mysql_conn.commit()

# Cerrar conexiones y cursores
sql_server_cursor.close()
sql_server_conn.close()
mysql_cursor.close()
mysql_conn.close()
