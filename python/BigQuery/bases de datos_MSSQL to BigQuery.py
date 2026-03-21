import pyodbc
from google.cloud import bigquery
from google.oauth2 import service_account

# Ruta al archivo JSON de credenciales, utilizar un prefijo de cadena cruda (r) antes de la cadena para indicar que no se deben interpretar secuencias de escape en esa cadena. Esto es útil cuando trabajas con rutas de archivo en Windows.
# se creo clave json, esta en https://console.cloud.google.com/iam-admin/serviceaccounts/details/100417657165292125041?hl=es-419&project=spatial-dryad-246322
ruta_credenciales = r'C:\Users\mantto2\Desktop\Codigos Python\BigQuery\spatial-dryad-246322-df7908d17aff.json'
# Cargar las credenciales desde el archivo JSON
credenciales = service_account.Credentials.from_service_account_file(
    ruta_credenciales,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
# Crear un cliente de BigQuery
client = bigquery.Client(credentials=credenciales)

# Configurar los detalles de la tabla
dataset_id = 'inkabor'
table_id = 'tagsScada'
table_ref = client.dataset(dataset_id).table(table_id)

#############################
## Base de datos SQL Server 1
#############################
# Configuración de la conexión a SQL Server
sql_server_conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=APP-SRV-01;"
    "DATABASE=DB_SERVICIOS;"
    "UID=Erwin;"
    "PWD=Inkabor999;"
)
# Crear cursor para conexion SQL
sql_server_cursor = sql_server_conn.cursor()

# Define la lista de relaciones entre "NombreTag" y "TagIndex", esto se obtiene de la tabla TagIndex en la Base de datos del SCADA
mapeo_tag = [
    ("PI24", "38"),
    ("PI23", "118"),
    # Agregar más relaciones aquí según sea necesario
]

# Iterar sobre las relaciones y realizar consultas y mapeo
for relacion in mapeo_tag:
    nombre_tag = relacion[0]
    tag_index = relacion[1]

    # Consulta para leer datos desde SQL Server con filtro WHERE
    sql_query = f"SELECT TOP (1) DateAndTime, TagIndex, Val FROM FloatTable WHERE TagIndex = '{tag_index}' ORDER BY DateAndTime DESC"

    # Ejecutar consulta en SQL Server
    sql_server_cursor.execute(sql_query)

    # Obtener los datos
    data_from_sql_server = sql_server_cursor.fetchall()

    if data_from_sql_server:
        fecha_hora = data_from_sql_server[0].DateAndTime.strftime('%Y-%m-%d %H:%M:%S')  # Convertir el objeto datetime a una cadena en formato YYYY-MM-DD HH:MM:SS que espera BigQuery
        tag_index = int(data_from_sql_server[0].TagIndex)
        valor = float(data_from_sql_server[0].Val)

        data = [
            {
                "Fecha_Hora": fecha_hora,
                "Nombre_Tag": nombre_tag,
                "TagIndex": tag_index,
                "Valor": valor
            }
        ]
        # Insertar los datos en la tabla
        errors = client.insert_rows_json(table_ref, data)
        if errors == []:
            print(f'Datos para NombreTag: {nombre_tag}, TagIndex: {tag_index} insertados correctamente en BigQuery.')
        else:
            print(f'Ocurrieron errores durante la inserción para NombreTag: {nombre_tag}, TagIndex: {tag_index}: {errors}')
    else:
        print(f'No se encontraron datos para NombreTag: {nombre_tag}, TagIndex: {tag_index}.')


# Cerrar conexiones y cursores
sql_server_cursor.close()
sql_server_conn.close()

#############################
## Base de datos SQL Server 2
#############################
# Configuración de la conexión a SQL Server
sql_server_conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=APP-SRV-01;"
    "DATABASE=DB_BZ_FP;"
    "UID=Erwin;"
    "PWD=Inkabor999;"
)
# Crear cursor para conexion SQL
sql_server_cursor = sql_server_conn.cursor()

# Define la lista de relaciones entre "NombreTag" y "TagIndex", esto se obtiene de la tabla TagIndex en la Base de datos del SCADA
mapeo_tag = [
    ("PIK800A", "4"),
    ("PIK800B", "5"),
    ("PIK800C", "6"),
    # Agregar más relaciones aquí según sea necesario
]

# Iterar sobre las relaciones y realizar consultas y mapeo
for relacion in mapeo_tag:
    nombre_tag = relacion[0]
    tag_index = relacion[1]

    # Consulta para leer datos desde SQL Server con filtro WHERE
    sql_query = f"SELECT TOP (1) DateAndTime, TagIndex, Val FROM FloatTable WHERE TagIndex = '{tag_index}' ORDER BY DateAndTime DESC"

    # Ejecutar consulta en SQL Server
    sql_server_cursor.execute(sql_query)

    # Obtener los datos
    data_from_sql_server = sql_server_cursor.fetchall()

    if data_from_sql_server:
        fecha_hora = data_from_sql_server[0].DateAndTime.strftime('%Y-%m-%d %H:%M:%S')  # Convertir el objeto datetime a una cadena en formato YYYY-MM-DD HH:MM:SS que espera BigQuery
        tag_index = int(data_from_sql_server[0].TagIndex)
        valor = float(data_from_sql_server[0].Val)

        data = [
            {
                "Fecha_Hora": fecha_hora,
                "Nombre_Tag": nombre_tag,
                "TagIndex": tag_index,
                "Valor": valor
            }
        ]
        # Insertar los datos en la tabla
        errors = client.insert_rows_json(table_ref, data)
        if errors == []:
            print(f'Datos para NombreTag: {nombre_tag}, TagIndex: {tag_index} insertados correctamente en BigQuery.')
        else:
            print(f'Ocurrieron errores durante la inserción para NombreTag: {nombre_tag}, TagIndex: {tag_index}: {errors}')
    else:
        print(f'No se encontraron datos para NombreTag: {nombre_tag}, TagIndex: {tag_index}.')


# Cerrar conexiones y cursores
sql_server_cursor.close()
sql_server_conn.close()
