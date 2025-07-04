# SCADA Data Scraper for MySQL / MariaDB Integration

This Python script performs web scraping to retrieve data from a SCADA system and stores the collected data in a MySQL or MariaDB database. The stored data can later be analyzed or visualized using tools such as Power BI.

## Features

✅ Logs into a SCADA system using session authentication  
✅ Periodically scrapes variable values from specific API endpoints  
✅ Stores the data in a structured MySQL/MariaDB table  
✅ Designed to run for a fixed number of cycles (e.g., 96 cycles at 5-minute intervals, covering 8 hours)  
✅ Includes basic error handling and logging  

## Requirements

- Python 3.x  
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `mariadb` (or `mysql-connector-python` if using MySQL)
  - `logging`

## Installation

```bash
pip install requests beautifulsoup4 mariadb
```
## Database

The script inserts data into a table called `estacion_gas` with the following structure:

| Column                   | Type (example) |
|--------------------------|---------------|
| `PresionCarreta01_[bar]`  | FLOAT          |
| `PresionCarreta02_[bar]`  | FLOAT          |
| `FlujoSalida_[m3/h]`      | FLOAT          |
| `VolAcumCorreg_[m3]`      | FLOAT          |
| `VolAcumNoCorreg_[m3]`    | FLOAT          |

> ⚠ **Ensure this table exists in your database before running the script.**

## Configuration

Update the following parts of the script as needed:

### Database connection

```python
conn = mariadb.connect(
    host='localhost',
    user='root',
    password='YOUR_PASSWORD',
    database='YOUR_DATABASE'
)
```
### SCADA login
```python
login = "your_email@example.com"
password = "your_password"
```