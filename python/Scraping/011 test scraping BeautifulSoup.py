# basado en tutorial https://www.zenrows.com/blog/web-scraping-login-python#scraping-behind-the-login-on-waf-protected-websites

import requests
import json
from bs4 import BeautifulSoup

login_url = "https://scadaflex.online/Account/Login?ReturnUrl=%2F" 
login = "" 
password = "" 

with requests.session() as s: 
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

#obtuve la URL del codigo de webpack:///src/app/services/VariavelService.js
#https://scadaflex.online/Registration/Variable?CodMed=1278&CodEmpr=799 para ver la lista de variables y sus codigos
Medidas_url = "https://scadaflex.online/api/variable/38576" 
r = s.get(Medidas_url) 
soup = BeautifulSoup(r.content, "html.parser")

# Convertir el contenido de la respuesta en una cadena
json_text = soup.get_text()
# Cargar el JSON en un diccionario
data = json.loads(json_text)
# Acceder al valor de la clave "valorInteger"
valor_integer = data["valorInteger"]
print(valor_integer)

valor_integer = data["dataLeitura"]
print(valor_integer)