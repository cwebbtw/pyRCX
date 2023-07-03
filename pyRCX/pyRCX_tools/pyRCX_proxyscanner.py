import socket
import random
import time

oper_details = "3 mypassword"
server_details = ("127.0.0.1",6667)
server = "pyRCX" # use "unreal" for unreal


def main():

	print " _____  __    __  _____    _____  __    __ "
	print "|  _  \ \ \  / / |  _  \  /  ___| \ \  / / "
	print "| |_| |  \ \/ /  | |_| |  | |      \ \/ /  "
	print "|  ___/   \  /   |  _  /  | |       }  {   "
	print "| |       / /    | | \ \  | |___   / /\ \  "
	print "|_|      /_/     |_|  \_\ \_____| /_/  \_\ v2.5"
	print "__________________________________________"
	print ""
	print "* Developed by chrisjw"
	print "* Python: www.python.org"
	print "* IRC:    irc.freenode.org"
	print "__________________________________________"
	print ""
	print "*** Proxy scanner started successfully"

	while 1:
		sock_connected = False
		msock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			msock.connect(server_details)
			sock_connected = True

		except socket.error, (value,message):
			pass

		if sock_connected:
			pyRCX_nick = "pyRCX_proxyscanner"

			msock.sendall("NICK %s\r\nUSER p 0 0 :pYRCX proxy scanning agent\r\n" % (pyRCX_nick))
			msock.sendall("OPER %s\r\nMODE %s +iwhs\r\n" % (oper_details,pyRCX_nick))

			while 1:
				pyRCX_data = ""
				while 1:
					try:
						char = msock.recv(1)
					except:
						break

					if char == "\r" or char == "\n":
						break
					else:
						pyRCX_data += char

				try:
					params = pyRCX_data.split(" ")
					if params[0] == "PING": msock.sendall("PONG %s\r\n" % (params[1]))
					if params[1] == "NOTICE" and "!" not in params[0]: # make sure it is not a user sending this message
						if params[3] == ":***" and params[6] + params[7] == "UserConnecting":
							user_ip = params[12].replace("[","").replace("]","")
							user_nick = params[11].split("!")[0].replace("(","")
							ports = (1080,3124,3128,6789,8080)
							msock.sendall("NOTICE %s :Your host is being scanned for any open proxies or tor servers\r\n" % (user_nick))

							f = user_ip.split(".")
							f.reverse()
		
							try:
								socket.gethostbyname(".".join(f) + ".tor.ahbl.org")
								msock.sendall("KILL %s :TOR server found on your host, please contact tor blacklist\r\n" % (user_nick))

								

								msock.sendall("ACCESS * ADD DENY @%s 0 :Permanently banned, blacklisted host found on host\r\n" % (user_ip))
							except:
								for each in ports:
									chksock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
									chksock.settimeout(0.2)
									try:
										chksock.connect((user_ip,each))
										msock.sendall("KILL %s :Open proxy found on your host, if you believe you have a problem, please virus scan your system for spyware and contact the service administrator\r\n"% (user_nick))
										msock.sendall("ACCESS * ADD DENY @%s 0 :Permanently banned, open proxy found on host\r\n" % (user_ip))
									except socket.error:
										pass

				except IndexError:
					pass

		time.sleep(10)

if __name__ == "__main__":
	import os,sys
	if hasattr(os,"fork"):
		try: 
			pid = os.fork() 
			if pid > 0: sys.exit(0) 
		except OSError: 
			sys.exit(1)
		
		os.setsid()
		os.umask(0)
		try: 
			pid = os.fork() 
			if pid > 0:
				sys.exit(0)
		except OSError: 
			sys.exit(1)
	else:
		pass
	
	main()
