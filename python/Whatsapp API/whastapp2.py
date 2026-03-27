import time
import requests
from opcua import Client

# OPC UA server URL
opc_url = "opc.tcp://10.10.10.23:49370"

# WhatsApp API setup
whatsapp_url = "https://graph.facebook.com/v22.0/716318174890764/messages"
whatsapp_headers = {
    "Authorization": "Bearer EAARMXPch1YcBPNppubywtWfJ1wZAvZBrFsQmihFZCwfh3QegpGlRCGRdrRiQNrh3kxIC56Vsg7iRuPpbGBndIz5812lHdE5sfPJYD5UvbrgkCK1mthEaBD2yJ497Une9jcseWHVH4Km7bCJV3d4xsUk2EthSDRzWxgm9BdWNIFvKjVxhsgGVYFt3ApPPFQGyAZDZD",
    "Content-Type": "application/json"
}

whatsapp_data = {
    "messaging_product": "whatsapp",
    "to": "51973698506",
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {
            "code": "en_US"
        }
    }
}

# OPC UA node path
# node_id = "PLC_S_COMPR.S_COMPR.M251data.GVL_EPTSA_ESTADO"
node_id = "PLC_S_COMPR.S_COMPR.M251data.GVL_PE21"

# Connect to OPC UA
client = Client(opc_url)
try:
    client.connect()
    print("Conectado al servidor OPC UA")

    while True:
        try:
            # Obtener el valor
            node = client.get_node(f"ns=2;s={node_id}")
            valor = node.get_value()

            print(f"Valor leído: {valor}")

            # Enviar mensaje si el valor es diferente de 'Encendido'
            # if str(valor) != '8':
            if valor < 0.6:
                response = requests.post(whatsapp_url, headers=whatsapp_headers, json=whatsapp_data)
                print(f"WhatsApp Status: {response.status_code}")
                print(f"WhatsApp Response: {response.text}")
            else:
                print("El valor es 'mayor a 0.6'. No se envía mensaje.")

        except Exception as e:
            print(f"Error al leer OPC o enviar WhatsApp: {e}")

        time.sleep(60) # Esperar 60 segundos antes de la siguiente lectura

except Exception as e:
    print(f"Error de conexión OPC UA: {e}")
finally:
    client.disconnect()
    print("Desconectado del servidor OPC UA")