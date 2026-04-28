from ftplib import FTP
import datetime

# Función para obtener la lista de archivos modificados entre las 06:00 de ayer y 06:00 de hoy de una extensión específica
def get_files_modified_between_6am_yesterday_and_6am_today(ftp, folder, extension):
    today = datetime.datetime.now()
    # Establecer la hora de inicio (06:00 de ayer)
    start_time = datetime.datetime.combine(today.date() - datetime.timedelta(days=1), datetime.time(11, 0))
    # Establecer la hora de fin (06:00 de hoy)
    end_time = datetime.datetime.combine(today.date(), datetime.time(11, 0))
    ftp.cwd(folder)
    file_list = []
    ftp.dir(file_list.append)
    modified_between_6am_yesterday_and_6am_today = []
    for line in file_list:
        info = line.split()
        file_name = info[-1]
        month = info[-4]
        day = int(info[-3])
        hour, minute = map(int, info[-2].split(':')) # la hora es UTC-0
        modification_date = datetime.datetime(today.year, datetime.datetime.strptime(month, "%b").month, day, hour, minute)
        if file_name.endswith(extension) and start_time <= modification_date < end_time:
            modified_between_6am_yesterday_and_6am_today.append(file_name)
    return modified_between_6am_yesterday_and_6am_today

# Conexión FTP
ftp = FTP('10.10.10.27')
ftp.login(user='user1', passwd='0')  # Ingresa tus credenciales si es necesario

# Ruta a la carpeta donde se encuentran los archivos en el servidor FTP
folder_path = '/COMTRADE_1'

# Obtener la lista de archivos modificados ayer con extensión .cfg
#cfg_files_modified_yesterday = get_files_modified_between_6am_yesterday_and_6am_today(ftp, folder_path, '.cfg')
# Obtener la lista de archivos modificados ayer con extensión .dat
dat_files_modified_yesterday = get_files_modified_between_6am_yesterday_and_6am_today(ftp, folder_path, '.dat')

import comtrade
import os

local_path = 'C:\\users\\mantto\\Schneider-ION-waveform\\'   # Ruta local donde se guardará el archivo

for filename_with_extension in dat_files_modified_yesterday:
    filename = filename_with_extension.split(".")[0]
    # Apertura de archivo local para escritura en modo binario
    with open(local_path + filename + '.dat', 'wb') as local_file:
        # Descarga del archivo desde el servidor FTP
        ftp.retrbinary('RETR ' + filename + '.dat', local_file.write)
    with open(local_path + filename + '.cfg', 'wb') as local_file:
        # Descarga del archivo desde el servidor FTP
        ftp.retrbinary('RETR ' + filename + '.cfg', local_file.write)

    # Decodificado de COMTRADE y conversion a csv
    rec = comtrade.load(local_path + filename + '.cfg', local_path + filename + '.dat')
    df = rec.to_dataframe()
    #print(df.head())
    df.to_csv(local_path + filename + '.csv')

    os.remove(local_path + filename + '.dat')
    os.remove(local_path + filename + '.cfg')


# Cerrar conexión FTP
ftp.quit()

