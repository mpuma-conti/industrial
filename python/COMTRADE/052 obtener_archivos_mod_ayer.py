from ftplib import FTP
import datetime

# Función para obtener la lista de archivos modificados ayer de una extensión específica
def get_files_modified_yesterday_with_extension(ftp, folder, extension):
    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(days=1)
    ftp.cwd(folder)
    file_list = []
    ftp.dir(file_list.append)
    modified_yesterday = []
    for line in file_list:
        info = line.split()
        file_name = info[-1]
        month = info[-4]
        day = int(info[-3])
        modification_date = datetime.datetime(today.year, datetime.datetime.strptime(month, "%b").month, day)
        if file_name.endswith(extension) and modification_date.date() == yesterday:
            modified_yesterday.append(file_name)
    return modified_yesterday

# Conexión FTP
ftp = FTP('10.10.10.27')
ftp.login(user='user1', passwd='0')  # Ingresa tus credenciales si es necesario

# Ruta a la carpeta donde se encuentran los archivos en el servidor FTP
folder_path = '/COMTRADE_1'

# Obtener la lista de archivos modificados ayer con extensión .cfg
cfg_files_modified_yesterday = get_files_modified_yesterday_with_extension(ftp, folder_path, '.cfg')
# Obtener la lista de archivos modificados ayer con extensión .dat
#dat_files_modified_yesterday = get_files_modified_yesterday_with_extension(ftp, folder_path, '.dat')

# Mostrar los archivos modificados ayer con extensión .cfg y .dat
#for cfg_file, dat_file in zip(cfg_files_modified_yesterday, dat_files_modified_yesterday):
#    print("Archivo .cfg:", cfg_file)
#    print("Archivo .dat:", dat_file)

# Cerrar conexión FTP

ftp.quit()

print(cfg_files_modified_yesterday)
