HWCrypto Controlled Publish Period
==================================

Connect your device to AWS IoT platform and start publishing at a default period, waiting for period updates requested as changes to things' shadow.
The connection is performed using a hardware private key stored in a ateccx08a crypto element.

To register a hardware key to AWS IoT platform the following steps are needed:

    # derive a CSR from the hardware key
    ztc provisioning uplink-config-firmware esp32_device_alias
    ztc provisioning get-csr esp32_device_alias privatekey_slot 'C=IT,O=ZER,CN=MyDevice' -o hwkey0.csr

    # get a certificate from AWS IoT and activate it
    aws iot create-certificate-from-csr --certificate-signing-request file://hwkey0.csr --certificate-pem-outfile certificate.pem.crt --set-as-active
    aws iot attach-thing-principal --thing-name my-thing --principal certificate-arn
    aws iot attach-principal-policy --policy-name my-policy --principal certificate-arn


