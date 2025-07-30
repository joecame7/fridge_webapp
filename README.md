# Smart Fridge Monitoring System

A comprehensive IoT-based smart refrigerator monitoring system that combines hardware sensors with a modern web interface to track food inventory, monitor environmental conditions, and prevent food waste through intelligent notifications.

## 🌟 Features

- **Real-time Environmental Monitoring**: Track temperature, humidity, and lighting conditions inside your refrigerator
- **Automated Barcode Scanning**: Camera-based barcode detection with automatic product identification using OpenFoodFacts API
- **Inventory Management**: Add, edit, and track food items with expiration dates through an intuitive web interface
- **Smart Notifications**: Automated email alerts for expiring items to reduce food waste
- **Motion Detection**: PIR sensor integration for user presence detection
- **Remote Access**: Secure remote monitoring via NGROK tunneling
- **Database Integration**: SQLite database for persistent data storage
- **Responsive Web UI**: Mobile-friendly Flask-based web application

## 🛠️ Hardware Components

- Raspberry Pi with camera module
- Grove sensors (temperature, humidity, light, PIR motion, ultrasonic distance)
- LCD display for real-time sensor readings
- GrovePi shield for sensor connectivity

## 🚀 Technology Stack

- **Backend**: Python, Flask, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Hardware**: Raspberry Pi, Grove sensors, Pi Camera
- **APIs**: OpenFoodFacts for product data
- **Communication**: NGROK for remote access, SMTP for notifications

├── temp/
│   ├── static/
│   │   ├── BACKGROUND.png
│   │   ├── settings.json
│   │   ├── smart_fridge.db
│   ├── templates/
│   │   ├── add_item.html
│   │   ├── base.html
│   │   ├── calendar.html
│   │   ├── edit_item.html
│   │   ├── email_setup.html
│   │   ├── home.html
│   │   ├── item_details.html
│   │   ├── items.html
│   │   ├── lookup_barcode.html
│   │   ├── scan_barcode.html
│   │   ├── settings.html
│   ├── app.py
│   ├── sendnotification.py
│
├── createdb.py
├── display.py
├── MasterSensorFile.py
├── openfoodfacts.py
├── readdb.py
├── README.md
├── requirements.txt
├── sendnotification.py


Prerequisites - software, libraries, frameworks

flask
flask-apschedular
flask-cors
grovepi
pandas
picamera
pillow
pyzbar
requests

OpenFoodFacts API
NGROK

Installation 

pip install -r requirements.txt

Install and set up NGROK - https://ngrok.com/downloads/linux

Set up the device by placing the camera, display and motion sensor outside of the refrigerator. The other sensors go inside the fridge for environmental tracking. 


Configuration - Environment Variables

Gmail App Password 




Running Instructions 

python3 MasterSensorFile.py
python3 temp/app.py
ngrok http 5000


Examples of output 

MasterSensorFile.py output
{"temperature": 30.0, "humidity": 0.0, "light_status": "On", "distance": 10, "pir_value": 1, "barcode_data": "No barcode found"}

app.py output
Started expiry notification scheduler
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

ngrok output

ngrok                                                           (Ctrl+C to quit)
                                                                               
🛡️ Protect endpoints w/ IP Intelligence: https://ngrok.com/r/ipintel            
                                                                               
Session Status                online                                            
Account                       cardiffgroup24@gmail.com (Plan: Free)            
Version                       3.22.1                                            
Region                        Europe (eu)                                      
Web Interface                 http://127.0.0.1:4040                            
Forwarding                    https://6fcb-131-251-32-104.ngrok-free.app -> http
                                                                               
Connections                   ttl     opn     rt1     rt5     p50     p90      
                              0       0       0.00    0.00    0.00    0.00  



Third-Party Software and Frameworks

Flask - 3.1.0
Purpose: Web framework 
https://flask.palletsprojects.com/en/stable/

Flask-APScheduler 1.13.1
Purpose: Scheduler for running tasks
https://pypi.org/project/Flask-APScheduler/

Flask-CORS - 5.0.1
Purpose: Access for API
https://pypi.org/project/flask-cors/

GrovePi - 1.0.4
Purpose: Interaction with sensors 
https://pypi.org/project/grovepi/

NGROK - 3.x
Purpose: Shares the local flask server to the internet for remote access

OpenCV - 4.x
Purpose: Camera and barcode detection 
https://docs.opencv.org/

OpenFoodFacts API 
Purpose: Retrieves product data from barcode scanned
https://world.openfoodfacts.org/data

Pandas - 2.2.3
Purpose: Data Analysis
https://pypi.org/project/pandas/ 

picamera - 1.13
Purpose: Controls the Raspberry Pi Camera module
https://picamera.readthedocs.io/en/release-1.13/

pyzbar - 0.1.9
Purpose: Decode barcodes from images
https://pypi.org/project/pyzbar/

requests - 2.32.0
Purpose: Making HTTP requests to the OpenFoodFacts API
https://pypi.org/project/requests/

sqlite3 (built-in) - Python 3.x
Purpose: Local database management 
https://docs.python.org/3/library/sqlite3.html

smtplib (built-in) - Python 3.x
Purpose: Sending the email notifications 
https://docs.python.org/3/library/smtplib.html

time, os, datetime (built-in) - Python 3.x
Purpose: System operations and time handling
https://docs.python.org/3/


Troubleshooting

Flask server not accessible? 

Ensure NGROK is started with the correct port, run ngrok http 5000, and use the forwarded HTTPS URL shown in terminal.

Barcode not detected? 

The lighting may be poor. Make sure the barcode is clearly visible to the camera, well-lit and in focus. Follow the distance required on the LCD screen.

GrovePi sensor not responding? 

Double-check that the wiring and the port assignments in the code. Run GrovePi's update tool, grove_firmware_update

PiCamera not working? 

Run sudo raspi-config, enable the camera interface and reboot. Check camera wire is connected. 

Emails not sending? 

Check SMTP server settings, credentials and port.

Module not found?

Run pip install -r requirements.txt
