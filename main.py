import urequests as requests
import time
import json
import os
import network
import secrets
import picographics
import jpegdec
from pimoroni import Button

def get_apod_data(api_key):
    raw_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text
    response = json.loads(raw_response)
    return response

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()

def get_data():
    
    apod_data = get_apod_data(secrets.apod_api)

    url = 'YOUR PI SERVER LINK'

    request_status = requests.get(url)
    print(request_status.status_code)

    apod_jpeg = requests.get(url).content

    if request_status.status_code == 200:
        with open("apod.jpg", 'wb') as f:
            f.write(apod_jpeg)
        desc_list = apod_data['explanation'].split()
        apod_date = apod_data['date']
        apod_title = apod_data['title']
        apod_copyright = apod_data['copyright']
        
    print(apod_data['explanation'])
    return desc_list, apod_date, apod_title, apod_copyright

def show_image():
    # Create a new JPEG decoder for our PicoGraphics
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    #j.open_file("apod_pico-5.jpeg")
    j.open_file("apod.jpg")

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)

    # Display the result
    display.update()
    
display = picographics.PicoGraphics(display=picographics.DISPLAY_PICO_DISPLAY_2)

display.set_font("bitmap8")

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
print(wlan.isconnected())

data_count = 0

while True:
    if data_count < 1:
        desc_list, apod_date, apod_title, apod_copyright = get_data()
    show_image()
    if button_a.read():                                         # if a button press is detected then...
        text_start = 0
        text_end = 8
        while text_start < len(desc_list):
            clear()                                                 # clear to black
            display.set_pen(WHITE)
            display.text(' '.join(desc_list[text_start:text_end]), 10, 10, 240, 4)  # display some text on the screen
            display.update()                                        # update the display
        
            time.sleep(4)
            text_start +=8
            text_end +=8
        clear()
    if button_b.read():                                         # if a button press is detected then..
        clear()                                                 # clear to black
        display.set_pen(WHITE)
        display.text("APOD date = " + apod_date, 10, 10, 240, 4)  # display some text on the screen
        display.update()                                        # update the display
        time.sleep(2)
    if button_x.read():                                         # if a button press is detected then..
        clear()                                                 # clear to black
        display.set_pen(WHITE)
        display.text("APOD title = " + apod_title, 10, 10, 240, 4)  # display some text on the screen
        display.update()                                        # update the display
        time.sleep(2)
    if button_y.read():                                         # if a button press is detected then..
        clear()                                                 # clear to black
        display.set_pen(WHITE)
        display.text("Copyright = " + apod_copyright, 10, 10, 240, 4)  # display some text on the screen
        display.update()                                        # update the display
        time.sleep(2)
    if data_count <= 10000:
        data_count += 1
    else:
        data_count = 0
        
