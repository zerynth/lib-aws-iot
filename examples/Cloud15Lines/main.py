from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver
from bosch.bme280 import bme280
from aws.iot import iot, default_credentials
wifi_driver.auto_init()
wifi.link("SSID",wifi.WIFI_WPA2,"PSW")

endpoint, mqttid, clicert, pkey = default_credentials.load()
thing = iot.Thing(endpoint, mqttid, clicert, pkey)
thing.mqtt.connect()
thing.mqtt.loop()
sensor = bme280.BME280(I2C0)
while True:
    thing.mqtt.publish("sensors", {'temp':sensor.get_temp()})
    sleep(1000)
