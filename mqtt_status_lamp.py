# Python 3.6
# Menggunakan Raspberry Pi untuk mengontrol LED menggunakan protokol MQTT sebagai Client Subscribe
# MIS AII (30 Juni 2022)

import random
import time
import RPi.GPIO as GPIO

# Menggunakan module paho-mqtt, silahkan import dan install terlebih dahulu menggunakan PIP
from paho.mqtt import client as mqtt_client

# Syntax MQTT Broker
# IP Address dan Port number dari MQTT Broker
# Pastikan port yang inisialisasi tidak diblokir oleh Firewall dari host yang digunakan.
broker = '192.168.0.234'
port = 1883
client_id = 'ASHV02_test_01'
# Username dan Password dari MQTT Broker
# Bila tidak ada, silahkan gunakan comment pada dua variable dibawah dan client.username_pw_set pada connect_mqtt()
username = ''
password = ''
# Topic yang akan di subscribe
topic = "test_mis_mqtt_sl"
# GPIO Number dari Input Relay
GreenPin = 27
RedPin = 17


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        # Terinisialisasi setiap terdapat pesan masuk
        # msg.payload.decode() adalah isi pesan dari
        if (msg.payload.decode() == '0'):
            GPIO.output(GreenPin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(GreenPin, GPIO.HIGH)
            # sleep for 1 second
        elif (msg.payload.decode() == '1'):
            GPIO.output(RedPin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(RedPin, GPIO.HIGH)
        else:
            print('NG')

    client.subscribe(topic)
    client.on_message = on_message


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GreenPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RedPin, GPIO.OUT, initial=GPIO.LOW)
    time.sleep(1)
    GPIO.output(GreenPin, GPIO.HIGH)
    GPIO.output(RedPin, GPIO.HIGH)


def main():
    print('Connecting...')
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


def destroy():
    GPIO.output(GreenPin, GPIO.LOW)
    GPIO.output(RedPin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
