import machine
import ubinascii

wifi_ssid = ""
wifi_password = ""

device_id = ubinascii.hexlify(machine.unique_id()).decode()  # hex string

# MQTT: topic and payload must be bytes
mqtt_username = ""
mqtt_password = ""
mqtt_address = ""
mqtt_topic = lambda t: bytes("%s/%s" % (device_id, t), "utf-8")
mqtt_client_id = device_id
mqtt_port = 8883
