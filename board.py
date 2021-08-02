import machine

D0 = 16  # WAKE
D1 = 5
D2 = 4
D3 = 0
D4 = 2  # LED
D5 = 14
D6 = 12
D7 = 13
D8 = 15
# A0 is ADC0
# RX/TX is also GPIO
# I2C, SPI, UART2 in Dx pins

led = machine.Pin(2, machine.Pin.OUT)


def deep_sleep(secs: int):
    # Wire D0 to RST!
    print("Deep sleep for %d seconds..." % secs)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, secs * 1000)
    machine.deepsleep()


def main():
    import utime
    while True:
        print(".", end="")
        led.value(not led.value())
        utime.sleep_ms(1000)


if __name__ == "__main__":
    main()
