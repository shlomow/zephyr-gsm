#!/usr/bin/env python3

import functools
import select
import serial
import socket

SERIAL_PATH = '/dev/serial/by-id/usb-ZEPHYR_USB-DEV_203136355836500F-if00'
ser = serial.Serial(SERIAL_PATH)

pppd_socket = socket.socket()
pppd_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
pppd_socket.bind(('', 8888))
pppd_socket.listen(1)

OK_RESULT = '\r\nOK\r\n'
CONNECT_RESULT = '\r\nCONNECT\r\n'

commands_dict = dict()

data_mode = False

def at_cmd(cmd_string):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            print(f'{cmd_string}')
            return f(*args, **kwargs)
        commands_dict[cmd_string] = wrapper
        return wrapper
    return decorator

'''
@at_cmd('AT')
def on_at(cmd):
    return OK_RESULT
'''

@at_cmd('ATE')
def on_e(cmd):
    return OK_RESULT

@at_cmd('ATH')
def on_h(cmd):
    return OK_RESULT

@at_cmd('AT+CMEE')
def on_cmee(cmd):
    return OK_RESULT

@at_cmd('AT+CGMI')
def on_cgmi(cmd):
    return OK_RESULT

@at_cmd('AT+CGMR')
def on_cgmr(cmd):
    return OK_RESULT

@at_cmd('AT+CGMM')
def on_cgmm(cmd):
    return OK_RESULT

@at_cmd('AT+CIMI')
def on_cimi(cmd):
    return OK_RESULT

@at_cmd('AT+CCID')
def on_ccid(cmd):
    return OK_RESULT

@at_cmd('AT+CGSN')
def on_cgsn(cmd):
    return OK_RESULT

@at_cmd('AT+CREG')
def on_creg(cmd):
    return OK_RESULT

@at_cmd('AT+CGDCONT')
def on_cgdcont(cmd):
    return OK_RESULT

@at_cmd('AT+COPS')
def on_cops(cmd):
    return OK_RESULT

@at_cmd('AT+CGATT')
def on_cgatt(cmd):
    resp = '+CGATT: 0,1\r\n'
    return resp + OK_RESULT

@at_cmd('ATD')
def on_dial(cmd):
    global data_mode
    data_mode = True
    return CONNECT_RESULT

def parse_data(buf):
    commands = buf.split(b'\r')
    last_cmd = commands[-1]
    commands = commands[:-1]
    for command in commands:
        command = command.decode()
        if command == 'AT':
            ser.write(OK_RESULT.encode())
            continue
        for known_command in commands_dict:
            if command.startswith(known_command):
                ser.write(commands_dict[known_command](command).encode())
                break
        else:
            print(f'unknown command: {command}')

    return last_cmd


def on_data_mode():
    print('start data mode')
    pppd, _ = pppd_socket.accept()
    while True:
        sers, _, _ = select.select([ser, pppd], [], [])
        for dev in sers:
            if dev is ser:
                pppd.sendall(ser.read_all())
            else:
                ser.write(pppd.recv(4096))

def main():
    remaining = b''
    while True:
        s = select.select([ser], [], [])
        buf = ser.read_all()
        remaining = parse_data(remaining + buf)
        if data_mode:
            on_data_mode()
            remaining = b''

if __name__ == '__main__':
    main()
