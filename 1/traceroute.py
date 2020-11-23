import subprocess
import sys
import os
def validIP(s):
	a=s.split(".")
	if len(a)!=4:
		return False
	return True
if __name__ == '__main__':
	waitTimeout=4
	dest=sys.argv[1]
	maxhops=30
	found=False
	numbytes=64
	ttle="Time to live exceeded"
	ip=""

	print("traceroute to",dest,maxhops, "hops max",numbytes, "byte packets")
	for i in range(1,maxhops+1):
		ip=""
		found=True
		output=os.popen("ping -W "+str(waitTimeout)+" -c 1 -t "+str(i)+"  "+dest).read()
		# print(output)
		o=output.split("\n")
		# print(o)

		if o[1]=='':
			print(i, "* * *")
			continue
		for ipstr in o:
			if ttle in ipstr:
				# print(ipstr)
				found=False
				ipstr=ipstr.replace("Time to live exceeded","")
				ipstr=ipstr.replace("From","")
				ipstr=ipstr.strip()
				string=ipstr.split(" ")
	
				if(validIP(string[0])):
					ip=string[0]
					print(i,ip, end=" ")
				elif(validIP(string[1].replace("(","").replace(")",""))):
					ip=string[1].replace("(","").replace(")","")					
					print(i,ip, end=" ")
				else:
					ip=""
					print(i,string[0], end=" * * *")
				break
			elif "ttl=" in ipstr:
				o=ipstr.split("(")
				sip=o[1]
				sip=sip.split(")")
				ip=sip[0]
				if(validIP(ip)):
					print(i,ip, end=" ")
				else:
					print(i, "* * *")
					ip=""
				break;
				#destination reached

		if ip!="":
			# ttli=i
			for it in range(3):
				# print(ip)
				output=os.popen("ping -W "+str(waitTimeout)+" -c 1 -t "+str(i)+"  "+ip).read()
				o=output.split("\n")
				f=False
				for string in o:
					# print(string)
					if "rtt" in string:
						f=True
						rttstr=string.split(" ")
						irtt=0
						for avgStr in rttstr[1].split("/"):
							if avgStr=="avg":
								break
							irtt+=1
						time=rttstr[3].split("/")[irtt]
						print(time, end=" ")
						break;
				if(not f):
					print("*", end=" ")
		print()

		if(found):
			break
	if(not found):
		print("TTL exceeded. Destination not reached")
	