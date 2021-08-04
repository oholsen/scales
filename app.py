import sys
import machine
import utime

import board
import mqtt
import wifi

from scales import scales


# Power save:
# * boot grace time - could depend on digital IO state - on pin with pull up/down
# * LED blink
# * prints
# * sleeps
# * power weight bridge - drive directly with pin? 3.3V over 2k is 1.5mA, should be ok. Test noise.
# * ADC power


def main():
    try:
        print("Running app.py")
        # board.led.value(1)
        wifi.connect()
        # print("Connecting to mqtt...")
        mqtt.client.connect()
        # scales.power_on()
        # sleep to stabilize...
        weight = scales.stable_value()
        scales.power_off()
        print("weight", weight)
        mqtt.client.publish(mqtt.topic("weight"), bytes(str(weight), 'utf-8'))
    except Exception as e:
        sys.print_exception(e)
    finally:
        try:
            mqtt.client.disconnect()
        except Exception:
            pass
    # board.led.value(0)
    if 1:
        # print("Deep sleep for 20 seconds...")
        # utime.sleep(5)
        board.deep_sleep(20)
    else:
        # debug
        print("Reset in 5 seconds...")
        utime.sleep(5)
        machine.reset()


if __name__ == "__main__":
    main()
