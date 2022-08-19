# pico_w_apod
Get the NASA asronomy picture of the day using a pico w (with a little help from a friendly raspberry pi)

I wanted a little desktop viewer for the NASA Astronomy Picture of the Day API data - I'm using those pictures for another project, so I wanted something sitting on my desktop in case today's picture is a 'good' one (they're all good, I just mean 'good' for this other project). When the Pico W came out I thought this would be ideal with a little Pimoroni Pico Display 2 - only thing is the NASA pictures are a little bit big for processing with a Pico.  

To compensate I've got a Raspberry Pi Zero W running a separate script to shrink the picture down to Pico size, and set up a as a little local web server so that instead of getting the picture from NASA it gets the transformed picture (and all the descriptions etc. come from the APOD site).

As I had buttons on the display I thought I'd print out some of the APOD text too - it was there, I had buttons, why not!

I have the pi zero script scheduled via crontab to run every hour, and the pico script is running continuously but only updates the data every so often.

First get the pi zero set up to run as a web server following this guide:  https://www.seeedstudio.com/blog/2020/06/23/setup-a-raspberry-pi-web-server-and-easily-build-an-html-webpage-m/ (everything from Installing Apache Web Server downwards).  index.html shows what I've got - it displays a raw binary image, a small pico sized jpeg and the full image.

Then run the pi_picture_server.py script on the pi zero w - this will create the picture files for the html page.  You can view the webpage created by entering the IP address in a web browser for the pi zero on another computer / your phone just to check it's displaying correctly.  Note this will only work on your local network.

Then set up the pico w.  You need the secrets.py file and the main.py - alter the details in secrets for your own network (and you can get an API key from the APOD site here: https://api.nasa.gov (it's free!).  Calling the other script main.py means it will run on start when the pico is plugged in.
