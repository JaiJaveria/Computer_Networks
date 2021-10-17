import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr=('vayu.iitd.ac.in', 80)
sock.connect(addr)
msg=b'GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\n\r\n'
sock.sendall(msg)
while True:
	data=sock.recv(1)
	if len(data)<1:
		break
	data=data.decode()
	print(data, end="")
