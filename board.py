import machine
import ubinascii
from hx711 import HX711
from dht import DHT22


########################################
# Wemos D1 Mini (ESP8266) board
########################################

# Wemos D1 mini label to GPIO number
D0 = 16  # WAKE
D1 = 5  # SCL
D2 = 4  # SDA
D3 = 0
D4 = 2  # LED
D5 = 14
D6 = 12
D7 = 13
D8 = 15
# A0 is ADC0
# RX/TX is also GPIO
# I2C, SPI, UART2 in Dx pins

adc = machine.ADC(0)
led = machine.Pin(2, machine.Pin.OUT, value=1) # LED off on pro....
device_id = ubinascii.hexlify(machine.unique_id()).decode() # hex string

scale = HX711(d_out=D5, pd_sck=D6, channel=HX711.CHANNEL_A_64)

# dht22_power = machine.Pin(D7, machine.Pin.OUT, value=1)
dht22 = DHT22(machine.Pin(D2))  # SDA


def deep_sleep(secs: int):
    # Wire D0 to RST!
    print("Deep sleep for %d seconds..." % secs)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, secs * 1000)
    machine.deepsleep()


def battery() -> float:
    """Return battery voltage in volts"""
    # Lolin D1 Mini Pro:
    # Vbat - 130k - A0 - 220k - ADC - 100k - GND
    # ADC = 100 / (130 + 220 + 100) * Vbat
    # ADC is 1024 at 1V
    # calibration factor
    return (0.985 * 4.5 / 1024) * min(adc.read() for i in range(5))


def main():
    import utime
    while True:
        print("battery", battery())
        # for i in range(5): print("battery adc", adc.read())
        # print(".", end="")
        led.value(not led.value())
        utime.sleep_ms(1000)


if __name__ == "__main__":
    main()
