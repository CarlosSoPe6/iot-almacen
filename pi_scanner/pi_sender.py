#!/usr/bin/env python3

from urllib.request import urlopen
from time import sleep

def send_to(chanel, data):
    baseURL = 'http://api.thingspeak.com/update?api_key=REPLACE_KEY&field{}={}'
    print(baseURL.format(chanel, data))
    f = urlopen(baseURL.format(chanel, data))
    f.close()
    sleep(1)
    pass
