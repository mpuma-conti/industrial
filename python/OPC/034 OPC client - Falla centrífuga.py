import asyncio
from asyncua import Client

#para fecha y hora
from datetime import datetime

# Assuming these are your Gmail credentials
gmail_user = "[EMAIL_ADDRESS]"
gmail_password = "[PASSWORD]"  # Use app password for security

url = "opc.tcp://10.10.10.23:49370" #Kepserver  
#namespace = "KEPServer"

async def main():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        #nsidx = await client.get_namespace_index(namespace)
        #print(f"Namespace Index for '{namespace}': {nsidx}")

        nsidx = 2 #me di cuenta que el valor es 2

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
                ["0:Objects", f"{nsidx}:PLC_TM221_Inkabor", f"{nsidx}:PLC_MS210", f"{nsidx}:Falla"]
        )

        # Inicializa el contador
        contador = 0
        estado_anterior = False
        
        while True:
            
            value = await var.read_value()
            #print(f"Value of FALLA EN VARIADOR ({var}): {value}")

            # Check if the value is different
            if value == True and estado_anterior == False:
                #fecha hora
                fecha_hora_actual = datetime.now()
                cadena_fecha_hora = fecha_hora_actual.strftime("%d-%b-%Y %I:%M:%S %p")
                print(cadena_fecha_hora)

                contador += 1
                print("Evento número:", contador)
                print(f"Value of FALLA EN VARIADOR ({var}): {value}")
                # Send email
                
            estado_anterior = value
            # Cerrar la sesión explícitamente
            #await client.close_session()
            await asyncio.sleep(60)        

        
if __name__ == "__main__":
    asyncio.run(main())
