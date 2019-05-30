#!/usr/bin/python

import bluetooth

bd_addr = "00:18:E5:04:7A:EA"
port = 1
sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
sock.bind((bd_addr,port))

data = ""
while 1:
    try:
        data += sock.recv(1024)
        data_end = data.find('\n')
        if data_end != -1:
            rec = data[:data_end]
        data = data[data_end+1:]
	print(data)
    except Keyboardintterrupt:
        break
sock.close()
