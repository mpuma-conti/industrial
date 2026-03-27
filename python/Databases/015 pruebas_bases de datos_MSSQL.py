import pyodbc

# Configuración de la conexión a SQL Server
sql_server_conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=APP-SRV-01;"
    "DATABASE=DB_CCM_ABG1;"
    "UID=Erwin;"
    "PWD=kabor999;"
)

# Crear cursores para ambas conexiones
sql_server_cursor = sql_server_conn.cursor()

# Consulta para leer datos desde SQL Server con filtro WHERE
#sql_query = "SELECT TOP (2) DateAndTime, TagIndex, Val FROM FloatTable WHERE TagIndex IN ('38', '35') ORDER BY DateAndTime DESC"
sql_query = "SELECT TOP (1) DateAndTime, TagIndex, Val FROM FloatTable WHERE TagIndex IN ('288') ORDER BY DateAndTime DESC"

# Ejecutar consulta en SQL Server
sql_server_cursor.execute(sql_query)

# Obtener los datos
data_from_sql_server = sql_server_cursor.fetchall()
print(data_from_sql_server)

# Cerrar conexiones y cursores
sql_server_cursor.close()
sql_server_conn.close()
