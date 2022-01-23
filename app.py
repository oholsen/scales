import sys
import machine
import utime

import board
import mqtt
import wifi


# Power save:
# * boot grace time - could depend on digital IO state - on pin with pull up/down
# * LED blink
# * prints
# * sleeps
# * power weight bridge - drive directly with pin? 3.3V over 2k is 1.5mA, should be ok. Test noise.
# * ADC power


def loop():
    wifi.connect()
    # print("Connecting to mqtt...")
    mqtt.client.connect()
    while True:
        scale_adcs = board.scale.read_multiple(10, 5000)
        print("scale", scale_adcs)
        mqtt.client.publish(mqtt.topic("scale_adcs"), bytes(str(scale_adcs), 'utf-8'))
 
        # battery_adcs = [board.adc.read() for i in range(10)]
        # battery = board.battery()
        # print("battery_adcs", battery_adcs)
        # print("battery", battery)
        # mqtt.client.publish(mqtt.topic("battery"), bytes(str(battery), 'utf-8'))
        # mqtt.client.publish(mqtt.topic("battery_adcs"), bytes(str(battery_adcs), 'utf-8'))
 
        board.dht22.measure()
        temperature = board.dht22.temperature()
        humidity = board.dht22.humidity()       
        print("dht22 measured", temperature, humidity)
        mqtt.client.publish(mqtt.topic("temperature"), bytes(str(temperature), 'utf-8'))
        mqtt.client.publish(mqtt.topic("humidity"), bytes(str(humidity), 'utf-8'))

        utime.sleep(5)


def single():
    # measure before wifi noise
    battery_adcs = [board.adc.read() for i in range(10)]
    battery = board.battery()
    print("adcs", battery_adcs)
    print("battery", battery)

    wifi.connect()
    # print("Connecting to mqtt...")
    mqtt.client.connect()
    #mqtt.client.publish(mqtt.topic("weight"), bytes(str(weight), 'utf-8'))
    mqtt.client.publish(mqtt.topic("battery"), bytes(str(battery), 'utf-8'))
    mqtt.client.publish(mqtt.topic("battery_adcs"), bytes(str(battery_adcs), 'utf-8'))


def main():
    try:
        print("Running app.py")
        # board.led.value(1)

        # measure weight before radio noise
        # scales.power_on()
        # sleep to stabilize...
        #weight = scales.stable_value()
        #scales.power_off()
        #print("weight", weight)

        loop()
        # single()

    except Exception as e:
        sys.print_exception(e)
    finally:
        try:
            mqtt.client.disconnect()
        except Exception as e2:
            sys.print_exception(e2)
    # board.led.value(0)
    if 0:
        # this is required to complete mqtt transmission!?
        utime.sleep(1)
        board.deep_sleep(500)
    else:
        # debug
        print("Reset in 5 seconds...")
        utime.sleep(5)
        machine.reset()


if __name__ == "__main__":
    main()
