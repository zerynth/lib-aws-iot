# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-09-21 16:17:16
# @Last Modified by:   m.cipriani
# @Last Modified time: 2019-09-11 14:49:32

"""
.. module:: iot

*******************************
Amazon Web Services IoT Library
*******************************

The Zerynth AWS IoT Library can be used to ease the connection to the `AWS IoT platform <https://aws.amazon.com/iot-platform/>`_.

It allows to make your device act as an AWS IoT Thing which can be registered through AWS tools or directly from the :ref:`Zerynth Toolchain <ztc-cmd-aws>`.

Check this video for a live demo:

.. raw:: html

    <div style="margin-top:10px;">
  <iframe width="100%" height="480" src="https://www.youtube.com/embed/IZzZF3DGWkY?ecver=1" frameborder="0" gesture="media" allow="encrypted-media" allowfullscreen></iframe>
      </div>


    """

import json
import ssl
#-if AWSCLOUD_LWMQTT
from lwmqtt import mqtt
#-else
from mqtt import mqtt
#-endif

import mcu

legacy_and_amazon_cas = '''-----BEGIN CERTIFICATE-----
MIIE0zCCA7ugAwIBAgIQGNrRniZ96LtKIVjNzGs7SjANBgkqhkiG9w0BAQUFADCB
yjELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQL
ExZWZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJp
U2lnbiwgSW5jLiAtIEZvciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxW
ZXJpU2lnbiBDbGFzcyAzIFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0
aG9yaXR5IC0gRzUwHhcNMDYxMTA4MDAwMDAwWhcNMzYwNzE2MjM1OTU5WjCByjEL
MAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQLExZW
ZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJpU2ln
biwgSW5jLiAtIEZvciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxWZXJp
U2lnbiBDbGFzcyAzIFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0aG9y
aXR5IC0gRzUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCvJAgIKXo1
nmAMqudLO07cfLw8RRy7K+D+KQL5VwijZIUVJ/XxrcgxiV0i6CqqpkKzj/i5Vbex
t0uz/o9+B1fs70PbZmIVYc9gDaTY3vjgw2IIPVQT60nKWVSFJuUrjxuf6/WhkcIz
SdhDY2pSS9KP6HBRTdGJaXvHcPaz3BJ023tdS1bTlr8Vd6Gw9KIl8q8ckmcY5fQG
BO+QueQA5N06tRn/Arr0PO7gi+s3i+z016zy9vA9r911kTMZHRxAy3QkGSGT2RT+
rCpSx4/VBEnkjWNHiDxpg8v+R70rfk/Fla4OndTRQ8Bnc+MUCH7lP59zuDMKz10/
NIeWiu5T6CUVAgMBAAGjgbIwga8wDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8E
BAMCAQYwbQYIKwYBBQUHAQwEYTBfoV2gWzBZMFcwVRYJaW1hZ2UvZ2lmMCEwHzAH
BgUrDgMCGgQUj+XTGoasjY5rw8+AatRIGCx7GS4wJRYjaHR0cDovL2xvZ28udmVy
aXNpZ24uY29tL3ZzbG9nby5naWYwHQYDVR0OBBYEFH/TZafC3ey78DAJ80M5+gKv
MzEzMA0GCSqGSIb3DQEBBQUAA4IBAQCTJEowX2LP2BqYLz3q3JktvXf2pXkiOOzE
p6B4Eq1iDkVwZMXnl2YtmAl+X6/WzChl8gGqCBpH3vn5fJJaCGkgDdk+bW48DW7Y
5gaRQBi5+MHt39tBquCWIMnNZBU4gcmU7qKEKQsTb47bDN0lAtukixlE0kF6BWlK
WE9gyn6CagsCqiUXObXbf+eEZSqVir2G3l6BFoMtEMze/aiCKm0oHw0LxOXnGiYZ
4fQRbxC1lfznQgUy286dUV4otp6F01vvpX1FQHKOtw5rDgb7MzVIcbidJ4vEZV8N
hnacRHr2lVz2XTIIM6RUthg/aFzyQkqFOFSDX9HoLPKsEdao7WNq
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
\x00'''


class AWSMQTTClient(mqtt.Client):

    def __init__(self, mqtt_id, endpoint, ssl_ctx):
        mqtt.Client.__init__(self, mqtt_id, clean_session=True)
        self.endpoint = endpoint
        self.ssl_ctx = ssl_ctx
#-if AWSCLOUD_LWMQTT
    def connect(self, port=8883, sock_keepalive=None, aconnect_cb=None, breconnect_cb=None, loop_failure=None):
        mqtt.Client.connect(self, self.endpoint, 60, port=port, ssl_ctx=self.ssl_ctx, sock_keepalive=sock_keepalive, aconnect_cb=aconnect_cb, breconnect_cb=breconnect_cb, loop_failure=loop_failure)
#-else
    def connect(self, port=8883, sock_keepalive=None, aconnect_cb=None, breconnect_cb=None):
        mqtt.Client.connect(self, self.endpoint, 60, port=port, ssl_ctx=self.ssl_ctx, sock_keepalive=sock_keepalive, aconnect_cb=aconnect_cb, breconnect_cb=breconnect_cb)
#-endif
    def publish(self, topic, payload=None):
        if type(payload) == PDICT:
            payload = json.dumps(payload)
        mqtt.Client.publish(self, topic, payload)

class Thing:
    """
===============
The Thing class
===============

.. class:: Thing(endpoint, mqtt_id, clicert, pkey, thingname=None, cacert=None)

        Create a Thing instance representing an AWS IoT Thing.

        The Thing object will contain an mqtt client instance pointing to AWS IoT MQTT broker located at :samp:`endpoint` endpoint.
        The client is configured with :samp:`mqtt_id` as MQTT id and is able to connect securely through AWS authorized :samp:`pkey` private key and :samp:`clicert` certificate (an optional :samp:`cacert` CA Certificate can also be passed).

        :ref:`Refer to Zerynth SSL Context creation <stdlib.ssl.create_ssl_context>` for admitted :samp:`pkey` values.

        The client is accessible through :samp:`mqtt` instance attribute and exposes all :ref:`Zerynth MQTT Client methods <lib.zerynth.mqtt>` so that it is possible, for example, to setup
        custom callback on MQTT commands.
        The only difference concerns mqtt.connect method which does not require broker url and ssl context, taking them from Thing configuration::

            my_thing = iot.Thing('my_ep_id.iot.my_region.amazonaws.com', 'my_thing_id', clicert, pkey)
            my_thing.mqtt.connect()
            ...
            my_thing.mqtt.loop()

        A :samp:`thingname` different from chosen MQTT id can be specified, otherwise :samp:`mqtt_id` will be assumed also as Thing name.
    """

    def __init__(self, endpoint, mqtt_id, clicert, pkey, thingname=None, cacert=None):
        global legacy_and_amazon_cas
        if cacert is None:
            cacert = legacy_and_amazon_cas
        else:
            legacy_and_amazon_cas = None
        self.ctx = ssl.create_ssl_context(cacert=cacert,clicert=clicert,pkey=pkey,options=ssl.CERT_REQUIRED|ssl.SERVER_AUTH)
        self.mqtt = AWSMQTTClient(mqtt_id, endpoint, self.ctx)
        self.thingname = (thingname or mqtt_id)

        self._shadow_cbk = None
        self._client_token = ''.join([ str(xx) for xx in mcu.uid()])

    def update_shadow(self, state):
        """
.. method:: update_shadow(state)

        Update thing shadow with reported :samp:`state` state.

        :samp:`state` must be a dictionary containing only custom state keys and values::

            my_thing.update_shadow({'publish_period': 1000})

        """
        shadow_rep = { 'state': { 'reported': state }}
        self.mqtt.publish('$aws/things/' + self.thingname + '/shadow/update', json.dumps(shadow_rep))

#-if !AWSCLOUD_LWMQTT
    def _is_shadow_delta(self, mqtt_data):
        if ('message' in mqtt_data):
            return (mqtt_data['message'].topic == ('$aws/things/' + self.thingname + '/shadow/update/delta'))
        return False
#-endif

#-if !AWSCLOUD_LWMQTT
    def _handle_shadow_request(self, mqtt_client, mqtt_data):
        reported = self._shadow_cbk(json.loads(mqtt_data['message'].payload)['state'])
        if reported is not None:
            self.update_shadow(reported)
#-else
    def _handle_shadow_request(self, mqtt_client, payload):
        reported = self._shadow_cbk(json.loads(payload)['state'])
        if reported is not None:
            self.update_shadow(reported)
#-endif

    def on_shadow_request(self, shadow_cbk):
        """
.. method:: on_shadow_request(shadow_cbk)

        Set a callback to be called on shadow update requests.

        :samp:`shadow_cbk` callback will be called with a dictionary containing requested state as the only parameter::

            def shadow_callback(requested):
                print('requested publish period:', requested['publish_period'])

            my_thing.on_shadow_request(shadow_callback)

        If a dictionary is returned, it is automatically published as reported state.
        """
        if self._shadow_cbk is None:
#-if !AWSCLOUD_LWMQTT
            self.mqtt.subscribe([['$aws/things/' + self.thingname + '/shadow/update/delta',0]])
#-else
            self.mqtt.subscribe('$aws/things/' + self.thingname + '/shadow/update/delta', self._handle_shadow_request)
#-endif
        self._shadow_cbk = shadow_cbk
#-if !AWSCLOUD_LWMQTT
        self.mqtt.on(mqtt.PUBLISH, self._handle_shadow_request, self._is_shadow_delta)
#-endif

