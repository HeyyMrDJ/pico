from phew import connect_to_wifi
from machine import Pin
import urequests as requests
import secrets

# Set constants to make it easier to specify which button to use
keyA = Pin(15,Pin.IN,Pin.PULL_UP)
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)
up = Pin(2,Pin.IN,Pin.PULL_UP)
down = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

# Connect to wifi using secrets from secrets.py
connect_to_wifi(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

# Set headers from secrets.py (includes private bearer token)
headers = secrets.headers

# Base URL for your Home Assistant
base_url = 'http://<URL FOR YOUR HOME ASSISTANT>:8123/api'

if __name__=='__main__':
    while(True):
        # Actions to perform when button or joystick is pressed
        if keyA.value() == 0:
            url = base_url+'/services/script/TestScript'
            requests.post(url=url, headers=headers)
            
        if keyB.value() == 0:
            pass

        if keyX.value() == 0:
            pass
            
        if keyY.value() == 0:
            pass
 
        if(up.value() == 0):
            pass

        if(down.value() == 0):
            pass
            
        if(left.value() == 0):
            pass
        
        if(right.value() == 0):
            pass
        
        if(ctrl.value() == 0):
            pass

