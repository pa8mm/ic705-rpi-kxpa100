# IC-705 Bluetooth Band Data Interface for KXPA100 Amplifier

A simple Band Data Interface using Raspberry Pi SBC. It uses an external HC-05 Bluetooth module for reading current operating frequency of the IC-705. Then it sets the band on the KXPA100 via the standard KXUSB serial cable.

## Manual

Make sure to enable a serial port in the raspi-config tool!

After wiring is completed, make sure that IC-705 is connected via the Bluetooth to the HC-05 and KXPA100 is connected to the Raspberry Pi SBC via standard KXUSB cable. Then run the script:

```
band-data-interface.py
./band-data-interface.py
```

PS - yes, I know it's an overkill to use full fledged Linux machine with an external Bluetooth module for such a simple task.
