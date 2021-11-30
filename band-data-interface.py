#!/usr/bin/env python3

import serial
import time

# Default device name and speed for KXUSB cable
KXPA100_SERIAL_PORT = "ttyUSB0"
KXPA100_SERIAL_SPEED = 38400

# Built-in UART port where we connect HC-05 module
IC705_SERIAL_PORT = "serial0"
IC705_SERIAL_SPEED = 9600


def kxpa100_set_band(freq):
    """
    Sets the band on the KXPA100 based on the frequency in KHz
    """
    ser = serial.Serial(f"/dev/{KXPA100_SERIAL_PORT}", KXPA100_SERIAL_SPEED)

    if freq < 2000:
        ser.write(b"^BN00;")
    elif freq > 2000 and freq < 5000:
        ser.write(b"^BN01;")
    elif freq > 5000 and freq < 6000:
        ser.write(b"^BN02;")
    elif freq > 6000 and freq < 8000:
        ser.write(b"^BN03;")
    elif freq > 9000 and freq < 11000:
        ser.write(b"^BN04;")
    elif freq > 13000 and freq < 15000:
        ser.write(b"^BN05;")
    elif freq > 18000 and freq < 19000:
        ser.write(b"^BN06;")
    elif freq > 20000 and freq < 22000:
        ser.write(b"^BN07;")
    elif freq > 24000 and freq < 25000:
        ser.write(b"^BN08;")
    elif freq > 27000 and freq < 30000:
        ser.write(b"^BN09;")
    elif freq > 50000:
        ser.write(b"^BN10;")

    ser.close()


def ic705_read_freq():
    """
    Reads the current frequency using CI-V commands
    """
    ser = serial.Serial(f"/dev/{IC705_SERIAL_PORT}", IC705_SERIAL_SPEED)

    # See IC-705 CI-V Reference guide
    data = bytearray([0xFE, 0xFE, 0xA4, 0xE0, 0x03, 0xFD])
    current_byte = 1
    khz1 = -1
    khz10 = -1
    khz100 = -1
    mhz1 = -1
    mhz10 = -1

    ser.write(data)
    ch = ser.read()

    while ch != b"\xfd":
        if current_byte == 5:
            # Sometimes, especially when reading a frequency during
            # a tuning, wrong command is returned.
            # We expect only x03 - operating frequency
            if ch != b"\x03":
                ser.close()
                return 0
        if current_byte == 6:
            hz10 = int.from_bytes(ch, "big") >> 4
            hz1 = int.from_bytes(ch, "big") & 0xF
        if current_byte == 7:
            khz1 = int.from_bytes(ch, "big") >> 4
            hz100 = int.from_bytes(ch, "big") & 0xF
        if current_byte == 8:
            khz100 = int.from_bytes(ch, "big") >> 4
            khz10 = int.from_bytes(ch, "big") & 0xF
        if current_byte == 9:
            mhz10 = int.from_bytes(ch, "big") >> 4
            mhz1 = int.from_bytes(ch, "big") & 0xF
        ch = ser.read()
        current_byte += 1

    # Again, sometimes incorrect data is returned during a read.
    # We simply ignore it and retry calling this function again
    if khz1 == -1 or khz10 == -1 or khz100 == -1 or mhz10 == -1 or mhz1 == -1:
        return 0

    freq = int(f"{mhz10}{mhz1}{khz100}{khz10}{khz1}")
    ser.close()

    return freq


def main():
    while True:
        freq = ic705_read_freq()
        if freq != 0:
            kxpa100_set_band(freq)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
