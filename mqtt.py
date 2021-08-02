import sys
import machine
import utime
import board
import config
import wifi
from umqtt.simple import MQTTClient

# MQTT: topic and payload must be bytes

def topic(t):
    return bytes("%s/%s" % (board.device_id, t), "utf-8")

client = MQTTClient(board.device_id, config.mqtt_address, config.mqtt_port, config.mqtt_username, config.mqtt_password)


def main():
    try:
        print("Running mqtt.py")
        wifi.connect()
        print("connecting to mqtt...")
        client.connect()
        while True:
            print("sleep 1")
            utime.sleep(1)
            print("publish")
            client.publish(topic("test"), bytes("hello world", 'utf-8'))
    except KeyboardInterrupt:
        try:
            client.disconnect()
        except:
            pass
        # sys.exit()
    except Exception as e:
        sys.print_exception(e)
        try:
            client.disconnect()
        except:
            pass
        print("Reset in 5 seconds...")
        utime.sleep(5)
        machine.reset()


if __name__ == "__main__":
    main()
