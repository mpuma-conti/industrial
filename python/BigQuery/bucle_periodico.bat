@echo off
:loop
rem Ejecutar el script de Python aquí
python "C:\Users\mantto2\Desktop\Codigos Python\BigQuery\bases de datos_MSSQL to BigQuery.py"

rem Esperar 8 horas (en segundos) antes de ejecutar nuevamente
timeout /t 28800 /nobreak

goto loop