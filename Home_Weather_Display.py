# Home_Weather_Display.py
#
# This is an project for using the Grove RGB LCD Display and the Grove DHT Sensor from the GrovePi starter kit
#
# In this project, the Temperature and humidity from the DHT sensor is printed on the RGB-LCD Display
#
#
# Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
#  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
#  1 - DHT22 - white one, aka DHT Pro or AM2302
#  2 - DHT21 - black one, aka AM2301
#
# For more info please see: http://www.dexterindustries.com/topic/537-6c-displayed-in-home-weather-project/
#
'''
The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
import pymysql

dht_sensor_port = 7 # connect the DHt sensor to port 7
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the I2C line
setRGB(0,255,0)

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="adm_user",
        password="1228",
        database="ProyectoMDS2025"
    )

def save_to_db(temp, hum):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather (temperature, humidity) VALUES (%s, %s)",
        (temp, hum)
    )
    conn.commit()
    cursor.close()
    conn.close()

def read_last_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT temperature, humidity FROM weather ORDER BY id DESC LIMIT 1"
    )
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


while True:
    try:
        # Leer sensor DHT
        [temp, hum] = dht(dht_sensor_port, dht_sensor_type)
        print("Temp =", temp, "C | Hum =", hum, "%")

        # Verificar valores inválidos
        if isnan(temp) or isnan(hum):
            raise TypeError("NaN error")

        # Guardar en MariaDB
        save_to_db(temp, hum)

        # Leer último dato de la BD
        t, h = read_last_data()

        # Mostrar en la LCD
        setText_norefresh(
            f"Temp: {t:.1f} C\nHumidity: {h:.1f} %"
        )

    except (IOError, TypeError) as e:
        print("Error:", e)
        setText("")

    except KeyboardInterrupt:
        print("Programa detenido")
        setText("")
        break

    # Espera entre lecturas (recomendado para BD)
    sleep(5)