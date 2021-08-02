# https://github.com/SergeyPiskunov/micropython-hx711

from hx711 import HX711
from utime import sleep, sleep_us
from board import led, D5, D6


class Scales(HX711):
    def __init__(self, d_out, pd_sck):
        super(Scales, self).__init__(d_out, pd_sck, channel=HX711.CHANNEL_A_64)
        self.offset = 0

    def reset(self):
        self.power_off()
        self.power_on()

    def tare(self):
        self.offset = self.stable_value()

    def raw_value(self):
        return self.read() - self.offset

    def stable_value(self, reads=10, delay_us=500):
        values = []
        for _ in range(reads):
            values.append(self.raw_value())
            sleep_us(delay_us)
        return self._stabilizer(values)

    @staticmethod
    def _stabilizer(values, deviation=10):
        return sum(values) / len(values)
        weights = []
        for prev in values:
            weights.append(sum([1 for current in values if abs(prev - current) / (prev / 100) <= deviation]))
        return sorted(zip(values, weights), key=lambda x: x[1]).pop()[0]


scales = Scales(d_out=D5, pd_sck=D6)


def main():
    print("Running scales.py")
    # hx711 = HX711(d_out=D5, pd_sck=D6)
    # scales.tare()
    # print("Tare", scales.offset)

    while True:
        # print("weighing...")
        # val = hx711.read_raw()
        # val = hx711.read()
        # print("raw", val)

        # sleep to stabilize...
        weight = scales.stable_value()
        print("weight", weight)
        # TODO: should also power off the bridge - drive directly with pin? 5V over 2k is 3mA, should be ok. Test noise.
        # Could use FET - if can power down the ESP...
        # scales.power_off()
        led.value(not led.value())
        sleep(2)
        # scales.power_on()


if __name__ == "__main__":
    main()
