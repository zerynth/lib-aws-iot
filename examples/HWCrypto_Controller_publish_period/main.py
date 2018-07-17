# AWS IoT Controlled publish period 
# Created at 2017-10-03 08:49:48.182639

import streams
import json
from wireless import wifi

# choose a wifi chip supporting secure sockets and client certificates
from espressif.esp32net import esp32wifi as wifi_driver

# import aws iot module
from aws.iot import iot

# import microchip ateccx08a module for its hw crypto element interface
from microchip.ateccx08a import ateccx08a

# import helpers functions to easily load keys, certificates and thing configuration
import helpers

# THING CERTIFICATE FILE MUST BE PLACED INSIDE PROJECT FOLDER 
new_resource('certificate.pem.crt')
# SET THING CONFIGURATION INSIDE THE FOLLOWING JSON FILE
new_resource('thing.conf.json')

# define a callback for shadow updates
def shadow_callback(requested):
    global publish_period
    print('requested publish period:', requested['publish_period'])
    publish_period = requested['publish_period']
    return {'publish_period': publish_period}

streams.serial()
wifi_driver.auto_init()

print('connecting to wifi...')
# place here your wifi configuration
wifi.link("SSID",wifi.WIFI_WPA2,"PSW")

# start hardware crypto interface
ateccx08a.hwcrypto_init(I2C0, 0)

clicert = helpers.load_cert('certificate.pem.crt')
thing_conf = helpers.load_thing_conf()
publish_period = 1000

# create aws iot thing instance, connect to mqtt broker, set shadow update callback and start mqtt reception loop
# N.B. private key is passed as an empty string to use an hardware stored one
thing = iot.Thing(thing_conf['endpoint'], thing_conf['mqttid'], clicert, '', thingname=thing_conf['thingname'])
print('connecting to mqtt broker...')
thing.mqtt.connect()
thing.on_shadow_request(shadow_callback)
thing.mqtt.loop()

thing.update_shadow({'publish_period': publish_period})

while True:
    print('publish random sample...')
    thing.mqtt.publish("dev/sample", json.dumps({ 'asample': random(0,10) }))
    sleep(publish_period)

