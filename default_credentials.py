# -*- coding: utf-8 -*-
# @Author: Lorenzo
# @Date:   2018-10-22 12:09:05
# @Last Modified by:   Lorenzo
# @Last Modified time: 2019-01-16 12:50:39

"""
.. module:: default_credentials

*******************************************
Amazon Web Services IoT Default Credentials
*******************************************

The Zerynth AWS IoT Default Credentials module is useful to achieve a zero-time startup for your AWS IoT project powered by Zerynth.

It makes it really simple to load connection credentials, which could be stored on flash or in a secure element, by means of a single call to the :func:`load` function.

    """

import json

#-if ZERYNTH_HWCRYPTO_ATECCx08A
from microchip.ateccx08a import ateccx08a
#-else
new_resource('private.pem.key')
#-endif

new_resource('thing.conf.json')
new_resource('certificate.pem.crt')

def _load_from_resource(mresource, tojson=False, append_zero=False):
    resource_stream = open('resource://' + mresource)
    resource_str = ''
    while True:
        line = resource_stream.readline()
        if not line:
            break
        resource_str += line
    if tojson:
        return json.loads(resource_str)
    if append_zero:
        resource_str += '\x00'
    return resource_str

def load():
    """
.. function:: load()

    This function returns:

        * AWS IoT endpoint for the device to connect to;
        * device Mqtt ID;
        * client certificate to be sent to AWS;
        * device private key.

    Endpoint and Mqtt ID are retrieved from the ``thing.conf.json`` configuration file which has to be put in the project and filled like this: ::

        {
            "endpoint": "myendpoint.iot.my-region.amazonaws.com",
            "mqttid": "mymqttid"
        }

    Client certificate is retrieved from ``certificate.pem.crt`` file which must be put in the project, too.
    On the other hand the private key can be retrieved from different sources depending on the presence of the ``ZERYNTH_HWCRYPTO_ATECCx08A`` define inside the Zerynth project ``project.yml`` file.

        * without ``ZERYNTH_HWCRYPTO_ATECCx08A``, the private key is taken from ``private.pem.key`` file put in the project and stored on flash (unsafe for production purposes)
        * with ``ZERYNTH_HWCRYPTO_ATECCx08A``, the private key is stored inside a secure element, returned private key is an empty string and the ``thing.conf.json`` needs extra configuration fields: ::

            {
                "crypto_drv": 0 # I2C the secure element is connected to, 0 for I2C0
                "crypto_addr": 88, # I2C address of the secure element
                "crypto_clock": 100000, # I2C clock (Hz) of the secure element 
                "crypto_slot": 2 # slot of the secure element where the private key is stored
            }        

    """
    thing_conf = _load_from_resource('thing.conf.json', tojson=True)
    clicert = _load_from_resource('certificate.pem.crt', append_zero=True)
#-if ZERYNTH_HWCRYPTO_ATECCx08A
    ateccx08a.hwcrypto_init(thing_conf['crypto_drv'], thing_conf['crypto_slot'],
                        i2c_addr=thing_conf['crypto_addr'], i2c_clock=thing_conf['crypto_clock'])
    return thing_conf['endpoint'], thing_conf['mqttid'], clicert, ''
#-else
    pkey = _load_from_resource('private.pem.key', append_zero=True)
    return thing_conf['endpoint'], thing_conf['mqttid'], clicert, pkey
#-endif