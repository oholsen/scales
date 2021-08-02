# https://github.com/SergeyPiskunov/micropython-hx711

import sys
from utime import sleep
from machine import reset

import board
import config
import wifi

from scales import scales
from mqtt import client, topic

# power save:
# * LED blink
# * prints
# * sleeps

def main():
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
        client.publish(topic("weight"), bytes(str(weight), 'utf-8'))
    except Exception as e:
        sys.print_exception(e)
    finally:
        try:
            client.disconnect()
        except Exception:
            pass
    board.led.value(0)
    if 1:
        print("Deep sleep for 20 seconds in 5 seconds...")
        sleep(5)
        board.deep_sleep(20)
    else:
        # debug
        print("Reset in 5 seconds...")
        sleep(5)
        reset()


if __name__ == "__main__":
    main()
