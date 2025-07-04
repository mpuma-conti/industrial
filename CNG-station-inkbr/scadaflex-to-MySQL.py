import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from bs4 import BeautifulSoup
import mariadb
from datetime import datetime
import time
import logging

# Desactivar advertencias SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configurar el log
logging.basicConfig(level=logging.INFO)

# Configura tu conexión MySQL
conn = mariadb.connect(
    host='localhost',
    user='root',
    password='PASSWORD',
    database='sensores'
)
cursor = conn.cursor()

# Iniciar sesión
login_url = "https://scadaflex.online/Account/Login?ReturnUrl=%2F"
login = "USERNAME"  # Reemplaza con tu nombre de usuario
password = "PASSWORD"  # Reemplaza con tu contraseña

with requests.session() as s:
    s.verify = False
    req = s.get(login_url).text
    html = BeautifulSoup(req, "html.parser")
    token = html.find("input", {"name": "__RequestVerificationToken"}).attrs["value"]

    payload = {
        "Input.Login": login,
        "Input.Password": password,
        "__RequestVerificationToken": token,
        "Input.RememberMe": "true"
    }

    res = s.post(login_url, data=payload)
    logging.info(f"Login status: {res.status_code} - {res.url}")

def obtener_valor_variable(session, url):
    r = session.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    json_text = soup.get_text()
    data = json.loads(json_text)
    return data["valorConv"]

def main():
    repeticiones = 96  # Número de veces que se repite el ciclo (cada 5 min = 8 horas)
    for i in range(repeticiones):
        try:
            logging.info(f"--- Ciclo {i+1} de {repeticiones} ---")

            # Obtener valores
            new_val_PresionCarreta01 = obtener_valor_variable(s, "https://scadaflex.online/api/variable/38572")
            new_val_PresionCarreta02 = obtener_valor_variable(s, "https://scadaflex.online/api/variable/38573")
            new_val_VolAcumNoCorreg  = obtener_valor_variable(s, "https://scadaflex.online/api/variable/38574")
            new_val_VolAcumCorreg    = obtener_valor_variable(s, "https://scadaflex.online/api/variable/38577")
            new_val_FlujoSalida      = obtener_valor_variable(s, "https://scadaflex.online/api/variable/38576")

            # Timestamp
            fecha_hora_actual = datetime.now()
            cadena_fecha_hora = fecha_hora_actual.strftime("%d-%b-%Y %I:%M:%S %p")
            logging.info(f"Hora de recolección: {cadena_fecha_hora}")

            # Insertar en la base de datos
            insert_query = """
                INSERT INTO estacion_gas (
                    `PresionCarreta01_[bar]`,
                    `PresionCarreta02_[bar]`,
                    `FlujoSalida_[m3/h]`,
                    `VolAcumCorreg_[m3]`,
                    `VolAcumNoCorreg_[m3]`
                ) VALUES (%s, %s, %s, %s, %s)
            """

            data = (
                new_val_PresionCarreta01,
                new_val_PresionCarreta02,
                new_val_FlujoSalida,
                new_val_VolAcumCorreg,
                new_val_VolAcumNoCorreg
            )

            cursor.execute(insert_query, data)
            conn.commit()
            logging.info("Datos insertados correctamente")

        except Exception as e:
            logging.error(f"Error durante la ejecución: {e}")

        # Esperar 5 minutos antes del siguiente ciclo
        if i < repeticiones - 1:
            time.sleep(300)

if __name__ == "__main__":
    try:
        main()
    finally:
        cursor.close()
        conn.close()
        logging.info("Conexión cerrada. Script finalizado tras 96 ciclos.")
