import requests
import time
import json
import os
from PIL import Image
from datetime import date
today = date.today()
print("Today's date:", today)
my_api='YOPUR APOD API'



def get_apod_data(api_key):
    raw_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text
    response = json.loads(raw_response)
    return response

def download_image(url, date):
    if os.path.isfile(f'{date}.png') == False:
        raw_image = requests.get(url).content
        with open(f'{date}.jpg', 'wb') as file:
            file.write(raw_image)
            
    else:
        return FileExistsError


apod_data = get_apod_data(my_api)
download_image(apod_data['url'], apod_data['date'])
file_name = apod_data['date'] + '.jpg'
apod_img_large = Image.open(file_name)
apod_img_large.save('/var/www/html/apod_large.png')         #note - saving here to set up the web server
apod_img = Image.open(file_name).resize((240,240))
apod_pico_img = Image.open(file_name).resize((320,240))
apod_pico_img.save('/var/www/html/apod_pico.jpeg')          #note - saving here to set up the web server

print(apod_img.size)
print(apod_pico_img.size)

#this next bit creates a raw binary file - in the end I didn't need this

import png

infile = 'apod_pico.png'

# outfile = "/apod/apod.raw"

outfile = "/var/www/html/apod.raw"

def color_to_bytes (color):

    r, g, b = color

    arr = bytearray(2)

    arr[0] = r & 0xF8

    arr[0] += (g & 0xE0) >> 5

    arr[1] = (g & 0x1C) << 3

    arr[1] += (b & 0xF8) >> 3

    return arr

png_reader=png.Reader(infile)

image_data = png_reader.asRGBA8()

with open(outfile, "wb") as file:

    #print ("PNG file \nwidth {}\nheight {}\n".format(image_data[0], image_data[1]))

    #count = 0

    for row in image_data[2]:

        for r, g, b, a in zip(row[::4], row[1::4], row[2::4], row[3::4]):

            #print ("This pixel {:02x}{:02x}{:02x} {:02x}".format(r, g, b, a))

            # convert to (RGB565)

            img_bytes = color_to_bytes ((r,g,b))


            file.write(img_bytes)


file.close()

print(apod_data['explanation'])
