import requests
import json

# Variable a evaluar
mi_variable = "Start"  # Cambia este valor para probar

# Si el valor es diferente de 'Run', se envía el mensaje
if mi_variable != 'Run':
    url = "https://graph.facebook.com/v22.0/716318174890764/messages"
    headers = {
        "Authorization": "Bearer EAARMXPch1YcBPFS4SX2e7JdJQaVzDSkIbz9Hc6TZCREe2wp8uUZCoyPYhGjnruZBAaAnvpUnyUyBJKjYtnkcjKlUbp9ZARRak6HCMh18vukUbuAlDUYWijsNWD6uHrXKoXaHvLufZBs7QvoZA4EvL6oGk0TsMliTh27c1yM63XFGYuC9o60diCJwSRwDBZBA8IHwQhsG5d7KAM1UHwGnLF5P1Pb7oMiXBV2YbZANLW5tkMPgIWR2OdffUPT4O0PTpUkZD",
        "Content-Type": "application/json"
    }
    data = {
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

    response = requests.post(url, headers=headers, json=data)

    # Mostrar respuesta de la API
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
else:
    print("La variable es 'Run'. No se envía el mensaje.")