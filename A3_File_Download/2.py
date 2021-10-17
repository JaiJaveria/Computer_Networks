import socket
import sys
import math
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr=('vayu.iitd.ac.in', 80)
sock.connect(addr)
msg='GET /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in\r\nConnection: keep-alive\r\nRange: bytes='
msgHead='HEAD /big.txt HTTP/1.1\r\nHost: vayu.iitd.ac.in'
endmsg='\r\n\r\n'
finalmsg=msgHead+endmsg
bfm=bytes(finalmsg,'ascii')
sock.sendall(bfm)
data=sock.recv(1024)
data=data.decode()
data=(data.split())
lenFile=0
for i in range(len(data)):
	if "Content-Length:" in data[i]:
		lenFile=int(data[i+1])
		break
start=0
msglen=10000
end=start+msglen-1
eof=False
if end > lenFile-1:
	end=lenFile-1
	eof=True
fd=open("debug.txt",'w')
# print(eof,file=fd)
datastr=b""

while True:
	finalmsg=msg+str(start)+'-'+str(end)+endmsg
	bfm=bytes(finalmsg,'ascii')
	sock.sendall(bfm)
	update=True
	recv=False
	while not recv:
		data=sock.recv(1)
		if len(data)<1:
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(addr)
			sock.sendall(bfm)
			data=sock.recv(1)
		data=data.decode()
		if data=='\n':
			data=sock.recv(2)
			data=data.decode()
			if data=='\r\n':
				recvlen=0
				dataRecv=b""
				while recvlen<msglen:
					data=sock.recv(msglen)
					recvlen+=len(data)
					if len(data)<1:
						sock.shutdown(socket.SHUT_RDWR)
						sock.close()
						sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						sock.connect(addr)
						update=False
						break
						# print("blank")
					dataRecv+=data
				assert( recvlen==msglen)
				recv=True
				datastr+=dataRecv

	if eof:
		break
	if update:
		start+=msglen
		end+=msglen
	if end > (lenFile-1):
		end=lenFile-1
		msglen=end-start+1
		eof=True
datastr=datastr.decode()
print(datastr, end="")