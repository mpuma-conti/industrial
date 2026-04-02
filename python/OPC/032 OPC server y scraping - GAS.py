#para OPC server
import asyncio
import logging
from asyncua import Server, ua
from asyncua.common.methods import uamethod

#para scraping
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning #para desactivar advertencias de SSL sin verificar
import json
from bs4 import BeautifulSoup

#para fecha y hora
from datetime import datetime

# Desactivar todas las advertencias InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@uamethod
def func(parent, value):
    return value * 2


async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://10.10.10.217:49370")

    # set up our own namespace, not really necessary but should as spec
    uri = "OPC_SIMULATION_SERVER"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "EstacionDeGas")
    
    PresionCarreta01 = await myobj.add_variable(idx, "PresionCarreta01", 0.0)
    PresionCarreta02 = await myobj.add_variable(idx, "PresionCarreta02", 0.0)
    VolAcumNoCorreg = await myobj.add_variable(idx, "VolAcumNoCorreg", 0.0)
    VolAcumCorreg = await myobj.add_variable(idx, "VolAcumCorreg", 0.0)
    FlujoSalida = await myobj.add_variable(idx, "FlujoSalida", 0.0)
    
    # Set MyVariable to be writable by clients
    await PresionCarreta01.set_writable()
    await PresionCarreta02.set_writable()
    await VolAcumNoCorreg.set_writable()
    await VolAcumCorreg.set_writable()
    await FlujoSalida.set_writable()
    
    await server.nodes.objects.add_method(
        ua.NodeId("ServerMethod", idx),
        ua.QualifiedName("ServerMethod", idx),
        func,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )
    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1) #tiempo de espera en segundos

            ####INICIA SCRAPING
            login_url = "https://scadaflex.online/Account/Login?ReturnUrl=%2F" 
            login = "[EMAIL_ADDRESS]" 
            password = "[PASSWORD]" 

            with requests.session() as s: 
                    s.verify = False # Desactivar la verificación del certificado SSL
                    req = s.get(login_url).text 
                    html = BeautifulSoup(req,"html.parser") 
                    token = html.find("input", {"name": "__RequestVerificationToken"}). attrs["value"]

            payload = { 

                    "Input.Login": login, 
                    "Input.Password": password, 
                    "__RequestVerificationToken": token, 
                    "Input.RememberMe: ": "true" 
            }

            res = s.post(login_url, data=payload) 
            print(res.url)
            print(res.status_code) # If the request went Ok we usually get a 200 status.

            #PresionCarreta01
            Medidas_url = "https://scadaflex.online/api/variable/38572" 
            r = s.get(Medidas_url) 
            soup = BeautifulSoup(r.content, "html.parser")
            # Convertir el contenido de la respuesta en una cadena
            json_text = soup.get_text()
            # Cargar el JSON en un diccionario
            data = json.loads(json_text)
            # Acceder al valor de la clave "valorConv"
            new_val_PresionCarreta01 = data["valorConv"]

            #PresionCarreta02
            Medidas_url = "https://scadaflex.online/api/variable/38573" 
            r = s.get(Medidas_url) 
            soup = BeautifulSoup(r.content, "html.parser")
            # Convertir el contenido de la respuesta en una cadena
            json_text = soup.get_text()
            # Cargar el JSON en un diccionario
            data = json.loads(json_text)
            # Acceder al valor de la clave "valorConv"
            new_val_PresionCarreta02 = data["valorConv"]

            #VolAcumNoCorreg
            Medidas_url = "https://scadaflex.online/api/variable/38574" 
            r = s.get(Medidas_url) 
            soup = BeautifulSoup(r.content, "html.parser")
            # Convertir el contenido de la respuesta en una cadena
            json_text = soup.get_text()
            # Cargar el JSON en un diccionario
            data = json.loads(json_text)
            # Acceder al valor de la clave "valorConv"
            new_val_VolAcumNoCorreg = data["valorConv"]

            #VolAcumCorreg
            Medidas_url = "https://scadaflex.online/api/variable/38577" 
            r = s.get(Medidas_url) 
            soup = BeautifulSoup(r.content, "html.parser")
            # Convertir el contenido de la respuesta en una cadena
            json_text = soup.get_text()
            # Cargar el JSON en un diccionario
            data = json.loads(json_text)
            # Acceder al valor de la clave "valorConv"
            new_val_VolAcumCorreg = data["valorConv"]

            #FlujoSalida
            Medidas_url = "https://scadaflex.online/api/variable/38576" 
            r = s.get(Medidas_url) 
            soup = BeautifulSoup(r.content, "html.parser")
            # Convertir el contenido de la respuesta en una cadena
            json_text = soup.get_text()
            # Cargar el JSON en un diccionario
            data = json.loads(json_text)
            # Acceder al valor de la clave "valorConv"
            new_val_FlujoSalida = data["valorConv"]
            
            ####FIN SCRAPING

            fecha_hora_actual = datetime.now()
            cadena_fecha_hora = fecha_hora_actual.strftime("%d-%b-%Y %I:%M:%S %p")
            print(cadena_fecha_hora)
            
            _logger.error("Set value of %s to %.1f", PresionCarreta01, new_val_PresionCarreta01)
            await PresionCarreta01.write_value(new_val_PresionCarreta01)
            _logger.error("Set value of %s to %.1f", PresionCarreta02, new_val_PresionCarreta02)
            await PresionCarreta02.write_value(new_val_PresionCarreta02)
            _logger.error("Set value of %s to %.1f", VolAcumNoCorreg, new_val_VolAcumNoCorreg)
            await VolAcumNoCorreg.write_value(new_val_VolAcumNoCorreg)
            _logger.error("Set value of %s to %.1f", VolAcumCorreg, new_val_VolAcumCorreg)
            await VolAcumCorreg.write_value(new_val_VolAcumCorreg)
            _logger.error("Set value of %s to %.1f", FlujoSalida, new_val_FlujoSalida)
            await FlujoSalida.write_value(new_val_FlujoSalida)

            await asyncio.sleep(300) #tiempo de espera en segundos


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=False)
