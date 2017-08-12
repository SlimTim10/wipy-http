import machine
import os
import socket
from machine import SD
from network import WLAN

WIFI_SSID = 'Network SSID'
WIFI_PASSWORD = 'password'
STATIC_IP = '192.168.1.10'
SUBNET_MASK = '255.255.255.0'
DEFAULT_GATEWAY = '192.168.1.1'
DNS = '8.8.8.8'

sd = SD()
try:
    os.mount(sd, '/sd')
except:
    pass
files = os.listdir('/sd')
file_list = '\n'.join(files)

def setup_wifi():
    wlan = WLAN(mode=WLAN.STA)
    if wlan.isconnected():
        return True
    wlan.ifconfig(config=(STATIC_IP, SUBNET_MASK, DEFAULT_GATEWAY, DNS))
    print('Searching for network...')
    nets = wlan.scan()
    for net in nets:
        if net.ssid == WIFI_SSID:
            print('Network found!')
            wlan.connect(ssid=WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASSWORD), timeout=5000)
            print('Connecting...')
            while not wlan.isconnected():
                machine.idle()
            if wlan.isconnected():
                print('WLAN connected')
                return True
            else:
                print('WLAN connection failed')
                return False
    print('Network not found')
    return False

def setup_server():
    addr = socket.getaddrinfo(STATIC_IP, 8080)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        response = file_list
        cl.send(response)
        cl.close()

if setup_wifi():
    setup_server()
else:
    print('Error connecting to access point')
