.. _gsm-modem-sample:

Generic GSM Modem Sample
########################

Overview
********

The Zephyr GSM modem sample application allows user to have a connection
to GPRS network. The connection to GSM modem is done using
PPP (Point-to-Point Protocol).


Run with Simulator
******************

If you want to connect your ppp device in the target to pppd on your pc
do the following:

1. Change SERIAL_PATH in `scripts/simulator.py` to your mcu uart device.
2. In terminal, run `./scripts/simulator.py`.
3. On another terminal, run `./scripts/run-pppd.sh`.


