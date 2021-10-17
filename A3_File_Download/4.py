import socket
import sys
import math
# import pandas as pd 
import threading as th
import time
# startG=6388635
startG=0
msglen=10000
lenFile=0
eof=False
finalAns=[]
connectRefresh=10
recvTimeOut=25
def restartSocket(sock, addr):
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	robustConnect(sock,addr)
	return sock
def robustConnect(sock,addr):
	global connectRefresh
	print("18--Robustly connecting", file=sys.stderr)
	while True:
		try:
			sock.connect(addr)
			# print("17--connected")
			break
		except:
			#if net off, exception is immediately raised
			# print("21--sleeping", file=sys.stderr)
			time.sleep(connectRefresh)		
	print("28--Robustly connection established", file=sys.stderr)

def getstartingByte():
	global startG, eof, lenFile, msglen
	a=startG
	startG+=msglen
	if(startG>=lenFile):
		eof=True
	return a
	# return Range: bytes=6480000-6488665
def threadConnection(msg, addr, sock, start_lock, ans_lock):
	# ()
	global msglen, eof, lenFile, finalAns
	breakOff=False

	while True:
		start_lock.acquire()
		if(eof):
			breakOff=True
		start=getstartingByte()
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
		finalmsg=msg+str(start)+'-'+str(end)+'\r\n\r\n'
		bfm=bytes(finalmsg,'ascii')
		successful=False
		while not successful:
			# print("start recieving", file=sys.stderr)
			sock.sendall(bfm)
			recv=False
			while not recv:
				try:
					data=sock.recv(1)
					if len(data)<1:
						sock=restartSocket(sock,addr)
						break
					if data==b'\n':
						data=sock.recv(2)#if this is allso empty then in the next itration it will be caught at data=sock.recv(1). Assumption: once it starts giving blank strings it will contnue giving them until restat happens.
						if data==b'\r\n':
							recvlen=0
							dataRecv=b""
							broken=False
							while recvlen<msglenT:
								data=sock.recv(msglenT)
								recvlen+=len(data)
								if len(data)<1:
									sock=restartSocket(sock,addr)
									broken=True
									break
									# print("blank")
								dataRecv+=data
							# assert( recvlen==msglenT)
							if not broken:
								recv=True
								ans_lock.acquire()
								finalAns.append((start,dataRecv))
								ans_lock.release()
								successful=True
							else:
								break
				# except socket.timeout as e:
				except:
					print("119-timeout inside thread while recieving. Restarting", file=sys.stderr)
					sock=restartSocket(sock,addr)
					break
	# print("83--a", sock)		
def main():
	global lenFile, recvTimeOut
	socket.setdefaulttimeout(recvTimeOut)
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
		host.append((int(h[1]),hostname,obj))
	msg2='\r\nConnection: keep-alive\r\nRange: bytes='
	msgHead='HEAD '+host[0][2]+' HTTP/1.1\r\nHost: '+host[0][1]
	endmsg='\r\n\r\n'
	finalmsg=msgHead+endmsg
	s=time.time()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr=(host[0][1], 80)
	bfm=bytes(finalmsg,'ascii')
	#establish a connection robustly
	robustConnect(sock,addr)
	successful=False
	#if timeout exception or content length not found in the header (rare) then restart again
	while not successful:
		# print("158--sleeping")
		# time.sleep(10)
		# print("161--times up")
		sock.sendall(bfm)
		# print("sent")
		# print("164--sleeping")
		# time.sleep(10)
		# print("166--times up")
		#if 1024 is less to capture length, keep on recieiving
		# times=0
		lenSet=False
		data=b""
		while not lenSet:
			# print("Still recieving", times)
			# times+=1
			try:
				d=sock.recv(1)
				if d==b'\n':
					d2=sock.recv(2)
					if d2==b'\r\n':
						lenSet=True
						# break
					else:
						data+=d+d2
				else:
					data+=d
			except:
				print("180--timeout while getting the length of data. restarting again", file=sys.stderr)
				break#start again
		if lenSet:
			data=data.decode()
			data=(data.split())
			for i in range(len(data)):
				if "Content-Length:" in data[i]:
					lenFile=int(data[i+1])
					successful=True
					# print(lenFile)
					break
	# print("196--",lenFile)
	# start=0
	# msglen=10000
	# end=start+msglen-1
	# eof=False
	# if end > lenFile-1:
		# end=lenFile-1
		# eof=True
	# fd=open("debug.txt",'w')
	# print(eof,file=fd)

	# print("206--sleeping")
	# time.sleep(10)
	# print("208--times up")
	
	#even if the net off then no excecption is raised below
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
			# sock.connect(addr)
			robustConnect(sock,addr)
			t= th.Thread(target=threadConnection, args=(msg, addr, sock, start_lock, ans_lock))
			threadArr.append(t)
			t.start()
	datastr=b""
	for t in threadArr:
		t.join()
	# print("finished--167")
	t=time.time()
	global finalAns
	finalAns=sorted(finalAns, key=lambda x: x[0])
	for a in finalAns:
		datastr+=a[1]
	datastr=datastr.decode()
	print(datastr, end="")
	print("Time Taken: ",t-s, file=sys.stderr)


if __name__ == '__main__':
	main()	