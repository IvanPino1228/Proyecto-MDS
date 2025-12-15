import pymysql

conn = pymysql.connect(
    host="localhost",
    user="weather_user",
    password="weather_pass",
    database="weather_db"
)