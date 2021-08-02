import network
import time
import config


def _connect(ssid, password):
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        print("Disabling wifi AP")
        ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to wifi network')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            time.sleep_ms(100)

    print('Connected', sta_if.ifconfig())


def connect():
    _connect(config.wifi_ssid, config.wifi_password)


def main():
    print("Running wifi...")
    connect()
    import socket
    # addr_info = socket.getaddrinfo("www.google.com", 80)
    addr_info = socket.getaddrinfo(config.mqtt_address, config.mqtt_port)
    addr = addr_info[0][-1]
    print("addr", addr)
    s = socket.socket()
    s.connect(addr)
    print("connected")
    while True:
        data = s.recv(500)
        print("data", data)
        # print(str(data, 'utf8'), end='')

    import test
    test.main()


if __name__ == "__main__":
    main()
