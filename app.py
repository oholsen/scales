# https://github.com/SergeyPiskunov/micropython-hx711

import sys
from utime import sleep
from machine import reset

import board
import config
import wifi

from scales import scales
from mqtt import client


def main1():
    try:
        print("Running app.py")
        wifi.connect()
        print("Connecting to mqtt...")
        client.connect()
        while True:
            sleep(2)
            # TODO: should also power off the bridge - drive directly with pin? 5V over 2k is 3mA, should be ok. Test noise.
            # Could use FET - if can power down the ESP...
            # scales.power_on()
            # sleep to stabilize...
            weight = scales.stable_value()
            # scales.power_off()
            print("weight", weight)
            client.publish(config.mqtt_topic("weight"), bytes(str(weight), 'utf-8'))
    except Exception as e:
        sys.print_exception(e)
    finally:
        try:
            client.disconnect()
        except:
            pass
    print("Reset in 5 seconds...")
    sleep(5)
    reset()


def main2():
    try:
        print("Running app.py")
        board.led.value(1)
        wifi.connect()
        print("Connecting to mqtt...")
        client.connect()
        sleep(1)
        # TODO: should also power off the bridge - drive directly with pin? 5V over 2k is 3mA, should be ok. Test noise.
        # Could use FET - if can power down the ESP...
        # scales.power_on()
        # sleep to stabilize...
        weight = scales.stable_value()
        scales.power_off()
        print("weight", weight)
        client.publish(config.mqtt_topic("weight"), bytes(str(weight), 'utf-8'))
    except Exception as e:
        sys.print_exception(e)
    finally:
        try:
            client.disconnect()
        except Exception:
            pass
    board.led.value(0)
    print("Sleep in 5 seconds...")
    sleep(5)
    board.deep_sleep(20)


main = main2


if __name__ == "__main__":
    main()
