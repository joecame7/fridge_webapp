#!/usr/bin/env python3
import time
import grovepi
import threading
from picamera import PiCamera
from time import sleep
from datetime import datetime
from PIL import Image
from pyzbar.pyzbar import decode
import openfoodfacts
import math
import json
import sqlite3
import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
import pandas as pd
import sys, os
from display import setText

# Configure logging 
handler = TimedRotatingFileHandler('sensor_log.log', when='D', interval=1, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)
logging.raiseExceptions = False

stderr_file = open(os.devnull, 'w')
sys.stderr = stderr_file

# Global variables to store sensor data
sensor_data = {
    'temperature': None,
    'humidity': None,
    'light_status': None,
    'distance': None,
    'pir_value': None,
    'barcode_data': None
}

scanned_barcodes = {}
scanned_barcodes_lock = threading.Lock()  

def save_product_to_db(barcode_data):
    conn = sqlite3.connect('temp/static/smart_fridge.db')
    cursor = conn.cursor()
    user_id = 1 

    if barcode_data and barcode_data != 'No barcode found':
   
        cursor.execute('SELECT product_id FROM Products WHERE barcode = ? AND user_id = ?', 
                       (barcode_data, user_id))
        existing_product = cursor.fetchone()


        try:
            product_info = openfoodfacts.lookup_barcode(barcode_data)
            if not product_info: 
                 logging.warning(f"No product info found for barcode {barcode_data}")
                 conn.close()
                 return

            product_name = product_info.get('Product Name', 'unknown')
            allergens_list = product_info.get('Allergens', []) 
            categories_list = product_info.get('Categories', []) 
            image_url = product_info.get('Image URL', 'unknown')
            nutritional_info_dict = product_info.get('Nutriments', {})

            nutritional_info_json = json.dumps(nutritional_info_dict) if nutritional_info_dict else '{}'
            allergens_json = json.dumps(allergens_list) 
            categories_json = json.dumps(categories_list) 

            if product_name != 'unknown':
                cursor.execute('''
                    INSERT INTO Products (user_id, product_name, barcode, nutritional_info, allergens, categories, image_url, added_at, expiration_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
                ''', (user_id, product_name, barcode_data, nutritional_info_json, allergens_json, categories_json, image_url, datetime.now()))
                logging.info(f'Saved Product to database: {product_name}, Barcode: {barcode_data}')
                conn.commit() 
            else:
                logging.warning(f'No valid product name found for the barcode {barcode_data}.')

        except openfoodfacts.ProductNotFoundError:
             logging.warning(f"Product not found on OpenFoodFacts for barcode: {barcode_data}")
        except Exception as e:
             logging.error(f"Error processing or saving product for barcode {barcode_data}: {e}")
             conn.rollback() 

    else:
        logging.warning('No valid barcode data to save.')

    conn.close()

def camera_thread():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (3280, 2464)
    camera.brightness = 60
    camera.contrast = 70
    camera.sharpness = 100
    buzzer = 8
    grovepi.pinMode(buzzer, "OUTPUT")
    while True:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'/home/pi/Desktop/images/image_{timestamp}.jpg'
            sleep(3)
            camera.capture(filename)

            # Decode barcode
            image = Image.open(filename)
            barcodes = decode(image)
            if barcodes:
                grovepi.digitalWrite(buzzer, 0)
                grovepi.digitalWrite(buzzer, 1)
                time.sleep(0.3)
                grovepi.digitalWrite(buzzer, 0)
                for barcode in barcodes:
                    data = barcode.data.decode('utf-8')
                    sensor_data['barcode_data'] = data
                    logging.info(f'Barcode Data: {data}')
                    
                    # Check if barcode was scanned in the last 5 seconds.
                    process_barcode = False
                    current_time = time.time()
                    with scanned_barcodes_lock:
                        last_scanned_time = scanned_barcodes.get(data, 0)
                        if current_time - last_scanned_time >= 5:
                            scanned_barcodes[data] = current_time
                            process_barcode = True
                        else:
                            logging.info(f"Barcode {data} scanned too recently. Ignoring.")
                    
                    if process_barcode:
                        setText("Product Scanned", priority=True)
                        save_product_to_db(data)
            else:
                sensor_data['barcode_data'] = 'No barcode found'
                logging.info('No barcode found')
            time.sleep(0.3)
        except Exception as e:
            logging.error(f"Camera error: {e}")

def update_sensors():
    light_sensor = 0
    led = 4
    buzzer = 8
    ultrasonic_ranger = 3
    dht_sensor = 4  
    blue = 0    
    pir = 2

    grovepi.pinMode(light_sensor, "INPUT")
    grovepi.pinMode(led, "OUTPUT")
    grovepi.pinMode(buzzer, "OUTPUT")
    grovepi.set_bus("RPI_1")
    while True:
        try:
            # Light Sensor
            sensor_value = grovepi.analogRead(light_sensor)
            resistance = float(1023 - sensor_value) * 10 / sensor_value
            sensor_data['light_status'] = 'Off' if resistance > 10 else 'On'
            logging.info(f'Light Status: {sensor_data["light_status"]}')

            # Ultrasonic Ranger
            distance = grovepi.ultrasonicRead(ultrasonic_ranger)
            sensor_data['distance'] = distance
            distance_message = ''
            if distance < 20:
                distance_message = "Too Close"
            elif distance > 30:
                distance_message = "Too Far"
            else:
                distance_message = "Optimal Distance"
            distance_message += f" | Distance: {distance}cm"
            logging.info(distance_message)
            
            # DHT Sensor
            [temp, humidity] = grovepi.dht(dht_sensor, blue)
            if not math.isnan(temp) and not math.isnan(humidity):
                sensor_data['temperature'] = temp
                sensor_data['humidity'] = humidity
                logging.info(f'Temperature: {temp}, Humidity: {humidity}')
            else:
                logging.warning('Received NaN for temperature or humidity')

            pir_value = grovepi.digitalRead(pir)
            sensor_data['pir_value'] = pir_value
            logging.info(f'PIR Value: {pir_value}')

            # Display the distance message on the LCD
            setText(distance_message)
            time.sleep(0.5)

        except Exception as e:
            logging.error(f"An error occurred: {e}")

def save_sensor_data_to_db(data):
    required_keys = ['temperature', 'humidity', 'light_status', 'pir_value']
    if any(data.get(key) is None for key in required_keys):
        logging.warning('Not all sensor data is available, skipping database save.')
        return

    conn = sqlite3.connect('temp/static/smart_fridge.db')
    cursor = conn.cursor()
    user_id = 1
    try:
        cursor.execute('''
            INSERT INTO FridgeMetrics (user_id, temperature, humidity, light_status, pir_value, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, data['temperature'], data['humidity'], data['light_status'], data['pir_value'], datetime.now()))
        logging.info('Saved FridgeMetrics to database.')
    except Exception as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.commit()
        conn.close()

def get_sensor_data():
    return sensor_data

if __name__ == '__main__':
    threading.Thread(target=camera_thread, daemon=True).start()
    threading.Thread(target=update_sensors, daemon=True).start()

    while True:
        data = get_sensor_data()
        print(json.dumps(data))
        logging.info(f'Sensor Data: {json.dumps(data)}')
        save_sensor_data_to_db(data)
        time.sleep(5)
