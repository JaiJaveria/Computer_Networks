import socket
import sys
import math
import pandas as pd 
import threading as th
import time
# startG=6388635
startG=0
msglen=10000
lenFile=0
eof=False
finalAns=[]
def getstartingByte():
	global startG, eof, lenFile, msglen
	a=startG
	startG+=msglen
	if(startG>=lenFile):
		eof=True
	return a
	# return Range: bytes=6480000-6488665


def threadConnection(msg, addr, sock, start_lock, ans_lock):
	# noErr=True
	# print(sock)

	global msglen, eof, lenFile, finalAns
	breakOff=False

	while True:
		# if noErr:
		# print("28",sock)
		start_lock.acquire()
		# print(sock)
		# print("27",eof)
		if(eof):
			breakOff=True
			# print("37","break",sock,start,end, file=sys.stderr)
			# break
		start=getstartingByte()
		# print("31",eof)
		# print(start)
		# print(startG)
		start_lock.release()
		if breakOff:
			break
		end=start+msglen-1
		msglenT=msglen
		if end >lenFile-1:
			end=lenFile-1
			msglenT=end-start+1
		if end <=start:
			start_lock.acquire()
			eof=True
			start_lock.release()
			break
			# print("56","break",sock,start,end, file=sys.stderr)

			# print("broke from loop")

		finalmsg=msg+str(start)+'-'+str(end)+'\r\n\r\n'
		bfm=bytes(finalmsg,'ascii')
		sock.sendall(bfm)
		# print("s: ",start, sock)
		# print("e: ",end)
		# print("m:",msglenT)
		complete=True
		recv=False
		while not recv:
			# print("s: ",start)
			# print(sock)
			data=sock.recv(1)
			if len(data)<1:
				sock.shutdown(socket.SHUT_RDWR)
				sock.close()
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect(addr)
				sock.sendall(bfm)
				data=sock.recv(1)
			# data=data.decode()
			if data==b'\n':
				data=sock.recv(2)
				# data=data.decode()
				if data==b'\r\n':
					recvlen=0
					dataRecv=b""
					while recvlen<msglenT:
						# print(sock)
						# print(recvlen)
						# print(msglenT)
						# print("73--a")
						data=sock.recv(msglenT)
						# print(data)
						# print("75--b")

						recvlen+=len(data)
						if len(data)<1:
							sock.shutdown(socket.SHUT_RDWR)
							sock.close()
							sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							sock.connect(addr)
							sock.sendall(bfm)
							complete=False
							break
							# print("blank")
						dataRecv+=data
					# assert( recvlen==msglenT)
					if complete:
						# break
						recv=True
						# print("completed",start, sock)
						# print(dataRecv.decode(), flush=True, end="")
						ans_lock.acquire()
						finalAns.append((start,dataRecv))
						# datastr+=dataRecv
						ans_lock.release()
	# start_lock.release()

	# print("83--a", sock)		
def main():
	filename=sys.argv[1]
	host=[]
	hostname=""
	f=open(filename,'r')
	for line in f:
		h=line.split(',')
		url=h[0]
		if "://" in url:
			url=url.split('://')[1]
		arr=url.split("/")
		hostname=arr[0]
		obj=""
		for a in arr[1:]:
			obj+="/"+a
		# print(url)
		# print(hostname)
		# print(obj)
		host.append((int(h[1]),hostname,obj))
	# print(host)
	# host=["vayu.iitd.ac.in","norvig.com"]
	# msg1='GET /big.txt HTTP/1.1\r\nHost:'
	msg2='\r\nConnection: keep-alive\r\nRange: bytes='
	msgHead='HEAD '+host[0][2]+' HTTP/1.1\r\nHost: '+host[0][1]
	endmsg='\r\n\r\n'
	finalmsg=msgHead+endmsg
	s=time.time()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr=(host[0][1], 80)
	sock.connect(addr)
	bfm=bytes(finalmsg,'ascii')
	sock.sendall(bfm)
	data=sock.recv(1024)
	data=data.decode()
	data=(data.split())
	global lenFile
	for i in range(len(data)):
		if "Content-Length:" in data[i]:
			lenFile=int(data[i+1])
			# print(lenFile)
			break
	# start=0
	# msglen=10000
	# end=start+msglen-1
	# eof=False
	# if end > lenFile-1:
		# end=lenFile-1
		# eof=True
	# fd=open("debug.txt",'w')
	# print(eof,file=fd)
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()
	threadArr=[]
	start_lock=th.Lock()
	ans_lock=th.Lock()
	for i in host:
		for j in range(i[0]):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			msg='GET '+i[2]+' HTTP/1.1\r\nHost:'+i[1]+msg2
			addr=(i[1],80)
			sock.connect(addr)
			t= th.Thread(target=threadConnection, args=(msg, addr, sock, start_lock, ans_lock))
			threadArr.append(t)
			t.start()
	datastr=b""
	for t in threadArr:
		t.join()
	# print("finished--167")
	t=time.time()
	print("Time Taken: ",t-s, file=sys.stderr)
	global finalAns
	finalAns=sorted(finalAns, key=lambda x: x[0])
	for a in finalAns:
		datastr+=a[1]
	datastr=datastr.decode()
	print(datastr, end="")
if __name__ == '__main__':
	main()