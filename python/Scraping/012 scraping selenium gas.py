""" se subio el script a servidor debian, se tuvo que instalar google chrome desde el instalador debian, aparecieron errores de dependencias no instaladas, pero habia un comando de apt-get install para instalar las dependencias faltantes
la ruta donde esta el script es /opt/bitnami/wordpress/inkabor/selenium_gas_scada.py
se descargo la fuente Aptos en esa ruta, es importante detallar la ruta completa a la fuente y a la salida donde generará la imagen
se probo con el comando 
python3 selenium_gas_scada.py
ejecute crontab -e
agregue a las 00:31
*/5 * * * * /usr/bin/python3 /opt/bitnami/wordpress/inkabor/selenium_gas_scada.py
con ello deberia repetirse cada 5 minutos
el log para verificar a que hora y si ejecuta la tarea crontab está en
sudo nano /var/log/syslog """


import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Configurar las opciones para el modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Es importante deshabilitar la GPU en modo headless

# Inicializar el controlador de Selenium (por ejemplo, ChromeDriver)
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=chrome_options)

# Iniciar sesión en el sitio web
login_url = 'https://scadaflex.online/Account/Login?ReturnUrl=%2F'
username = ''
password = ''

driver.get(login_url)

# Localizar y llenar los campos de usuario y contraseña
username_field = driver.find_element(By.ID, "Input_Login") # Cambia el selector según tu página
password_field = driver.find_element(By.ID, 'Input_Password')  # Cambia el selector según tu página
username_field.send_keys(username)
password_field.send_keys(password)

# Enviar el formulario de inicio de sesión
login_button = driver.find_element(By.XPATH, '//button')  # Cambia el selector según tu página
login_button.click()

# Esperar un momento para que la página de inicio de sesión termine de cargar
time.sleep(3)

# Navegar a la URL donde se tomará la captura de pantalla
captura_url = 'https://scadaflex.online/localdata/drawing/10_1653_0005.svg?CodEst=866'
driver.get(captura_url)

# Esperar un momento para que la página cargue completamente
time.sleep(3)

driver.set_window_size(1460, 920)

# Definir las coordenadas de la porción de la página que deseas capturar
x = 100  # coordenada x del inicio
y = 0  # coordenada y del inicio
width = 1290  # ancho de la porción 1290
height = 810  # altura de la porción 780

#Ejecutar JavaScript para cambiar el nivel de zoom a 60%
#driver.execute_script("document.body.style.zoom='60%'")
#Al ser un objeto SVG no aplica esa funcion js

# Access each dimension individually
##width_ = driver.get_window_size().get("width")
##height_ = driver.get_window_size().get("height")
##print(width_)
##print(height_)

driver.set_window_size(1440, 900)
# Realizar un scroll 375 horizontal y 100 vertical
script = "window.scrollBy(375, 100);"
driver.execute_script(script)
# Maximiza a pantalla completa
driver.fullscreen_window()

# Tomar una captura de pantalla de la porción especificada
# screenshot = driver.get_screenshot_as_png()
screenshot = driver.get_screenshot_as_png()

# Crear una imagen recortada a partir de la captura de pantalla completa
from PIL import Image
from io import BytesIO
image = Image.open(BytesIO(screenshot))
cropped_image = image.crop((x, y, x + width, y + height))

# Obtener fecha y hora
import datetime

# Obtener la fecha y hora actual
now = datetime.datetime.now()
# Redondear los minutos al múltiplo de 5 más cercano
rounded_minutes = (now.minute // 5) * 5
# Crear una nueva fecha y hora con los minutos redondeados
rounded_time = now.replace(minute=rounded_minutes)
# Formatear la fecha y hora en el formato deseado
formatted_time = rounded_time.strftime('%d-%b-%Y %I:%M %p')

# Agregar esa fecha y hora a la imagen recortada
from PIL import ImageDraw
from PIL import ImageFont
# Agregar texto a la imagen
draw = ImageDraw.Draw(cropped_image)
font_size = 28
font = ImageFont.truetype("aptos.ttf", font_size)
#font = ImageFont.load_default()  # Utiliza la fuente preinstalada
text = "Datos obtenidos el " + formatted_time
position = (400, 0)  # Coordenadas donde se agregará el texto
draw.text(position, text, font=font, fill="blue")  # Puedes cambiar el color de relleno


# Guardar la imagen recortada
cropped_image.save('ruta_de_salida.png')




# Cerrar el controlador de Selenium
driver.quit()
