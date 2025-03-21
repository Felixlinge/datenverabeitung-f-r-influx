import os, time
from opcua import ua
from time import sleep
from opcua import Client
from influxdb_client_3 import InfluxDBClient3, Point

token = "OUxMLbGNNulXf100g7Nmlj6XkxOATetWN48lRdfUR4WQtRtmVfeLFxb0t79v8YkTq-kuTM9PM7elNLJtdk6rNg=="
org = "BBS Brinkstraße"
host = "http://192.168.24.108:8086/"
clientdb = InfluxDBClient3(host=host, token=token, org=org)

ua_cert = r"C:\Users\Felix\Desktop\Neuer Ordner\certs\uaexpert.der"
ua_key = r"C:\Users\Felix\Desktop\Neuer Ordner\private\uaexpert_key.pem"

client = Client("opc.tcp://192.168.24.108:4840")
client.set_security_string(f"Basic256Sha256,SignAndEncrypt,{ua_cert},{ua_key}")
client.application_uri = "urn:FlexLappentop:UnifiedAutomation:UaExpert"
# setze Benutzername und Passwort
client.set_user('opc')
client.set_password('opc')

try:
    client.connect()

    # greife auf Elemente im Baum zu
    root = client.get_root_node()
    objects = client.get_objects_node()
    #app = objects.get_child(["2:DeviceSet", "4:CODESYS Control for Raspberry Pi 64 SL", "3:Resources", "4:Application","3: Programs","4:PLC_PRG"])

    # erzeuge Objekte für Knoten aus dem Baum über OPC UA Notation
    eingang1 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.PLC_PRG.var_1')
    eingang2 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.PLC_PRG.var_2')
    ausgang = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.PLC_PRG.ausgang_1')

    # OPC-Variablen besitzen vier Attribute Datentyp, Wert, Status, Zeitstempel
    data = ausgang.get_data_value()
    print(' Variable Ausgang ')
    print('Datentyp    ', data.Value.VariantType)
    print('Wert        ', data.Value.Value)
    print('Status      ', data.StatusCode)
    print('Zeitstempel ', data.SourceTimestamp)
    print('')

    eingang1.set_value(ua.Variant(10.0, ua.VariantType.Float))
    eingang2.set_value(ua.Variant(3.0, ua.VariantType.Float))
    #var.set_value(ua.Variant([50], ua.VariantType.Double))

    # Variable ausgang auslesen
    while True:
        print('Wert der Variable ausgang ', ausgang.get_value())

        point = (
            Point("census")
            .field("grad",ausgang.get_value())
        )
        clientdb.write(database="Data", record=point)
        time.sleep(2)
finally:
    client.disconnect()

