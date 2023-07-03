import threading

# memory happy iterations

import itertools

# Random generator

from random import random

import socket
import re

import time

import os

# Select module

from select import select
from copy import copy

#error reporting20/06/2007
 
import sys

from traceback import extract_tb

#link hashing

import sha


import errno

# link compression
try:
	from zlib import compress,decompress
except ImportError: # compression isn't mandatory but linking servers must support linking

	print "*** IMPORTANT: zlib is not installed on this copy of python, either install it or make sure that the server you link with also doesn't have zlib installed"

	def compress(blah):
		return blah

	def decompress(blah):
		return blah

# link object serialization

from pickle import dumps,loads

# link NTP

from struct import unpack

# Nickserv

#Here are some settings, these can be coded into the conf later I suppose



BotFile = ""
DefaultModes = "ntl 75"

NickfloodAmount = 5
NickfloodWait = 30
MaxChannels = 50
MaxChannelsPerUser = 10
MaxServerEntries = 0
MaxUserEntries = 0
MaxChannelEntries = 0
HostMasking = 0
HostMaskingParam = ""
ipaddress = ""
PrefixChar = ""
ChanPrefix = "#"
AdminPassword = ""
ServerAddress = ""
NetworkName = ""
ServerAdmin1 = ""
ServerAdmin2 = ""
ServerName = ""
ServerPassword = ""
passmsg = ""
MaxUsers = 10
MaxUsersPerConnection = 3
ServerLaunch = time.strftime(" :On-line since %A %B %d %H:%M:%S %Y",time.localtime())
NickservParam = ""
defconMode = 1

ChanLockDown = 0

NTPtime = 0
timeDifference = 0
NTPServer = ""


Ports = []
FloodingExempt = []
profanity = []
temp_noopers = []
Filter = []
operlines = []
connections = []
invisible = []
unknownConnections = []
connectionsExempt = []
opersecret = []
ServerAccess = []
servers = []
linkedServers = []

createmute = {}
nickmute = {}
Nickserv = {}
nicknames = {}
opers = {}
channels = {}
currentports = {}
Disabled = {}
NickservIPprotection = True

# L:<method>:<server name>:<server address>:<port>:<password>:<info>;

# servers.append(ServerInformation(s_line[1],s_line[2],s_line[3],s_line[4],s_line[5],s_line[6]))

class ServerInformation:
	def __init__(self,method,serverName,serverAddress,port,password,info):
		self._sock = None
		self._method = method
		self._serverName = serverName
		self._info = info
		self._serverAddress = serverAddress
		self._port = int(port)
		self._password = password

		self._linkfail = 0

		self._use = False
		self._close = False
		self._authenticated = False

class LinkOpers:
	operlevel = 0
	guide = False
	hidden = False
	watchserver = False
	watchbans = False
	watchnickserv = False
	usage = False

	def __init__ (self,username,password,flags,filename):
		self.username = username
		self.password = password
		self.flags = flags
		self.filename = filename

class ChannelBaseClass:
	def __init__(self):
		self._users = {}
		self._watch = []
		self._prop = None
		self.channelname = ""
		self._topic = ""
		self._topic_time = 0
		self._topic_nick = ""
		self._founder = ""

		self._voice = []
		self._op = []
		self._owner = []

		self.localChannel = False

		self.ChannelAccess = []
		self.cloneindex = 0
		self.totalclones = 0
		self.cloneid = self

		self.MODE_inviteonly = False
		self.MODE_moderated = False
		self.MODE_createclone = False
		self.MODE_noclones = False
		self.MODE_cloneroom = False
		self.MODE_ownersetmode = False
		self.MODE_gagonban = False
		self.MODE_ownerkick = False
		self.MODE_Adminonly = False
		self.MODE_profanity = False
		self.MODE_servicechan = False
		self.MODE_ownersetprop = False
		self.MODE_ownersetaccess = False
		self.MODE_registeredonly = False
		self.MODE_whisper = False
		self.MODE_secret = False
		self.MODE_nomodechanges = False
		self.MODE_hidden = False
		self.MODE_ownertopic = False
		self.MODE_optopic = False
		self.MODE_externalmessages = False
		self.MODE_registered = False
		self.MODE_auditorium = False
		self.MODE_authenticatedclients = False
		self.MODE_private = False
		self.MODE_nocolour = False
		self.MODE_stripcolour = False
		self.MODE_knock = False
		self.MODE_noircx = False
		self.MODE_limitamount = "75"
		self.MODE_limit = False
		self.MODE_key = ""

	def GetChannelModes(self,objid,nokey=False):
		modestr = ""
		if self.MODE_moderated: modestr+="m"
		if self.MODE_noclones: modestr+="K"
		if self.MODE_cloneroom: modestr+="e"
		if self.MODE_createclone: modestr+="d"
		if self.MODE_ownersetmode: modestr+="M"
		if self.MODE_Adminonly: modestr+="A"
		if self.MODE_ownerkick== True: modestr+="Q"
		if self.MODE_profanity: modestr+="f"
		if self.MODE_whisper: modestr+="w"
		if self.MODE_gagonban: modestr +="G"
		if self.MODE_secret: modestr+="s"
		if self.MODE_nomodechanges: modestr+="S"
		if self.MODE_inviteonly: modestr+="i"
		if self.MODE_hidden: modestr+="h"
		if self.MODE_private: modestr+="p"
		if self.MODE_externalmessages: modestr+="n"
		if self.MODE_ownersetprop: modestr+="P"
		if self.MODE_optopic: modestr+="t"
		if self.MODE_ownertopic: modestr+="T"
		if self.MODE_registered: modestr+="r"
		if self.MODE_auditorium: modestr+="x"
		if self.MODE_registeredonly: modestr+="R"
		if self.MODE_ownersetaccess: modestr+="X"
		if self.MODE_noircx: modestr+="Z"
		if self.MODE_authenticatedclients: modestr+="a"
		if self.MODE_servicechan: modestr+="N"
		if self.MODE_nocolour: modestr+="c"
		if self.MODE_stripcolour: modestr+="C"
		if self.MODE_knock: modestr+="u"
		if self.MODE_limit:
			mstr = modestr.split(" ")
			if self.MODE_key == "":
				modestr = mstr[0] + "l " + self.MODE_limitamount
			else:
				if objid == 0 or objid in self._users:
					modestr = mstr[0].replace("k","") + "lk " + self.MODE_limitamount + " " + self.MODE_key
				else:
					modestr = mstr[0].replace("k","") + "lk " + self.MODE_limitamount

		if self.MODE_key != "" and nokey == False:
			mstr = modestr.split(" ")
			if self.MODE_limit:
				if objid == 0 or objid in self._users:
					modestr = mstr[0].replace("k","") + "k " + self.MODE_limitamount + " " + self.MODE_key
				else:
					modestr = mstr[0].replace("k","") + "k " + self.MODE_limitamount
			else:
				modestr = mstr[0] + "k " + self.MODE_key
		
		return modestr

	def isBanned(self,cid):
		_Access.CheckChannelExpiry(self)
		if cid._nickname.lower() in opers or isOp(cid._nickname,self.channelname): return False
		for each in self.ChannelAccess:
			if each._level.upper() == "DENY":
				ret = _Access.MatchAccess(each._mask,cid)
				if ret == 1:
					_override = False
					for eachgrant in self.ChannelAccess:
						if eachgrant._level.upper() != "DENY":
							gret = _Access.MatchAccess(eachgrant._mask,cid)
							if gret == 1:
								_override = True
								break

					if _override: return False
					return True
		return False

	def ClearUsersModes (self,nick):
		if nick.lower() in self._owner: self._owner.remove(nick.lower())
		if nick.lower() in self._op: self._op.remove(nick.lower())
		if nick.lower() in self._voice: self._voice.remove(nick.lower())
		
	def kick(self,nick,knick,kickmsg):
		clientid = nicknames[knick.lower()]
		ChanCopyNames = list(self._users)
		for each in ChanCopyNames:
			cclientid = nicknames[each.lower()]
			if self.MODE_auditorium == False or isOp(cclientid._nickname,self.channelname) or isOp(nick._nickname,self.channelname) or isOp(knick._nickname,self.channelname) or cclientid._nickname.lower() == knick.lower():
				cclientid.send(":%s!%s@%s KICK %s %s :%s\r\n" % (nick._nickname,nick._username,nick._hostmask,self.channelname,knick,kickmsg))

		if self.channelname in clientid._channels: clientid._channels.remove(self.channelname)
		self.__remuser(knick,False)
		

		if self._prop.onpart != "":
			iloop = 0
			numstr = len(self._prop.onpart.split("\\n"))
			while iloop < numstr:
				clientid.send(":%s NOTICE %s :%s\r\n" % (self.channelname,clientid._nickname,self._prop.onpart.split("\\n")[iloop] ))
				iloop+=1
		
		if len(self._users) == 0:
			self.resetchannel()

	def sendnames(self,nick,owner=False,sendwatch=False):
		cclientid = getUserOBJ(nick.lower())
		str_chanlist = ""
		iloop = 0
		if isSecret(self,"private","hidden") == False or nick.lower() in self._users or nick.lower() in opers:
			for each in list(self._users):
				cid = getUserOBJ(each)
				iloop+=1
				if iloop == 20:
					raw(cclientid,"353",cclientid._nickname,self.channelname,str_chanlist[1:])
					str_chanlist = ""
					iloop = 0

				if self.channelname in cid._watch:
					if cclientid == cid:
						if cclientid._IRCX and self.MODE_noircx == False: str_chanlist += " ."
						else: str_chanlist += " @"

						if cid._nickname.lower() in self._voice: str_chanlist += "+"
						
						str_chanlist += cid._nickname

				elif cid._nickname.lower() in self._owner or cid._nickname.lower() in self._op or cid._nickname.lower() in self._voice:

					if nick.lower() not in self._users and cid._MODE_invisible and nick.lower() not in opers:
						pass
					else:
						isVoice = False
						if cid._nickname.lower() in self._voice:
							isVoice = True
						
						if cid._nickname.lower() in self._op:
							str_chanlist += " @"
							if isVoice: str_chanlist+="+"

							str_chanlist += cid._nickname

						elif cid._nickname.lower() in self._owner:
							if cclientid._IRCX:
								if self.MODE_noircx:
									str_chanlist += " @"
								else:
									str_chanlist +=  " ."
							else:
								str_chanlist += " @"
							
							if isVoice: str_chanlist+="+"

							str_chanlist+=cid._nickname

						else:
							str_chanlist += " +" + cid._nickname

				else:
					if nick.lower() not in self._users and cid._MODE_invisible and nick.lower() not in opers:
						pass
					else:
						if self.MODE_auditorium:
							if isOp(nick,self.channelname) or cid._nickname.lower() == nick.lower():
								str_chanlist = str_chanlist + " " + cid._nickname
						else:
							str_chanlist = str_chanlist + " " + cid._nickname
		
			if str_chanlist != "":
				raw(cclientid,"353",cclientid._nickname,self.channelname,str_chanlist[1:])

		raw(cclientid,"366",cclientid._nickname,self.channelname)

			
	def __remuser(self,nick,sendmsg): # remove users from the user record for this channel
		if nick.lower() in self._users:
			#cclientid = nicknames[nick.lower()]
			cclientid = getUserOBJ(nick.lower())
			if self.channelname in cclientid._watch: cclientid._watch.remove(self.channelname)
			if sendmsg:

				if nick.lower() in self._watch:
					cclientid.send(":%s!%s@%s PART %s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname))
				else:
					for each in list(self._users):
						#clientid = nicknames[each.lower()]
						clientid = getUserOBJ(each.lower())
						if self.MODE_auditorium == False or isOp(clientid._nickname,self.channelname) or isOp(cclientid._nickname,self.channelname) or cclientid == clientid:
							clientid.send(":%s!%s@%s PART %s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname))


			self.ClearUsersModes(nick.lower()) # once a user leaves the channel, they lose their modes, it's now up to access to give them the modes back if enabled
			if nick.lower() in self._watch: self._watch.remove(nick.lower())
			del self._users[nick.lower()]
			return True
		else:
			return False # return false if user wasn't on the channel to begin with

	def __adduser(self,nick,key=""):
		if nick.lower() in self._users:
			return -1 # return False if user is already in channel
		else:
			cclientid = nicknames[nick.lower()]
			haskey = False
			if self.MODE_authenticatedclients and nick.lower() not in opers: return 0
			
			if self.MODE_Adminonly:
				if nick.lower() in opers:
					opid = opers[nick.lower()]
					if opid.operlevel >=3:
						cclientid._channels.append(self.channelname)
						self._users[nick.lower()] = cclientid
					else:
						return -4
				else:
					return -4

			if self.MODE_registeredonly:
				if nick.lower() in opers:
					pass
				else:
					if cclientid._MODE_register == False:
						return -6
					
			if key != "":
				if key == self._prop.ownerkey: haskey = True
				if key == self._prop.hostkey: haskey = True

			if self.MODE_limit:
				if len(self._users) >= myint(self.MODE_limitamount) and nick.lower() not in opers and haskey == False:
					return -3

			if self.MODE_noclones and nick.lower() not in opers:
				susers = copy(self._users)
				for each in susers:
					uid = nicknames[each.lower()]
					if uid.details[0] == cclientid.details[0]:
						return -7

			if self.MODE_inviteonly and nick.lower() not in opers:
				cid = nicknames[nick.lower()]
				if self.channelname.lower() not in cid._invites and haskey == False: return -2

			if nick.lower() not in opers and nick.lower() not in self._op and nick.lower() not in self._owner:
				for each in self.ChannelAccess:
					if each._level.upper() == "DENY":
						ret = _Access.MatchAccess(each._mask,cclientid)
						if ret == 1:
							_override = False
							for eachgrant in self.ChannelAccess:
								if eachgrant._level.upper() != "DENY":
									gret = _Access.MatchAccess(eachgrant._mask,cclientid)
									if gret == 1:
										_override = True
										break

							if _override: break

							return -5 # no access!!!

			if self.channelname.lower() in cclientid._invites: cclientid._invites.remove(self.channelname.lower())
			cclientid._channels.append(self.channelname)
			self._users[nick.lower()] = cclientid
			return 1
			
	def resetchannel(self,killchan=False):
		if self.MODE_registered or self.MODE_servicechan: pass
		elif self._prop.reset != 0 and killchan == False:
			PropResetChannel(self).start()
		else:
			#self._users = {}
			#self._watch = []
			#self._prop = None
			#self._topic = ""
			#self.ChannelAccess = []
			delGlobalChannel(self.channelname.lower())
			#self.channelname = ""
			del self

	def updateuser(self,oldnick,newnick): # This function will update the user record for this channel
		if oldnick.lower() in self._users:
			if oldnick.lower() in self._op: self._op.append(newnick.lower())
			if oldnick.lower() in self._owner: self._owner.append(newnick.lower())
			if oldnick.lower() in self._voice: self._voice.append(newnick.lower())
			self.ClearUsersModes(oldnick)

			del self._users[oldnick.lower()]
			self._users[newnick.lower()] = getUserOBJ(oldnick.lower())
			return True
		else:
			return False

	def part(self,partuser):
		cclientid = getUserOBJ(partuser.lower())
		if cclientid:
			if self.__remuser(partuser,True) == False:
				raw(cclientid,"442",cclientid._nickname,self.channelname)
				return False
			else:
				cclientid._channels.remove(self.channelname)

				if self._prop.onpart != "":
					iloop = 0
					numstr = len(self._prop.onpart.split("\\n"))
					while iloop < numstr:
						cclientid.send(":%s NOTICE %s :%s\r\n" % (self.channelname,cclientid._nickname,self._prop.onpart.split("\\n")[iloop] ))
						iloop+=1
				
				if len(self._users) == 0:
					self.resetchannel()

				return True
	
	def quit(self,quituser):
		self.__remuser(quituser,False)

		if len(self._users) == 0:
			self.resetchannel()

	def join(self,joinuser,key=""):
		_Access.CheckChannelExpiry(self)
		_r = self.__adduser(joinuser,key)
		cclientid = getUserOBJ(joinuser.lower())

		if joinuser.lower() not in opers and _r != -1 and _r != -4 and _r != 0 and _r != -6: #opers not affected
			for each in self.ChannelAccess:
				if each._level.upper() != "DENY" and each._level.upper() != "GRANT":
					ret = _Access.MatchAccess(each._mask,cclientid)
					if ret == 1:
						if each._level.upper() == "OWNER":
							if joinuser.lower() in self._op: self._op.remove(joinuser.lower())
							if joinuser.lower() not in self._owner: self._owner.append(joinuser.lower())
							_r = 1
							break

						if each._level.upper() == "HOST":

							if joinuser.lower() in self._owner:
								break
							else:
								if joinuser.lower() not in self._op: self._op.append(joinuser.lower())
								_r = 1

						if each._level.upper() == "VOICE":
							if joinuser.lower() not in self._voice: self._voice.append(joinuser.lower())
							_r = 1


		if _r == 1:

			if self.MODE_noircx:
				if joinuser.lower() in self._owner:
					self._owner.remove(joinuser.lower())
					if joinuser.lower() not in self._op: self._op.append(joinuser.lower())

			if self.channelname.lower() in cclientid._invites: cclientid._invites.remove(self.channelname.lower())
			if self.channelname not in cclientid._channels: cclientid._channels.append(self.channelname)
			if joinuser.lower() not in self._users: self._users[joinuser.lower()] = cclientid

			keyjoin=0

			isoper=False
			if joinuser.lower() in opers:
				if self.MODE_noircx:
					if joinuser.lower() not in self._op: self._op.append(joinuser.lower()) # make opers owner of channel automatically
				else:
					if joinuser.lower() not in self._owner: self._owner.append(joinuser.lower()) # make opers owner of channel automatically

				isoper=True

			if self.channelname in cclientid._watch:
				self._watch.append(joinuser.lower())
				cclientid.send(":%s!%s@%s JOIN :%s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname))
			else:
				ChanCopyNames = list(self._users)
				for each in ChanCopyNames:
					clientid = getUserOBJ(each.lower())
					if self.MODE_auditorium == False or isOp(clientid._nickname,self.channelname) or isOp(cclientid._nickname,self.channelname) or clientid == cclientid:
						if isoper or key == self._prop.ownerkey and key != "" or joinuser.lower() in self._owner:
							keyjoin = 2
							if clientid._IRCX and self.MODE_noircx == False: clientid.send(":%s!%s@%s JOIN :%s\r\n:%s MODE %s +q %s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname,ServerName,self.channelname,cclientid._nickname))
							else:	 clientid.send(":%s!%s@%s JOIN :%s\r\n:%s MODE %s +o %s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname,ServerName,self.channelname,cclientid._nickname))

						elif key == self._prop.hostkey and key != "" or joinuser.lower() in self._op:
							clientid.send(":%s!%s@%s JOIN :%s\r\n:%s MODE %s +o %s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname,ServerName,self.channelname,cclientid._nickname))
							keyjoin = 1

						elif joinuser.lower() in self._voice and joinuser.lower() not in self._op and joinuser.lower() not in self._owner:
							clientid.send(":%s!%s@%s JOIN :%s\r\n:%s MODE %s +v %s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname,ServerName,self.channelname,cclientid._nickname))
						else:
							clientid.send(":%s!%s@%s JOIN :%s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname))
							

				del ChanCopyNames

			if keyjoin == 1:
				if joinuser.lower() not in self._op: self._op.append(joinuser.lower())
			elif keyjoin == 2:
				if self.MODE_noircx:
					if joinuser.lower() not in self._owner: self._op.append(joinuser.lower())
				else:
					if joinuser.lower() not in self._owner: self._owner.append(joinuser.lower())

			elif keyjoin == 3:
				if joinuser.lower() not in self._voice: self._voice.append(joinuser.lower())

			if self._topic != "":
				raw(cclientid,"332",cclientid._nickname,self.channelname,self._topic)
				raw(cclientid,"333",cclientid._nickname,self.channelname,self._topic_nick,self._topic_time)
			
			self.sendnames(cclientid._nickname,False,True)

			if self._prop.onjoin != "": 
				iloop = 0
				numstr = len(self._prop.onjoin.split("\\n"))
				while iloop < numstr:
					cclientid.send(":%s PRIVMSG %s :%s\r\n" % (self.channelname,self.channelname,self._prop.onjoin.split("\\n")[iloop] ))
					iloop+=1
		else:
			k_numeric = ""
			if _r == -1:	
				raw(cclientid,"927",cclientid._nickname,self.channelname)

			elif _r == -2:
				raw(cclientid,"473",cclientid._nickname,self.channelname)
				if self.MODE_knock: k_numeric = "473"

			elif _r == -3:
				if self.MODE_createclone:
					
					newc = self.cloneid.channelname + str(self.cloneindex + 1)

					if newc.lower() in channels: # get rid of any channels that were made before clone rooms were created
						chanid = channels[newc.lower()]
						if chanid.MODE_cloneroom == False:
							for each in chanid._users:
								cid = getUserOBJ(each.lower())
								raw(cid,"934",cid._nickname) # LINK NOTE: sendRawDataHere

							chanid.resetchannel()
						else:
							chanid.join(joinuser)
							return

					channels[newc.lower()] = copy(self)
					newchan = channels[newc.lower()]
					newchan.cloneid = self.cloneid
					newchan.cloneindex = self.cloneindex + 1
					newchan.channelname = newc
					newchan.MODE_cloneroom = True
					newchan._users = {}
					newchan.join(joinuser)

				else:
					raw(cclientid,"471",cclientid._nickname,self.channelname)
					if self.MODE_knock: k_numeric = "471"

			elif _r == -4:	
				raw(cclientid,"483",cclientid._nickname,self.channelname,"You are not an Administrator")
				if self.MODE_knock: k_numeric = "483"

			elif _r == -5:
				raw(cclientid,"913",cclientid._nickname,self.channelname)
				if self.MODE_knock: k_numeric = "913"

			elif _r == -6:
				raw(cclientid,"477",cclientid._nickname,self.channelname)
				if self.MODE_knock: k_numeric = "477"

			elif _r == -7:
				raw(cclientid,"483",cclientid._nickname,self.channelname,"User with same address already in channel")
				if self.MODE_knock: k_numeric = "483"

			elif _r == 0:
				raw(cclientid,"520",cclientid._nickname,self.channelname)
				if self.MODE_knock: k_numeric = "520"

			if k_numeric:
				for each in copy(self._users):
					clientid = getUserOBJ(each)
					clientid.send(":%s!%s@%s KNOCK %s %s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,self.channelname,k_numeric))

	def communicate(self,msguser,nop,msg):
		cclientid = nicknames[msguser.lower()]
		if msguser.lower() in self._users or self.MODE_externalmessages == False:
			sendto = True
			
			if self.channelname in cclientid._watch:
				raw(cclientid,"404",cclientid._nickname,self.channelname,"Cannot send to channel")
				cclientid.send(":" + ServerName + " NOTICE SERVER :*** You are watching this channel, you can't participate\r\n")
				sendto = False
				
			elif self.MODE_moderated:
				if msguser.lower() in self._voice or msguser.lower() in self._op or msguser.lower() in self._owner or msguser.lower() in opers: pass
				else:	
					sendto = False
					raw(cclientid,"404",cclientid._nickname,self.channelname,"Cannot send to channel")

			elif self.MODE_nocolour:
				if chr(3) in msg or chr(2) in msg or "\x1F" in msg:
					raw(cclientid,"404",cclientid._nickname,self.channelname,"Cannot send to channel")
					sendto = False

			if self.MODE_gagonban:
				if self.isBanned(cclientid):
					raw(cclientid,"404",cclientid._nickname,self.channelname,"Cannot send to channel whilst banned")
					sendto = False

			if self.MODE_profanity:
				foundprofanity=False
				for all in profanity:
					tmsg = re.compile(all.lower().replace(".",r"\.").replace("*","(.+|)"))
					if tmsg.match(msg.lower()):
						foundprofanity = True
						break

				if foundprofanity:
					sendto = False
					raw(cclientid,"404",cclientid._nickname,self.channelname,"Cannot send to channel (filter in use)")
					cclientid.send(":" + ServerName + " NOTICE SERVER :*** A filter is in use, your last message was blocked\r\n")

			if sendto:
				for each in copy(self._users):
					clientid = nicknames[each.lower()]
					if clientid != cclientid:
						if self.MODE_auditorium == False or isOp(clientid._nickname,self.channelname) or isOp(cclientid._nickname,self.channelname):
							if self.MODE_stripcolour:
								msg = re.sub("\x03[0-9]{1,2}(\,[0-9]{1,2}|)|\x1F|\x02","",msg)

							clientid.send(":%s!%s@%s %s %s :%s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,nop.upper(),self.channelname,msg))

			if "PRIVMSG" not in FloodingExempt:
				if cclientid._nickname.lower() not in self._op and cclientid._nickname.lower() not in self._owner and cclientid._nickname.lower() not in opers:
					time.sleep(0.8)
				else:
					time.sleep(0.18)

		else:
			raw(cclientid,"442",cclientid._nickname,self.channelname)


class ClientBaseClass:
	def __init__(self,_servername=ServerName):
		self._access = []
		self._nickamount = 0
		self._nicklock = 0
		self._nickflood = 0
		self._away = ""
		self._nosendnickserv = False
		self._channels = []
		self._invites = []
		self._IRCX = False
		self._MODE_ = "+"
		self._MODE_register = False
		self._MODE_registerchat = False
		self._MODE_filter = False
		self._MODE_gag = False
		self._MODE_invisible = False
		self._MODE_inviteblock = False
		self._MODE_nowhisper = False
		self._MODE_private = False
		self._nickname = ""
		self._username = ""
		self._fullname = ""
		self._hostmask = ""
		self._hostname = ""
		self._server = _servername
		self._signontime = 0
		self._idletime = 0
		self._watch = []
		self.details = ["",""]
		self._friendlyname = ""
		self.linkclass = None

	def send(self,data):
		try:
			print "Data to send: " + data
			self.linkclass.sendRawData(self._nickname,data)
		except:
			pass


class Recipient:
	def __init__(self,recipient,request,ID,parameters):
		self.recipient = recipient
		self.request = request
		self.ID = ID
		self.parameters = parameters

linkRequests = {}

def sendLinkRequestData(recipients,request,parameters):
	for eachlink in linkedServers:
		if eachlink.link._authenticated:
			try:
				eachlink.link._sock.sendall("\x00\x01\x00 0 %s %s\r\n" % (request,parameters))
			except:
				tuError = sys.exc_info()
				print tuError


#sendLinkRequestData(loller,"2","") # Request Channel list

class Link(threading.Thread):
	def __init__(self,LinkServer):
		self.link = LinkServer
		self.replydata = {}
		
		self._nicknames = {}
		self._opers = {}
		self._channels = {}

		self._handshake = [self.link._password]

		threading.Thread.__init__(self)

	def send(self,d):
		try:
			self.link._sock.sendall(d)
		except:
			pass

	def AuthenticationOK(self):
		linkedServers.append(self)
		sendLinkRequestData(None,"0","") # Request Users
		sendLinkRequestData(None,"1","") # Request Opers
		sendLinkRequestData(None,"2","") # Request Channels

		self.oNotice(":" + ServerName + " NOTICE LINK :*** Link response; (" + self.link._serverName + "@" + self.link._serverAddress + ") is now authenticated\r\n")
		self.linktime = time.time()
		self.oNotice(":" + ServerName + " NOTICE LINK :*** Synchronising server data; (" + self.link._serverName + "@" + self.link._serverAddress + ") please wait..\r\n")

	# communication commands to server
	# upon receiving the server shall check if the nickname is in the database on that specific server, if it is not in the database, it will tell the server to reply with:
	# 263 - Server link is currently having difficulties. Please wait a while and try again
	#
	# server will the update the database again by requesting the pickled nickname object of the user who it couldn't find




#	1   -   2   -   3
#
#		 4


	def sendUserNick(self,theirnick,theirnewnick):
		compileUser = (theirnick + " " + theirnewnick).encode("hex")
		socketsendData = "\x01\x00\x01 0 -2 %s\r\n" % (compileUser) # Users transport key here
		self.send(socketsendData)

	def sendUserMode(self,theirnick,theirmodes):
		compileUser = (theirnick + " " + theirmodes).encode("hex")
		socketsendData = "\x01\x00\x01 0 -5 %s\r\n" % (compileUser) # Users transport key here
		self.send(socketsendData)

	def sendMessage(self,theirnick,msgtype,msg):
		compileUser = (theirnick + " " + msgtype + " " + msg).encode("hex")
		socketsendData = "\x01\x00\x01 0 -6 %s\r\n" % (compileUser) # Users transport key here
		self.send(socketsendData)

	def sendHostIdentNameChange(self,theirnick,theirident,theirhost,theirname):
		newIAL = theirnick + " "
		if theirident == 0: newIAL += "0 "
		else: newIAL += theirident + " "

		if theirhost == 0: newIAL += "0 "
		else: newIAL += theirhost + " "

		if theirname == 0: newIAL + " 0"
		else: newIAL += theirname

		socketsendData = "\x01\x00\x01 0 -3 %s\r\n" % (newIAL.encode("hex")) # Users transport key here
		self.send(socketsendData)

	def sendUserOper(self,theirnick,pickledoper):
		compileUser = "%s %s" % (theirnick,pickledoper)
		socketsendData = "\x01\x00\x01 0 -4 %s\r\n" % (compileUser.encode("hex")) # Users transport key here
		self.send(socketsendData)

	def sendUserPrivmsg(self,theirnick,mynick,msgtype,theirmsg):
		compileUser = "%s %s %s %s" % (theirnick,mynick,msgtype,theirmsg)
		socketsendData = "\x01\x00\x01 0 -7 %s\r\n" % (compileUser.encode("hex")) # Users transport key here
		self.send(socketsendData)

	def sendUserAway(self,theirnick,reason):
		compileUser = "%s %s" % (theirnick,reason)
		socketsendData = "\x01\x00\x01 0 -8 %s\r\n" % (compileUser.encode("hex")) # Users transport key here
		self.send(socketsendData)

	def sendChannelData(self,channel,modes,properties,access):
		compileData = "%s\x00%s\x00%s\x00%s" % (channel,modes,properties,access)
		socketsendData = "\x01\x00\x01 0 -9 %s\r\n" % (compileData.encode("hex")) # Users transport key here
		self.send(socketsendData)

	def sendRawData(self,theirnick,data):
		pass
		#nid = nicknames[theirnick.lower()]
		#nid.send(data)

	def sendUserDisconnect(self,theircid):
		compileUser = theircid._nickname.encode("hex")
		socketsendData = "\x01\x00\x01 0 -1 %s\r\n" % (compileUser) # Users transport key here
		self.send(socketsendData)

	def sendUserConnect(self,theircid):
		compileUser = ""
		compileUser += theircid._nickname + "\x00" # seperator character
		compileUser += theircid._username + "\x00"
		compileUser += theircid._hostmask + "\x00"
		compileUser += theircid._fullname + "\x00"
		compileUser += theircid._friendlyname + "\x00"
		compileUser += theircid.details[0] + "\x00"
		compileUser += theircid._MODE_ + "\x00"
		compileUser += str(theircid._signontime) + "\x00"
		compileUser += str(theircid._idletime) + "\x00"
		compileUser += dumps(theircid._channels)
		compileUser += "\r\n"

		zcompileUser = compress(compileUser).encode("hex")

		socketsendData = "\x01\x00\x01 0 0 %s\r\n" % (zcompileUser) # Users transport key here

		self.send(socketsendData)

	# end of communication commands

	def LinkMain(self):
		self.link._sock.setblocking(0)
		while True:
			sdata = ""
			r,w,e = select([self.link._sock],[],[self.link._sock],1)
			if e or self.link._close == True:
				if e: self.link._linkfail = 4
				else: self.link._linkfail = 3

				return
			
			elif r:
				char = ""
				while True:
					try:
						char = self.link._sock.recv(1)
					except:
						self.link._close = True
						break

					if not char:
						self.link._close = True
						break

					if char == "\r" or char == "\n":
						break

					sdata += char
				
				try:
					print "recv:" + sdata + "#"
					p = sdata.split(" ")
					try:
						if p[0] + p[1] + p[3] == "\x00\x00\x00": #HANDSHAKE
							handShakeList = loads(decompress(p[2].decode("hex")))
							if handShakeList[0] == self.link._password:
								self.link._authenticated = True
								self.send("\x00 ISOK \x00\r\n")
								self.AuthenticationOK()
							else:
								self.link._linkfail = 5
								return


					except IndexError:
						pass
						
					if sdata.strip() == "\x00 ISOK \x00":
						self.link._authenticated = True
						self.AuthenticationOK()
					
					if self.link._authenticated == True:
						if p[0] == "\x00\x01\x00": #Recieving request

							try:
								linkparams = sdata.strip().split(" ",3)[3]
							except:
								linkparams = ""

						

							if p[2] == "0": # 0 will mean request all data from pyRCX server, request looks like
										# \x00\x01\x00 098f6bcd4621d373cade4e832627b4f6 0

										#reply will be
										# \x01\x00\x01 098f6bcd4621d373cade4e832627b4f6 0 <zlib code data here>

								compileListOfUsers = ""
								for eachnicks in nicknames:

									eachnick = nicknames[eachnicks.lower()]
									compileListOfUsers += eachnick._nickname + "\x00" # seperator character
									compileListOfUsers += eachnick._username + "\x00"
									compileListOfUsers += eachnick._hostmask + "\x00"
									compileListOfUsers += eachnick._fullname + "\x00"
									compileListOfUsers += eachnick._friendlyname + "\x00"
									compileListOfUsers += eachnick.details[0] + "\x00"
									compileListOfUsers += eachnick._MODE_ + "\x00"
									compileListOfUsers += str(eachnick._signontime) + "\x00"
									compileListOfUsers += str(eachnick._idletime) + "\x00"
									compileListOfUsers += dumps(eachnick._channels)
									compileListOfUsers += "\r\n"

								zcompileListOfUsers = compress(compileListOfUsers).encode("hex")

								#zcompileListOfUsers = compileListOfUsers.encode("hex")
								socketsendData = "\x01\x00\x01 %s 0 %s\r\n" % (p[1],zcompileListOfUsers) # Users transport key here

								self.send(socketsendData)
							
							if p[2] == "1":
								compileListOfOpers = compress(dumps(opers)).encode("hex")
								socketsendData = "\x01\x00\x01 %s 1 %s\r\n" % (p[1],compileListOfOpers) # Users transport key here
								self.send(socketsendData)

							if p[2] == "2":
								try:
									compileListOfChannels = ""
									for eachchans in channels:
										eachchan = channels[eachchans.lower()]
										if eachchan.localChannel == False: # & or %& channels will not be available to remote servers
											compileListOfChannels += eachchan.channelname + "\x00"
											compileListOfChannels += eachchan.GetChannelModes(0) + "\x00"
											compileListOfChannels += eachchan._topic + "\x00" + str(eachchan._topic_time) + "\x00" + eachchan._topic_nick + "\x00" + eachchan._founder + "\x00"
											compileListOfChannels += dumps(eachchan._prop).encode("hex") + "\x00"
											flist = {}
											for each in eachchan._users.keys():
												ioperLevel = 0
												if each in eachchan._op: ioperLevel = 5
												if each in eachchan._owner: ioperLevel = 7
												if each in eachchan._voice: ioperLevel += 1
												flist[each.lower()] = ioperLevel

											compileListOfChannels += dumps(flist).encode("hex")
											compileListOfChannels += "\r\n"

									zcompileListOfChannels = compress(compileListOfChannels).encode("hex")

									socketsendData = "\x01\x00\x01 %s 2 %s\r\n" % (p[1],zcompileListOfChannels) # Users transport key here

									self.send(socketsendData)
								except:
									tuError = sys.exc_info()
									print tuError
									print extract_tb(tuError[2])

						elif p[0] == "\x01\x00\x01": # Receiving data (IGNORE NOW 095455 ID)

							try:
								linkparams = sdata.strip().split(" ",3)[3]
							except:
								linkparams = ""


							#possibly add first linkparam here for nickname, check here then can add server request new data here

							if p[2] == "-9":
								chan,modes,properties,access = linkparams.decode("hex").split(" ",3)
#	def sendChannelData(self,channel,modes,properties,access):
#		compileData = "%s %s %s %s" % (channel,modes,properties,access)
#		socketsendData = "\x01\x00\x01 0 -9 %s\r\n" % (compileData.encode("hex")) # Users transport key here
#		self.send(socketsendData)



							if p[2] == "-8":
								theirnick,reason = linkparams.decode("hex").split(" ",1)
								if theirnick.lower() in self._nicknames:
									nid = self._nicknames[theirnick.lower()]
									nid._away = reason


							if p[2] == "-7":
								theirnick,mynick,msgtype,msg = linkparams.decode("hex").split(" ",3)
								if theirnick.lower() in self._nicknames and mynick.lower() in nicknames:
									nid = self._nicknames[theirnick.lower()]
									cid = nicknames[mynick.lower()]
									cid.send(":%s!%s@%s %s %s :%s\r\n" % (nid._nickname,nid._username,nid._hostmask,msgtype.upper(),cid._nickname,msg))

							if p[2] == "-6":
								theirnick,msgtype,msg = linkparams.decode("hex").split(" ",2)

								nid = getUserOBJ(theirnick)

								for eachuser in nicknames:
									cid = nicknames[eachuser]
									if nid == None: cid.send(":%s %s %s :%s\r\n" % (NetworkName,msgtype.upper(),cid._nickname,msg))
									else: cid.send(":%s!%s@%s %s %s :%s\r\n" % (nid._nickname,nid._username,nid._hostmask,msgtype.upper(),cid._nickname,msg))

							if p[2] == "-5":
								theirnick,theirmodes = linkparams.decode("hex").split(" ",1)
								if theirnick.lower() in self._nicknames:
									nid = self._nicknames[theirnick.lower()]
									m_setting = True
									if theirmodes[0] == "-":
										m_setting = False

									for eachmode in theirmodes.replace("+","").replace("-","").split(" ")[0]:
										if m_setting == True:
											if eachmode not in nid._MODE_: nid._MODE_ += eachmode
										else: nid._MODE_ = nid._MODE_.replace(eachmode,"")
										if eachmode == "x": nid._IRCX = True
										if eachmode == "f": nid._MODE_filter = m_setting
										if eachmode == "z": nid._MODE_gag = m_setting
										if eachmode == "i": nid._MODE_invisible = m_setting
										if eachmode == "I": nid._MODE_inviteblock = m_setting
										if eachmode == "p": nid._MODE_private = m_setting
										if eachmode == "P": nid._MODE_nowhisper = m_setting
										if eachmode == "X":
											if m_setting: nid._friendlyname = theirmodes.split(" ",1)[1]
											else: nid._friendlyname = ""

										if eachmode == "r":
											if m_setting:
												nid._MODE_register = True
												nid._username = nid._username.replace(PrefixChar,"")
											else:
												nid._MODE_register = False
												if nid._username[0] != PrefixChar: nid._username = PrefixChar + nid._username


										if m_setting == False:
											if eachmode == "o":
												if theirnick.lower() in self._opers:
													print "removing opers"
													del self._opers[theirnick.lower()]
													nid._MODE_ = nid._MODE_.replace("o","")
													nid._MODE_ = nid._MODE_.replace("a","")
													nid._MODE_ = nid._MODE_.replace("A","")
													nid._MODE_ = nid._MODE_.replace("O","")
													if nid._MODE_register == False:
														nid._username = PrefixChar + nid._username
										# oper modes

										if eachmode == "w":
											if theirnick.lower() in self._opers:
												opid = self._opers[theirnick.lower()]
												if m_setting == False: opid.watchserver = False
												else: opid.watchserver = True

										if eachmode == "s":
											if theirnick.lower() in self._opers:
												opid = self._opers[theirnick.lower()]
												if m_setting == False:
													opid.hidden = False
												else:
													opid.hidden = True

										if eachmode == "g":
											if theirnick.lower() in self._opers:
												opid = self._opers[theirnick.lower()]
												if m_setting == False:
													nid._username = opid.username
													opid.guide = False
												else:
													nid._username = "Guide"
													opid.guide = True


							if p[2] == "-4":
								theirnick,pickledoper = sdata.split(" ",3)[3].strip().decode("hex").split(" ")

								opid = loads(pickledoper)
								if theirnick.lower() in self._nicknames:
									nid = self._nicknames[theirnick.lower()]
									if theirnick.lower() not in opers:
										self._opers[theirnick.lower()] = opid
										nid._username = nid._username.replace(PrefixChar,"")
										if opid.operlevel == 4: nid._MODE_ += "aoAO"
										if opid.operlevel == 3: nid._MODE_ += "aoO"
										if opid.operlevel == 2: nid._MODE_ += "ao"
										if opid.operlevel == 1: nid._MODE_ += "o"

							if p[2] == "-3":
								theirnick,ident,host,name = sdata.split(" ",3)[3].strip().decode("hex").split(" ")
								nickid = getUserOBJ(theirnick)
								if nickid:
									if ident != "0" and ident != "": nickid._username = ident
									if host != "0" and host != "": nickid._hostmask = host
									if name != "0" and name != "": nickid._fullname = name

							if p[2] == "-2":
								oldnick,newnick = sdata.split(" ",3)[3].strip().decode("hex").split(" ")

								if oldnick.lower() in self._nicknames:
									self._nicknames[newnick.lower()] = self._nicknames[oldnick.lower()]
									del self._nicknames[oldnick.lower()]
									self._nicknames[newnick.lower()]._nickname = newnick
									if oldnick.lower() in self._opers:
										self._opers[newnick.lower()] = self._opers[oldnick.lower()]
										del self._opers[oldnick.lower()]
							
							if p[2] == "-1":
								linkparams = sdata.split(" ",3)[3].strip()
								uncompileData = linkparams.decode("hex").lower()
								if uncompileData in self._nicknames:
									del self._nicknames[uncompileData]

							if p[2] == "0":
								linkparams = sdata.split(" ",3)[3].strip()
								uncompileListOfUsers = decompress(linkparams.decode("hex"))
								for eachuser in uncompileListOfUsers.split("\r\n"):
									if eachuser != "":
										properties = eachuser.split("\x00")
										self._nicknames[properties[0].lower()] = ClientBaseClass(self.link._serverName)
										lu = self._nicknames[properties[0].lower()]
										lu.linkclass = self
										lu._nickname = properties[0]
										lu._fullname = properties[3]
										lu._friendlyname = properties[4]
										lu._username = properties[1]
										lu._hostmask = properties[2]
										lu.details = [properties[5],""]
										lu._MODE_ = properties[6]
										lu._signontime = int(properties[7])
										lu._idletime = int(properties[8])
										lu._channels = loads(properties[9])

										if "r" in lu._MODE_: lu._MODE_register = True
										if "f" in lu._MODE_: lu._MODE_filter = True
										if "z" in lu._MODE_: lu._MODE_gag = True
										if "i" in lu._MODE_: lu._MODE_invisible = True
										if "I" in lu._MODE_: lu._MODE_inviteblock = True
										if "P" in lu._MODE_: lu._MODE_nowhisper = True
										if "p" in lu._MODE_: lu._MODE_private = True

										if properties[0].lower() in nicknames:
											collision_nick = nicknames[properties[0].lower()]
											collision_linknick = self._nicknames[properties[0].lower()]
											if collision_nick._signontime < collision_linknick._signontime:
												print "collision on server with the nickname being linked with me"
											else:
												self.oNotice(":" + ServerName + " NOTICE LINK :*** Nickname collision on this server (%s!%s@%s$%s) [%s]\r\n" % (collision_nick._nickname,collision_nick._username,collision_nick._hostmask,ServerName,collision_nick.details[0]))
												collision_nick.send(":" + ServerName + " NOTICE LINK :*** You have been involved in a nickname collision and will be disconnected\r\n")
												collision_nick.quittype = 5
												collision_nick.die = True
												collision_nick.close()

							if p[2] == "1":
								linkparams = sdata.split(" ",3)[3].strip()
								self._opers = loads(decompress(linkparams.decode("hex")))

							if p[2] == "2":
								try:
									uncompileListOfChannels = decompress(linkparams.decode("hex"))
									for each in uncompileListOfChannels.split("\r\n"):
										if each != "":
											properties = each.split("\x00")
											self._channels[properties[0].lower()] = ChannelBaseClass()
											lc = self._channels[properties[0].lower()]
											print "The channel I am adding to my database is: " + properties[0].lower()
											lc.channelname = properties[0]
											setupModes(lc,properties[1])
											lc._topic = properties[2]
											lc._topic_time = int(properties[3])
											lc._topic_nick = properties[4]
											lc._founder = properties[5]
											lc._prop = loads(properties[6].decode("hex"))

											flist = loads(properties[7].decode("hex"))
											for eachuser in flist:
												ioperLevel = flist[eachuser]
												lc._users[eachuser] = None
												if ioperLevel == 5 or ioperLevel == 6:
													lc._op.append(eachuser)
													if ioperLevel == 6: lc._voice.append(eachuser)

												if ioperLevel == 7 or ioperLevel == 8:
													lc._owner.append(eachuser)
													if ioperLevel == 8: lc._voice.append(eachuser)

												if ioperLevel == 1: lc._voice.append(eachuser)
								except:
									tuError = sys.exc_info()
									print tuError
									print extract_tb(tuError[2])

								self.oNotice(":" + ServerName + " NOTICE LINK :*** Synchronisation of server data (" + self.link._serverName + "@" + self.link._serverAddress + ") complete.. (%.2fs)\r\n" % (time.time() - self.linktime))

				except IndexError:
					print "UH OH BUG"

		self.link._linkfail = 3

		# Reset link settings, connection faile

	def oNotice(self,notice):
		for op in opers:
			opid1 = opers[op]
			e = nicknames[op.lower()]
			if opid1.operlevel >= 3: # Send to admins or above
				e.send(notice)
	
	def run(self):
		self.link._use = True
		self.link._sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		if self.link._method == "1":
			self.link._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.link._sock.bind((ipaddress,int(self.link._port)))
			self.link._sock.listen(100)
			self.link._sock.settimeout(5.0)
			self.oNotice(":" + ServerName + " NOTICE LINK :*** Attempting to link to " + self.link._serverName + " [Listening...]\r\n")
			while True:
				try:
					(self.link._sock,addr) = self.link._sock.accept()
					break
				except:
					if self.link._use == False:
						break

			self.LinkMain()
		else:
			self.oNotice(":" + ServerName + " NOTICE LINK :*** Attempting to link to " + self.link._serverName + "@" + self.link._serverAddress + " [Connecting...]\r\n")
			try:
				self.link._sock.connect((self.link._serverAddress,self.link._port))
				self.send("\x00 \x00 " + compress(dumps(self._handshake)).encode("hex") + " \x00\r\n")

				try:
					self.LinkMain()
				except:
					self.link._linkfail = 3

			except:
				self.link._linkfail = 1



		for op in opers:
			opid1 = opers[op]
			e = nicknames[op.lower()]
			if opid1.operlevel >= 3: # Send to admins or above
				if self.link._linkfail == 1:
					e.send(":" + ServerName + " NOTICE LINK :*** Link failed; (" + self.link._serverName + "@" + self.link._serverAddress + ") refused the connection\r\n")
				if self.link._linkfail == 2:
					e.send(":" + ServerName + " NOTICE LINK :*** Link failed; the attempt to connect to (" + self.link._serverName + "@" + self.link._serverAddress + ") timed out\r\n")
				if self.link._linkfail == 3:
					e.send(":" + ServerName + " NOTICE LINK :*** Closing link; (" + self.link._serverName + "@" + self.link._serverAddress + ") reset the link\r\n")
				if self.link._linkfail == 4:
					e.send(":" + ServerName + " NOTICE LINK :*** Closing link; (" + self.link._serverName + "@" + self.link._serverAddress + ") was closed because of a socket error\r\n")
				if self.link._linkfail == 5:
					e.send(":" + ServerName + " NOTICE LINK :*** Closing link; (" + self.link._serverName + "@" + self.link._serverAddress + ") Authentication Failed\r\n")
				if self.link._linkfail == 6:
					e.send(":" + ServerName + " NOTICE LINK :*** Closing link; (" + self.link._serverName + "@" + self.link._serverAddress + ") is already configured to connect to one of the servers you're connected to, please resolve this conflict\r\n")

		try:
			self.link._sock.close()
		except:
			pass

		if self in linkedServers: linkedServers.remove(self)

		self.link._linkfail = 0
		self.link._use = False
		self.link._close = False
		self.link._authenticated = False
		self.link._use = False

# End of linking
		
class NickServ:
	def __init__(self,nick,passw,emaila,registrationtime,ip,vhost,level,showmail=False):
		self._nickname = nick
		self._groupnick = []
		self._password = passw
		self._email = emaila
		self._registrationtime = registrationtime
		self._details = ip
		self._vhost = vhost
		self._level = int(level)
		self._showemail = showmail

class Oper:

	operlevel = 0
	guide = False
	hidden = False
	watchserver = False
	watchbans = False
	watchnickserv = False
	usage = False

	def __init__ (self,username,password,flags,filename):
		self.username = username
		self.password = password
		self.flags = flags
		self.filename = filename

class filters:

	def __init__ (self,level,filterword,override):
		self.level = level
		self.filterword = filterword
		self.override = override

def stripx01(badstring):
	return badstring.replace("\x01","")


def GetUsers():
	myfile = open("database/users.dat","r")
	l = 1
	localusers = 0
	globalusers = 0
	for lineStr in myfile.readlines():
		if l == 1:
			localusers = lineStr
		elif l == 2:
			globalusers = lineStr
		
		lineStr = myfile.readline()
		l+=1

	myfile.close()

	myfile = open("database/Nickserv.dat","rb")
	global Nickserv
	rdata = myfile.read()
	try:
		if rdata != "":
			Nickserv = loads(decompress(rdata))
			#Nickserv = pickle.loads(rdata)
	except:
		raise IOError, "Could not load Nickserv database, possibly because it is corrupted"

	myfile.close()

	return (localusers.strip(),globalusers.strip())

readl = GetUsers()

MaxGlobal = readl[1]
MaxLocal = readl[0]


writeUsers_lock = False

def WriteUsers(localusers,globalusers,nicksv=True,chans=True,access=False):
	global writeUsers_lock
	if writeUsers_lock == False:
		writeUsers_lock = True
		try:
			myfile = open("database/users.dat","w")
			myfile.write("%s\r\n%s" % (localusers,globalusers))
			myfile.close()
			if nicksv:
				myfile = open("database/Nickserv.dat","wb")
				myfile.write(compress(dumps(Nickserv)))
				myfile.close()

			if chans:
				myfile = open("database/channels.dat","wb")
				schan = copy(channels)
				for each in schan:
					chanid = channels[each.lower()]
					if chanid.MODE_registered == True:
						myfile.write("C=%s\x01=%s\x01=%s\x01=%s\x01=%s\x01=%s\r\n" % (stripx01(chanid.channelname),stripx01(chanid.GetChannelModes(0,True)),stripx01(chanid._topic),chanid._founder,compress(dumps(chanid._prop)).encode("hex"),compress(dumps(chanid.ChannelAccess)).encode("hex")))

				myfile.close()

			if access:
				myfile = open("database/access.dat","wb")
				myfile.write(dumps(ServerAccess))
				myfile.close()
		except:
			pass
		
		writeUsers_lock = False



def rehash(par=1): # this information will be rehashed by any operator with level 4 privlidges (Administrator)
	myfile = open("pyRCX.conf", "r")
	try:
		global ServerAddress,ServerName,NetworkName,connectionsExempt,operlines,profanity,Ports,Disabled
		global Filter,FloodingExempt,MaxUsers,MaxUsersPerConnection,servers,NickfloodAmount,NickfloodWait
		global NickservParam,NTPServer,ipaddress,ServerAdmin1,ServerAdmin2,AdminPassword,ServerPassword
		global passmsg,HostMaskingParam,HostMasking,PrefixChar,MaxServerEntries,MaxChannelEntries,MaxUserEntries
		global DefaultModes,MaxChannels,MaxChannelsPerUser,ChanPrefix,defconMode,ChanLockDown,UserDefaultModes

		operlines = []
		profanity = []
		Ports = []
		Disabled = {}
		Filter = []
		FloodingExempt = []
		connectionsExempt = []
		servers = []
		
		line_num = 0

		for lineStr in myfile.readlines():
			
			line_num += 1
			if lineStr[0] == "S":
				s_line = lineStr.split(":")
			
				ServerAddress = s_line[1]
				ServerName = s_line[2]
				NetworkName =  s_line[3].split(";")[0]

			if lineStr[0] == "E":
				s_line = lineStr.split(":")
				connectionsExempt.append(s_line[1].split(";")[0])

			if lineStr[0] == "U":
				s_line = lineStr.split(":")
				MaxUsers = s_line[1]
				MaxUsersPerConnection = int(s_line[2])
				UserDefaultModes = s_line[3].split(";")[0]

			if lineStr[0] == "L":
				s_line = lineStr.split(":")
				servers.append(ServerInformation(s_line[1],s_line[2],s_line[3],s_line[4],s_line[5],s_line[6].split(";")[0]))

			if lineStr[0] == "N":
				s_line = lineStr.split(":")
				NickfloodAmount = int(s_line[1])
				NickfloodWait = int(s_line[2].split(";")[0])

			if lineStr[0] == "n":
				s_line = lineStr.split(":")
				NickservParam = s_line[1]
				defconMode = int(s_line[2].split(";")[0])
				if defconMode != 1 and defconMode != 2 and defconMode != 3: defconMode = 1

			if lineStr[0] == "T":
				s_line = lineStr.split(":")
				NTPServer = s_line[1].split(";")[0]

			if lineStr[0] == "I":
				s_line = lineStr.split(":")
				ipaddress = s_line[1].split(";")[0]

			if lineStr[0] == "A":
				s_line = lineStr.split(":")
				ServerAdmin1 = s_line[1]
				ServerAdmin2 = s_line[2]
				AdminPassword = s_line[3].split(";")[0]

			if lineStr[0] == "P":
				s_line = lineStr.split(":")
				ServerPassword = s_line[1]
				passmsg = s_line[2].split(";")[0]

			if lineStr[0] == "p":
				s_line = lineStr.split(":")		
				Ports.append(s_line[1].split(";")[0])

			if lineStr[0] == "f":
				s_line = lineStr.split(":")
				FloodingExempt.append(s_line[1].upper().split(";")[0])

			if lineStr[0] == "D":
				s_line = lineStr.split(":")
				if len(s_line) == 2: 
					value = 0
				else:
					value = s_line[2].split(";")[0]
				
				Disabled[s_line[1].upper()] = value

			if lineStr[0] == "H":
				s_line = lineStr.split(":")
				HostMasking = s_line[1]
				HostMaskingParam = s_line[2].split(";")[0]

			if lineStr[0] == "s":
				s_line = lineStr.split(":")
				PrefixChar = s_line[1].split(";")[0]

			if lineStr[0] == "X":
				s_line = lineStr.split(":")
				MaxServerEntries = s_line[1]
				MaxChannelEntries = s_line[2]
				MaxUserEntries = s_line[3].split(";")[0]
				

			if lineStr[0] == "C":
				s_line = lineStr.split(":")
				DefaultModes = s_line[1]
				MaxChannels = s_line[2]
				MaxChannelsPerUser = s_line[3]
				ChanLockDown = int(s_line[4].split(";")[0])

			if lineStr[0] == "c":
				s_line = lineStr.split(":")
				ChanPrefix = s_line[1].split(";")[0]

			if lineStr[0] == "O":
				s_line = lineStr.split(":")
				operlines.append(Oper(s_line[1],s_line[2],s_line[3],s_line[4].split(";")[0]))

			if lineStr[0] == "F":
				s_line = lineStr.split(":")
				if s_line[1] == "profanity":
					profanity.append(s_line[2])
				else:
					Filter.append(filters(s_line[1],s_line[2],s_line[3].split(";")[0]))
				
			lineStr = myfile.readline()

		myfile.close()

		if par == 1:
			SetupListeningSockets()
	except:
		tuError = sys.exc_info()
		_lastError.append([tuError,[time.strftime("%a %b %d %H:%M:%S %Y GMT",time.localtime()),"System rehash on line: " + str(line_num)],extract_tb(tuError[2])])
		print "Rehash error, line: " + str(line_num)
		

def unsigned(number):
	if number < 0: return 0
	else: return number

def raw(param1="",param2="",param3="",param4="",param5="",param6="",param7=""):
	if param3 == "":
		param3 = "*"

	if param2 == "001":
		param1.send(":" + ServerName + " 001 " + param3 + " :Welcome to the " + NetworkName + " chat service " + param3 + "\r\n")

	if param2 == "002":
		param1.send(":" + ServerName + " 002 " + param3 + " :Your host is " + param4 + ", running version 2.5.2\r\n")

	if param2 == "003":
		param1.send(":" + ServerName + " 003 " + param3 + " :This server was created on %s\r\n" % (time.strftime("%A %B %d %H:%M:%S %Y GMT",time.localtime())))

	if param2 == "004":
		param1.send(":" + ServerName + " 004 " + param3 + " " + param4 + " pyRCX 2.5.2 abAfghiInoOpPrwzX aAbcCdefGhikKlmMnNopPqQrRsStTuvwxXZ\r\n")

	if param2 == "005":
		if "IRCX" in Disabled:
			param1.send(":" + ServerName + " 005 " + param3 + " IRC PREFIX=(ov)@+ NETWORK=" + NetworkName + " are supported by this server\r\n")		
		else:
			param1.send(":" + ServerName + " 005 " + param3 + " IRCX PREFIX=(qov).@+ NETWORK=" + NetworkName + " are supported by this server\r\n")

	if param2 == "221":
		param1.send(":" + ServerName + " 221 " + param3 + " " + param4 + "\r\n")

	if param2 == "251":
		param1.send(":" + ServerName + " 251 " + param3 + " :There are " + str(unsigned(len(nicknames) - len(invisible))) + " users and " + str(len(invisible)) + " invisible on " + str(len(linkedServers)+1) + " server(s)\r\n")

	if param2 == "252":
		if unsigned(len(opers)) - len(opersecret) > 0:
			param1.send(":" + ServerName + " 252 " + param3 + " " + str(unsigned(len(opers)) - len(opersecret)) + " :operator(s) online\r\n") #display if operators available

	if param2 == "253":
		if len(unknownConnections) > 0:		
			param1.send(":" + ServerName + " 253 " + param3 + " " + str(len(unknownConnections)) + " :unknown connection(s)\r\n") #display if operators available

	if param2 == "254":
		totalchannels = len(channels)
		for eachserver in linkedServers: totalchannels += len(eachserver._channels)
		if totalchannels > 0:
			param1.send(":" + ServerName + " 254 " + param3 + " " + str(totalchannels) + " :channels formed\r\n")

	if param2 == "255":
		param1.send(":" + ServerName + " 255 " + param3 + " :I have " + str(len(nicknames)) + " client(s) and " + str(len(linkedServers)+1) + " server(s)\r\n") #display if operators available

	if param2 == "256":
		param1.send(":" + ServerName + " 256 " + param3 + " :" + NetworkName + " communications service\r\n") #display if operators available

	if param2 == "257":
		param1.send(":" + ServerName + " 257 " + param3 + " :pyRCX version 2.5.2, see /CREDITS\r\n") #display if operators available

	if param2 == "258":
		param1.send(":" + ServerName + " 258 " + param3 + " :" + ServerAdmin1 + "\r\n")

	if param2 == "259":
		param1.send(":" + ServerName + " 259 " + param3 + " :" + ServerAdmin2 + "\r\n")

	if param2 == "263":
		param1.send(":" + ServerName + " 263 " + param3 + " :Message too long, restrict your output\r\n")

	if param2 == "265":
		param1.send(":" + ServerName + " 265 " + param3 + " :Current Local Users: " + str(len(nicknames)) + "  Max: " + str(MaxLocal) + "\r\n") #display if operators available

	if param2 == "266":
		global MaxGlobal
		if MaxGlobal < getGlobalUserCount():
			MaxGlobal = getGlobalUserCount()

		param1.send(":" + ServerName + " 266 " + param3 + " :Current Global Users: " + str(getGlobalUserCount()) + "  Max: " + str(MaxGlobal) + "\r\n") #display if operators available

	if param2 == "301":
		param1.send(":" + ServerName + " 301 " + param3 + " " + param4._nickname + " " + param4._away + "\r\n")

	if param2 == "302":
		param1.send(":" + ServerName + " 302 " + param3 + " :" + param4._nickname + "=+" + param4._username + "@" + iif(param5,param4.details[0],param4._hostmask) + "\r\n")

	if param2 == "303":
		param1.send(":" + ServerName + " 303 " + param3 + " :" + param4 + "\r\n")

	if param2 == "305":
		param1.send(":" + ServerName + " 305 " + param3 + " :You are no longer marked as being away\r\n")

	if param2 == "306":
		param1.send(":" + ServerName + " 306 " + param3 + " :You have been marked as being away\r\n")

	if param2 == "307":
		param1.send(":" + ServerName + " 307 " + param3 + " " + param4._nickname + " :is registered to services\r\n")

	if param2 == "311":
		param1.send(":" + ServerName + " 311 " + param3 + " " + param4._nickname + " " + param4._username + " " + param4._hostmask + " * :" + param4._fullname + "\r\n")
		
	if param2 == "312":
		param1.send(":" + ServerName + " 312 " + param3 + " " + param4._nickname + " " + param4._server + " :" + NetworkName + "\r\n")

	if param2 == "313":
		opid = getOperOBJ(param4._nickname)
		if opid != None:
			if opid.hidden == False:
				if opid.guide == False:
					if "A" in opid.flags:
						param1.send(":" + ServerName + " 313 " + param3 + " " + param4._nickname + " :is the Network Administrator\r\n")

					elif "O" in opid.flags:
						param1.send(":" + ServerName + " 313 " + param3 + " " + param4._nickname + " :is a Server Administrator\r\n")

					elif "a" in opid.flags:
						param1.send(":" + ServerName + " 313 " + param3 + " " + param4._nickname + " :is a System Chat Manager\r\n")

					elif "o" in opid.flags:
						param1.send(":" + ServerName + " 313 " + param3 + " " + param4._nickname + " :is a System Operator\r\n")
				
				else:
					param1.send(":" + ServerName + " 313 " + param3 + " " + param4._nickname + " :is a Guide Operator\r\n")


	if param2 == "315":
		param1.send(":" + ServerName + " 315 " + param3 + " " + param4 + " :End of /WHO list.\r\n")
	
	if param2 == "316":
		param1.send(":" + ServerName + " 316 " + param3 + " " + param4 + " :is unable to participate because they are on the gag list\r\n")
	
	if param2 == "317":
		if param4._MODE_invisible != True or param3.lower() in opers:
			param1.send(":" + ServerName + " 317 " + param3 + " " + param4._nickname + " " + str(unsigned(int(GetEpochTime()) - param4._idletime)) + " " + str(param4._signontime) + " :seconds idle, signon time\r\n")

	if param2 == "318":		
		param1.send(":" + ServerName + " 318 " + param3 + " " + param4 + " :End of /WHOIS list\r\n")

	if param2 == "319":

		w_channels = ""
		cnick = param3.lower()
		cid = getUserOBJ(cnick)
		for c in param4._channels:

			if len(w_channels.split(" ")) == 10:
				param1.send(":" + ServerName + " 319 " + param3 + " " + param4._nickname + " :" + w_channels[1:] + "\r\n")
				w_channels = ""

			chanid = getChannelOBJ(c.lower())
			if chanid:
				if isSecret(chanid,"private","hidden") != True or cnick in chanid._users or getOperOBJ(cnick):
					if chanid.MODE_auditorium == False or isOp(cnick,chanid.channelname) or isOp(param4._nickname,chanid.channelname):

						#cid is me
						#param4 is them, param 5 is the one who should be hidden if watching channel 

						if chanid.channelname in param4._watch and cid != param4:
							pass
						
						elif param4._nickname.lower() in chanid._voice and param4._nickname.lower() not in chanid._op and param4._nickname.lower() not in chanid._owner:
							w_channels = w_channels + " +" + c

						elif param4._nickname.lower() in chanid._op:
							w_channels = w_channels + " @" + c

						elif param4._nickname.lower() in chanid._owner:
							if cid._IRCX:
								w_channels = w_channels + " ." + c
							else:
								w_channels = w_channels + " @" + c
						else:
							w_channels = w_channels + " " + c
						

		if w_channels != "":
			param1.send(":" + ServerName + " 319 " + param3 + " " + param4._nickname + " :" + w_channels[1:] + "\r\n")
	
	if param2 == "320":
		if param4._friendlyname:
			param1.send(":" + ServerName + " 320 " + param3 + " " + param4._nickname + " :" + param4._friendlyname + "\r\n")

	if param2 == "321":
		param1.send(":" + ServerName + " 321 " + param3 + " Channel :Users  Name\r\n")
	
	if param2 == "322":
		param1.send(":" + ServerName + " 322 " + param3 + " " + param4 + " " + param5 + " :" + param6 + "\r\n")

	if param2 == "323":
		param1.send(":" + ServerName + " 323 " + param3 + " :End of /LIST\r\n")
	
	if param2 == "324":
		param1.send(":" + ServerName + " 324 " + param3 + " " + param4 + " +" + param5 + "\r\n")

	if param2 == "331":
		param1.send(":" + ServerName + " 331 " + param3 + " " + param4 + " :No topic is set\r\n")

	if param2 == "332":
		param1.send(":" + ServerName + " 332 " + param3 + " " + param4 + " :" + param5 + "\r\n")


	if param2 == "333":
		if param5 == "": param5 = ServerName
		param1.send(":" + ServerName + " 333 " + param3 + " " + param4 + " " + param5 + " " + str(param6) + "\r\n")

	if param2 == "341":
		param1.send(":" + ServerName + " 341 " + param3 + " " + param4 + " " + param5 + "\r\n")

	if param2 == "352":
		param1.send(":" + ServerName + " 352 " + param3 + " " + param4 + "\r\n")

	if param2 == "353":
		param1.send(":" + ServerName + " 353 " + param3 + " = " + param4 + " :" + param5 + "\r\n")

	if param2 == "364":
		param1.send(":" + ServerName + " 364 " + param3 + " " + param4 + " " + NetworkName + " :0 " + param5 + "\r\n")

	if param2 == "365":
		param1.send(":" + ServerName + " 365 " + param3 + " * :End of /LINKS list.\r\n")

	if param2 == "366":
		param1.send(":" + ServerName + " 366 " + param3 + " " + param4 + " :End of /NAMES list.\r\n")


	if param2 == "367":
		param1.send(":" + ServerName + " 367 " + param3 + " " + param4 + " " + param5 + " " + param6 + " " + param7 + "\r\n")	


	if param2 == "368":
		param1.send(":" + ServerName + " 368 " + param3 + " " + param4 + " :End of Channel Ban List\r\n")

	if param2 == "371":
		param1.send(":" + ServerName + " 371 " + param3 + " :" + NetworkName + " communication service 2.5.2\r\n:" + ServerName + " 371 " + param3 + ServerLaunch + "\r\n")

	if param2 == "372":
			param1.send(":" + ServerName + " 372 " + param3 + " :- " + param4.replace("\r","").replace("\n","") + "\r\n")
			

	if param2 == "374":
		param1.send(":" + ServerName + " 374 " + param3 + " :End of /INFO list.\r\n")

	if param2 == "375": 
		param1.send(":" + ServerName + " 375 " + param3 + " :- " + ServerName + " Message of the Day\r\n")

	if param2 == "376":
		param1.send(":" + ServerName + " 376 " + param3 + " :End of /MOTD command.\r\n")

	if param2 == "378":
		if param3.lower() in opers:
			xopid = 0
			opid = opers[param3.lower()]
			if param4._nickname.lower() in opers:
				sopid = opers[param4._nickname.lower()]
				xopid = sopid.operlevel

			if opid.operlevel >= xopid:
				param1.send(":" + ServerName + " 378 " + param3 + " " + param4._nickname + " :is connecting from " + param4.details[0] + "\r\n")

	if param2 == "381":
		param1.send(":" + ServerName + " 381 " + param3 + " :" + param4 + "\r\n")

	if param2 == "391":
		param1.send(":" + ServerName + " 381 " + param3 + " :%s\r\n" % (time.strftime("%A %B %d %H:%M:%S %Y GMT",time.localtime())))


	if param2 == "401":
		param1.send(":" + ServerName + " 401 " + param3 + " " + param4 + " :No such nick/channel\r\n")

	if param2 == "403":
		param1.send(":" + ServerName + " 403 " + param3 + " " + param4 + " :No such channel\r\n")

	if param2 == "404":
		param1.send(":" + ServerName + " 404 " + param3 + " " + param4 + " :" + param5 + "\r\n")

	if param2 == "405":
		param1.send(":" + ServerName + " 405 " + param3 + " " + param4 + " :You have joined too many channels\r\n")

	if param2 == "409":
		param1.send(":" + ServerName + " 409 " + param3 + " :No origin specified\r\n")

	if param2 == "411":
		param1.send(":" + ServerName + " 411 " + param3 + " :No recipient given (" + param4 + ")\r\n")

	if param2 == "412":
		param1.send(":" + ServerName + " 412 " + param3 + " :No text to send (" + param4 + ")\r\n")

	if param2 == "416":
		param1.send(":" + ServerName + " 416 " + param3 + " " + param4 + " :Too many lines in the output, restrict your request\r\n")

	if param2 == "421":
		param1.send(":" + ServerName + " 421 " + param3 + " " + param4 + " :Unknown Command\r\n")

	if param2 == "422":
		param1.send(":" + ServerName + " 422 " + param3 + " :MOTD File is missing\r\n")

	if param2 == "432":
		if param3 == "" or param3 == "*":
			param3 = "*"
			param1._nosendnickserv = True
		
		param1.send(":" + ServerName + " 432 " + param3 + " " + param4 + " :Erroneous Nickname\r\n")

	if param2 == "433":
		if param3 == "" or param3 == "*":
			param3 = "*"
			param1._nosendnickserv = True
		
		param1.send(":" + ServerName + " 433 " + param3 + " " + param4 + " :Nickname is already in use\r\n")

	if param2 == "434":
		if param3 == "":
			param3 = "*"
		
		param1.send(":" + ServerName + " 434 " + param3 + " " + param4 + " :Erroneous Username\r\n")

	if param2 == "437":
		param1.send(":" + ServerName + " 437 " + param3 + " " + param4 + " :Cannot change nickname while banned on channel\r\n")

	if param2 == "438":
		param1.send(":" + ServerName + " 438 " + param3 + " :Nick change too fast. Please try again in a few minutes.\r\n")

	if param2 == "441":
		param1.send(":" + ServerName + " 441 " + param3 + " " + param4 + " :They aren't on that channel\r\n")

	if param2 == "442":
		param1.send(":" + ServerName + " 442 " + param3 + " " + param4 + " :You're not in that channel\r\n")

	if param2 == "443":
		param1.send(":" + ServerName + " 443 " + param3 + " " + param4 + " " + param5 +" :is already on channel\r\n")


	if param2 == "446":
		param1.send(":" + ServerName + " 446 " + param3 + " :" + param4 + " has been disabled\r\n")

	if param2 == "451":
		param1.send(":" + ServerName + " 451 " + param3 + " :You have not registered\r\n")

	if param2 == "461":
		if param3 == "":
			param3 = "*"
		param1.send(":" + ServerName + " 461 " + param3 + " " + param4 + " :Not enough parameters\r\n")
	
	if param2 == "462":
		if param3 == "":
			param3 = "*"
		param1.send(":" + ServerName + " 462 " + param3 + " " + ":You may not reregister\r\n")

	if param2 == "465":
		param1.send(":" + ServerName + " 465 " + param3 + " " + ":You are banned from this server\r\n")
		if param4 != "":
			param1.send("ERROR :Closing Link: " + param1.details[0] + " (" + param4.strip() + ")\r\n")

	if param2 == "468":
		param1.send(":" + ServerName + " 468 " + param3 + " " + param4 + " :Only servers can change that mode\r\n")	

	if param2 == "471":
		param1.send(":" + ServerName + " 471 " + param3 + " " + param4 + " :Cannot join channel (+l)\r\n")	

	if param2 == "472":
		param1.send(":" + ServerName + " 472 " + param3 + " " + param4 + " :is unknown mode char to me\r\n")	

	if param2 == "473":
		param1.send(":" + ServerName + " 473 " + param3 + " " + param4 + " :Cannot join channel (+i)\r\n")
		
	if param2 == "475":
		param1.send(":" + ServerName + " 475 " + param3 + " " + param4 + " :Cannot join channel (+k)\r\n")

	if param2 == "477":
		param1.send(":" + ServerName + " 477 " + param3 + " " + param4 + " :You need a registered nickname to join that channel\r\n")

	if param2 == "481":
		param1.send(":" + ServerName + " 481 " + param3 + " :" + param4 + "\r\n")

	if param2 == "482":
		param1.send(":" + ServerName + " 482 " + param3 + " " + param4 + " :You're not channel operator\r\n")

	if param2 == "483":
		param1.send(":" + ServerName + " 483 " + param3 + " " + param4 + " :Cannot join channel (" + param5 + ")\r\n")	

	if param2 == "485":
		param1.send(":" + ServerName + " 485 " + param3 + " " + param4 + " :You're not channel owner\r\n")	
		
	if param2 == "491":
		param1.send(":" + ServerName + " 491 " + param3 + " :" + param4 + "\r\n")	

	if param2 == "501":
		param1.send(":" + ServerName + " 501 " + param3 + " :Unknown MODE flag\r\n")

	if param2 == "502":
		param1.send(":" + ServerName + " 502 " + param3 + " :Can't change mode for other users\r\n")

	if param2 == "520":
		param1.send(":" + ServerName + " 520 " + param3 + " " + param4 + " :Authenticated clients only\r\n")

	if param2 == "613": # :TK2CHATWBC05 613 null :207.68.167.157 6667
		param1.send(":" + ServerName + " 613 " + param3 + " :" + param4 + " +" + param5 + "\r\n")

	if param2 == "702":
		param1.send(":" + ServerName + " 702 " + param3 + " " + param4 + " :Channel not found\r\n")

	if param2 == "705":
		param1.send(":" + ServerName + " 705 " + param3 + " " + param4 + " :Channel with same name exists\r\n")

	if param2 == "710":
		param1.send(":" + ServerName + " 710 " + param3 + " :The server Administrator has limited this server to " + MaxChannels + " channels\r\n")

	if param2 == "800":
		param1.send(":" + ServerName + " 800 " + param3 + " " + param4 + " 0 ANON 512 *\r\n")

	if param2 == "801":
		param1.send(":%s 801 %s %s\r\n" % (ServerName,param3,param4))

	if param2 == "802":
		param1.send(":%s 802 %s %s\r\n" % (ServerName,param3,param4))

	if param2 == "803":
		param1.send(":%s 803 %s %s :Start of access entries\r\n" % (ServerName,param3,param4))

	if param2 == "804":
		param1.send(":%s 804 %s %s\r\n" % (ServerName,param3,param4))

	if param2 == "805":
		param1.send(":%s 805 %s %s :End of access entries\r\n" % (ServerName,param3,param4))

	if param2 == "818":
		param1.send(":" + ServerName + " 818 " + param3 + " " + param4 + "\r\n")

	if param2 == "819":
		param1.send(":" + ServerName + " 819 " + param3 + " " + param4 + " :End of properties\r\n")

	if param2 == "820":
		param1.send(":%s 820 %s %s %s :Clear\r\n" % (ServerName,param3,param4,param5))

	#if param2 == "821":
	#	param1.send(":%s 821 :User unaway\r\n" % (param3._nickname))

	#if param2 == "822":
	#	param1.send(":%s 822 :%s\r\n" % (param3._nickname,param3._away))

	if param2 == "900":
		param1.send(":%s 900 %s %s :Bad command\r\n" % (ServerName,param3,param4))

	if param2 == "903":
		param1.send(":%s 903 %s %s :Bad level\r\n" % (ServerName,param3,param4))

	if param2 == "905":
		param1.send(":%s 905 %s %s :Bad property specified\r\n" % (ServerName,param3,param4))

	if param2 == "906":
		param1.send(":%s 906 %s %s :Bad value specified\r\n" % (ServerName,param3,param4))

	if param2 == "908":
		param1.send(":%s 908 %s :No permissions to perform command\r\n" % (ServerName,param3))

	if param2 == "909":
		param1.send(":%s 909 %s :No such nickname registered to services\r\n" % (ServerName,param3))

	if param2 == "912":
		param1.send(":%s 912 %s %s :Unsupported authentication package\r\n" % (ServerName,param3,param4))

	if param2 == "913":
		param1.send(":%s 913 %s %s :No access\r\n" % (ServerName,param3,param4))

	if param2 == "914":
		param1.send(":%s 914 %s %s :Duplicate access entry\r\n" % (ServerName,param3,param4))

	if param2 == "915":
		param1.send(":%s 915 %s %s :Unknown access entry\r\n" % (ServerName,param3,param4))

	if param2 == "916":
		param1.send(":%s 916 %s %s :Too many access entries\r\n" % (ServerName,param3,param4))

	if param2 == "922":
		param1.send(":%s 922 %s %s :Some entries not cleared due to security\r\n" % (ServerName,param3,param4))
	 
	if param2 == "923":
		param1.send(":%s 923 %s %s :Does not permit whispers\r\n" % (ServerName,param3,param4))

	if param2 == "924":
		param1.send(":%s 924 %s %s :No such object found\r\n" % (ServerName,param3,param4))

	if param2 == "925":
		param1.send(":%s 925 %s %s :Command not supported.\r\n" % (ServerName,param3,param4))

	if param2 == "927":
		param1.send(":%s 927 %s %s :Already in the channel.\r\n" % (ServerName,param3,param4))

	if param2 == "934":
		param1.send(":%s 934 %s %s :The channel you were on has been closed\r\n" % (ServerName,param3,param4))

	if param2 == "935":
		param1.send(":%s 935 %s %s :Too many wildcards\r\n" % (ServerName,param3,param4))

	if param2 == "997":
		param1.send(":%s 997 %s %s %s :Not supported by object\r\n" % (ServerName,param3,param4,param5))

	if param2 == "998":
		param1.send(":%s 998 %s %s %s :Cannot invite to channel\r\n" % (ServerName,param3,param4,param5))

	if param2 == "955":
		param1.send(":%s 955 %s :\x02Credits - pyRCX networking chat service 2.5.2\x02\r\n:%s 955 %s :Christopher James\r\n" % (ServerName,param3,ServerName,param3))
		param1.send(":%s 955 %s :-\r\n" % (ServerName,param3))
		param1.send(":%s 955 %s :\x02With thanks to:\x02\r\n:%s 955 %s :Darren Davies, Rob Lancaster, Kevin Deveau, Aaron Caffrey\r\n" % (ServerName,param3,ServerName,param3))

def myint(strdata):
	try:
		return int(strdata)
	except:
		return 0

def iif(state,stateiftrue,stateiffalse):
	if state == "" or state == False:
		return stateiffalse
	else:
		return stateiftrue

def isSecret(channel,extra="",extra2=""):
	if channel.MODE_secret: return True
	if channel.MODE_servicechan: return True
	if extra == "hidden" or extra2 == "hidden":
		if channel.MODE_hidden: return True

	if extra == "private" or extra2 == "private":
		if channel.MODE_private: return True

	return False

def isAdmin(nick):
	opid = getOperOBJ(nick.lower())
	if opid:
		if opid.operlevel >= 3: return opid.username
		else: return ""
	else:
		return ""

# this isOp will help

def isOp(nick,channel):	 # return true or false depending upon whether nick is oper
	chan = getChannelOBJ(channel.lower())
	if nick.lower() in chan._op or nick.lower() in chan._owner or getOperOBJ(nick.lower()):
		return True
	else:
		return False

def InChannel(s,them):
	for eachchan in them._channels:
		chanid = getChannelOBJ(eachchan.lower())
		if s._nickname.lower() in chanid._users:
			return True
	
	return False

def Whouser(_whouser,chan,selfn):
	if len(_whouser._channels) > 0:
		if chan != "": _whochan_ = channels[chan]
		else: _whochan_ = channels[_whouser._channels[0].lower()]

		if isSecret(_whochan_,"private","hidden") and selfn._nickname.lower() not in _whochan_._users and selfn._nickname.lower() not in opers:
			_whochan = "*"
		else:
			if chan != "": _whochan_ = channels[chan.lower()]
			_whochan = _whochan_.channelname
	else:
		_whochan = "*" # not in any channels

	if _whouser._nickname.lower() in opers:
		opid = opers[_whouser._nickname.lower()]
		if opid.hidden:
			_isoper = ""
		else:	
			if opid.guide:
				_isoper = "g"
			else:
				if opid.operlevel > 2:
					_isoper = "a"
				else:
					_isoper = "*"
	else:
		_isoper = ""

	if _whouser._away == "": _whoaway = "H"
	else: _whoaway = "G"

	_whomode = ""
	if _whochan != "*":
		if _whouser._nickname.lower() in _whochan_._op: _whomode = "@"
		if _whouser._nickname.lower() in _whochan_._owner: _whomode = "."
		if _whouser._nickname.lower() in _whochan_._voice: _whomode += "+"

	if _whochan != "*":
		if _whochan_.MODE_auditorium and isOp(selfn._nickname,_whochan_.channelname) == False and isOp(_whouser._nickname,_whochan_.channelname) == False  and _whouser != selfn:
			_whochan = "*"

		if _whouser._nickname.lower() in _whochan_._watch and _whouser != selfn and selfn._nickname.lower() not in opers:
			_whochan = "*"

	if chan != "":
		if _whochan_.MODE_auditorium and isOp(selfn._nickname,_whochan_.channelname) == False and isOp(_whouser._nickname,_whochan_.channelname) == False and _whouser != selfn:
			return ""
		if _whouser._nickname.lower() in _whochan_._watch and _whouser != selfn and selfn._nickname.lower() not in opers:
			return ""

	whostring = "%s %s %s %s %s %s%s%s :0 %s" % (_whochan,_whouser._username,_whouser._hostmask,ServerName,_whouser._nickname,_whoaway,_isoper,_whomode,_whouser._fullname)

	return whostring

def SendComChan (_channels,_self,_cid,_send,param):
	sendto = []
	sendto.extend((_self,_cid))
	
	nonIRCXsend = ":%s!%s@%s QUIT :Killed by %s (%s)\r\n" % (_cid._nickname,_cid._username,_cid._hostmask,_self._nickname,param) #non IRCX clients don't understand KILL

	if _self._IRCX: _self.send(_send)
	else: _self.send(nonIRCXsend)
		
	if _cid != _self:
		if _cid._IRCX: _cid.send(_send)
		else: _cid.send(nonIRCXsend)

	for each in copy(_channels):  #for each in selfs comchannels
		chan = channels[each.lower()]
		for n in chan._users:
			if n in nicknames:
				nick = nicknames[n.lower()]
				if nick not in sendto:
					if _cid._nickname.lower() not in chan._watch:
						if chan.MODE_auditorium == False or isOp(n,chan.channelname):
							sendto.append(nick)
							if nick._IRCX:
								nick.send(_send)
							else:
								nick.send(nonIRCXsend)

	del sendto

def compilemodestr(modes,chan=False):
	
	retval = ""
	il = 0
	while il < len(modes):
		if il == 32: return retval
		if chan:
			if modes[il] == "+" or modes[il] == "-" or modes[il] == "q" or modes[il] == "o" or modes[il] == "v" or modes[il] == "k" or modes[il] == "l" or modes[il] == "b":
				retval = retval + modes[il]

		elif modes[il] == "+" or modes[il] == "-":
			retval = retval + modes[il]
			il+=1

		if modes[il] not in retval: retval = retval + modes[il]

		il+=1

	return retval

def _filter(cid,text,param):
	for each in Filter:
		if cid._nickname.lower() in opers and each.filterword.lower() in text.lower():
			opid = opers[cid._nickname.lower()] 
			if str(opid.operlevel) >= str(each.override) and str(each.override) != str(0) and param == each.level: return True

		if each.filterword.lower() in text.lower() and param == each.level:return False

	return True

class Prop:
	def __init__(self,name,account):
		self.name = name
		self.profanity = []
		self.ownerkey = ""
		self.hostkey = ""
		self.memberkey = ""
		self.reset = 0
		self.client = ""
		self.subject = ""
		self.creation = str(int(GetEpochTime()))
		if "_nickname" in dir(account):
			self.account = True
			self.account_name = account._nickname
			self.account_user = account._username
			self.account_hostmask = account._hostmask
			self.account_address = account.details[0]
		else:
			self.account = False

		self.registered = ""
		self.onjoin = ""
		self.onpart = ""
		self.lag = 0
		self.language = ""

	def validate(self,property):
		p = re.compile("^[\x21-\xFF]{1,32}$")
		if p.match(property) == None: return False
		else: return True

	def _onmessage(self,chanid,_self,param3,sData,onmsg):
		if _self._nickname.lower() in chanid._users:
			if _self._nickname.lower() in chanid._op or _self._nickname.lower() in chanid._owner:
				if sData.__len__() > 256:
					raw(_self,"905",_self._nickname,chanid.channelname)
				else:
					stroj = sData
					if stroj[0] != ":":
						stroj = param3
					else:
						stroj = stroj[1:]

					chanid._prop.onjoin = stroj
					for each in chanid._users:
						cid = nicknames[each]
						cid.send(":%s!%s@%s PROP %s %s :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,onmsg,stroj))
			else:
				raw(_self,"482",_self._nickname,chanid.channelname)
		else:
			raw(_self,"442",_self._nickname,chanid.channelname)

	def _client(self,chanid,_self,sData):
		if _self._nickname.lower() in chanid._users:
			if _self._nickname.lower() in chanid._op or _self._nickname.lower() in chanid._owner:
				if sData.__len__() > 32:
					raw(_self,"905",_self._nickname,chanid.channelname)
				else:
					if sData == ":": sData = ""
					if sData != "" and sData[0] == ":":
						sData = sData[1:]

					chanid._prop.client = sData
					for each in chanid._users:
						cid = nicknames[each]
						cid.send(":%s!%s@%s PROP %s CLIENT :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,sData))
			else:
				raw(_self,"482",_self._nickname,chanid.channelname)
		else:
			raw(_self,"442",_self._nickname,chanid.channelname)

	def _topic(self,chanid,_self,sData,strd):
		if strd.__len__() > 512:
			raw(_self,"905",_self._nickname,chanid.channelname)
		else:
			dotopic = False

			if chanid.MODE_optopic == False or _self._nickname.lower() in chanid._op or _self._nickname.lower() in chanid._owner:
				dotopic = True
				
			if dotopic:
				if chanid.MODE_ownertopic and _self._nickname.lower() not in chanid._owner:
					raw(_self,"485",self._nickname,chanid.channelname)
				else:
					chanid._topic = sData
					if chanid._topic[0] == ":": chanid._topic = strd
					if chanid._topic == "":
						chanid._topic = ""
					else:
						chanid._topic_nick = _self._nickname
						chanid._topic_time = int(GetEpochTime())

					for each in chanid._users:
						cid = nicknames[each]
						cid.send(":%s!%s@%s TOPIC %s :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,chanid._topic))
			else:
				raw(_self,"482",_self._nickname,chanid.channelname)

	def _subject(self,chanid,_self,sData):
		if _self._nickname.lower() in chanid._users:
			if _self._nickname.lower() in chanid._op or _self._nickname.lower() in chanid._owner:
				if sData.__len__() > 32:
					raw(_self,"905",_self._nickname,chanid.channelname)
				else:
					if sData == ":": sData = ""
					if sData != "" and sData[0] == ":":
						sData = sData[1:]
					chanid._prop.subject = sData
					for each in chanid._users:
						cid = nicknames[each]
						cid.send(":%s!%s@%s PROP %s SUBJECT :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,sData))
			else:
				raw(_self,"482",_self._nickname,chanid.channelname)
		else:
			raw(_self,"442",_self._nickname,chanid.channelname)

	def _lag(self,chanid,_self,sData):
		if _self._nickname.lower() in chanid._users:
			if _self._nickname.lower() in chanid._op or _self._nickname.lower() in chanid._owner:
				if myint(sData) >= 5 or myint(sData) < -1 or myint(sData) == 0 and sData != "0":
					raw(_self,"905",_self._nickname,chanid.channelname)
				else:
					if myint(sData) == 0: sData = 0
					chanid._prop.lag = myint(sData)
					for each in chanid._users:
						cid = nicknames[each]
						cid.send(":%s!%s@%s PROP %s LAG :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,str(myint(sData))))
			else:
				raw(_self,"482",_self._nickname,chanid.channelname)
		else:
			raw(_self,"442",_self._nickname,chanid.channelname)

	def _language(self,chanid,_self,sData):
		if _self._nickname.lower() in chanid._users:
			if _self._nickname.lower() in chanid._op or _self._nickname.lower() in chanid._owner:
				if myint(sData) >= 65535 or myint(sData) < -1 or myint(sData) == 0 and sData != "0" and sData != ":":
					raw(_self,"905",_self._nickname,chanid.channelname)
				else:
					if sData == ":": 
						chanid._prop.language = ""
					else:
						chanid._prop.language = myint(sData)
					
					for each in chanid._users:
						cid = nicknames[each]
						cid.send(":%s!%s@%s PROP %s LANGUAGE :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,str(chanid._prop.language)))
			else:
				raw(_self,"482",_self._nickname,chanid.channelname)
		else:
			raw(_self,"442",_self._nickname,chanid.channelname)

	def _name(self,chanid,_self,sData):
		if _self._nickname.lower() in opers:
			opid = opers[_self._nickname.lower()]
			if opid.operlevel > 2:
				if sData.lower() == chanid.channelname.lower():
					for each in chanid._users:
						cid = nicknames[each]
						cid._channels.remove(chanid.channelname)
						cid._channels.append(sData)
						cid.send(":%s!%s@%s PROP %s NAME :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,sData))

					chanid.channelname = sData
				else:
					raw(_self,"908",_self._nickname)
			else:
				raw(_self,"908",_self._nickname)
		else:
			raw(_self,"908",_self._nickname)

	def _hostkey(self,chanid,_self,sData):
		if _self._nickname.lower() in chanid._users:
			if _self._nickname.lower() in chanid._owner:
				if chanid._prop.validate(sData) == False:
					raw(_self,"905",_self._nickname,chanid.channelname)
				else:
					if sData == ":": sData = ""
					if sData != "" and sData[0] == ":":
						sData = sData[1:]

					chanid._prop.hostkey = sData
					for each in chanid._users:
						cid = nicknames[each]
						if each.lower() in chanid._owner:
							cid.send(":%s!%s@%s PROP %s HOSTKEY :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,sData))
			else:
				raw(_self,"485",_self._nickname,chanid.channelname)
		else:
			raw(_self,"442",_self._nickname,chanid.channelname)	
		
	def _memberkey(self,chanid,_self,sData):
		if _self._nickname.lower() in chanid._op or _self._nickname.lower() in chanid._owner:
			if len(sData) <= 16:
				if sData == ":": sData = ""
				if sData != "" and sData[0] == ":":
					sData = sData[1:]

				chanid.MODE_key = str(sData)
				for each in chanid._users:
					cclientid = nicknames[each]
					if sData == "":
						cclientid.send(":%s!%s@%s MODE %s -k\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname))
					else:
						cclientid.send(":%s!%s@%s MODE %s +k %s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,sData))
			else:
				raw(self,"905",_self._nickname,chanid.channelname)
		else:
			raw(self,"482",_self._nickname,chanid.channelname)

	def _ownerkey(self,chanid,_self,sData):

		if _self._nickname.lower() in chanid._users:
			if _self._nickname.lower() in chanid._owner:
				if chanid._prop.validate(sData) == False:
					raw(_self,"905",_self._nickname,chanid.channelname)
				else:
					if sData == ":": sData = ""
					if sData != "" and sData[0] == ":":
						sData = sData[1:]
					
					chanid._prop.ownerkey = sData

					time.sleep(0.2)

					for each in chanid._users:
						cid = nicknames[each]
						if each.lower() in chanid._owner:
							cid.send(":%s!%s@%s PROP %s OWNERKEY :%s\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,sData))
					
					time.sleep(0.2)  # let people have fun!
					
			else:
				raw(_self,"485",_self._nickname,chanid.channelname)
		else:
			raw(_self,"442",_self._nickname,chanid.channelname)

	def _reset(self,chanid,_self,sData):

		if _self._nickname.lower() in opers or _self._nickname.lower() in chanid._owner:
			b = True
			r = myint(sData)
			if r == 0 and sData == "0":
				chanid._prop.reset = 0
			elif r <= 120 and r > -1:
				chanid._prop.reset = r
			else:
				raw(_self,"906",_self._nickname,sData)
				b = False
				
			if b:
				for each in chanid._users:
					cid = nicknames[each]
					cid.send(":%s!%s@%s PROP %s RESET :%d\r\n" % (_self._nickname,_self._username,_self._hostmask,chanid.channelname,chanid._prop.reset))
		else:
			raw(_self,"485",_self._nickname,chanid.channelname)


def CheckServerAccess(nickid=False):
	for each in list(ServerAccess):
		if int(GetEpochTime()) >= each._expires:
			if each._deleteafterexpire:
				ServerAccess.remove(each)
				WriteUsers(MaxLocal,MaxGlobal,False,False,True)

class AccessInformation:

	def __init__(self,object,level,mask,setby,expires,reason,oplevel):
		self._object = object # objects: *, #, $
		self._level = level.upper()
		self._reason = reason
		self._mask = mask
		self._setby = setby
		self._setat = int(GetEpochTime())
		if expires == 0: 
			self._expires = 0
			self._deleteafterexpire = False
		else:
			self._expires = int(GetEpochTime()) + (expires*60)
			self._deleteafterexpire = True
	
		self._oplevel = oplevel

class Access:
	def __init__(self):
		pass
		#self.records = [] # will contain the list of records added using the AccessInformation class

	def CheckChannelExpiry(self,chanid):	# channels only - this only needs to be done on events where access may apply, commands are JOIN and ACCESS
		for each in list(chanid.ChannelAccess):
			if int(GetEpochTime()) >= each._expires:
				if each._deleteafterexpire:
					chanid.ChannelAccess.remove(each)
					#_Access.records.remove(each)

	def CheckSelfExpiry(self,nickid):	# channels only - this only needs to be done on events where access may apply, commands are JOIN and ACCESS
		for each in list(nickid._access):
			if int(GetEpochTime()) >= each._expires:
				if each._deleteafterexpire:
					nickid._access.remove(each)
					#_Access.records.remove(each)
			

	def CFS(self,_mask):
		"Create format string"
		_mask = _mask.replace("\\","\\\\").replace("[","\[").replace("]","\]").replace("{","\{")
		_mask = _mask.replace("}","\}").replace(".","\.").replace("+","\+").replace("^","\^").replace("$","\$").replace("?",".").replace("*",".*")

		return _mask

	def MatchAccess(self,_mask,cid,NoMatchIP=False):
		if _mask[0] == "&":
			if "&" == _mask[0]:
				if cid._MODE_register:
					for groupnicks in Nickserv.values():
						if _mask[1:].lower() in groupnicks._groupnick or _mask[1:].lower() == groupnicks._nickname.lower():
							if cid._nickname.lower() in groupnicks._groupnick or cid._nickname.lower() == groupnicks._nickname.lower():
								return 1



		p = re.compile("^(.+)\!(.+)\@(.+)\$(.+)$")
		g = p.match(_mask)
		if g == None:
			return -1
		else:
			_nick = g.group(1)
			_nick_re = "^" + self.CFS(_nick.lower()) + "\!"

			_user = g.group(2)
			_user_re = self.CFS(_user.lower()) + "\@"

			_host = g.group(3)
			_host_re = self.CFS(_host.lower())

			_server = g.group(4)
			_server_re = "^" + self.CFS(_server.lower()) + "$"

			x = re.compile(_nick_re + _user_re + _host_re + "$")

			s = re.compile(_server_re)

			if s.match(cid._server):
				if x.match(cid._nickname.lower() + "!" + cid._username.lower() + "@" + cid._hostmask.lower()) != None: return 1
				if x.match(cid._nickname.lower() + "!" + cid._username.lower() + "@" + cid._hostname.lower()) != None  and NoMatchIP == False: return 1
				if x.match(cid._nickname.lower() + "!" + cid._username.lower() + "@" + cid.details[0]) != None and NoMatchIP == False: return 1
			else:
				return -1

	def getgroup(self,d,id):
		try:
			if d.group(id) == "": return "*"
			else: return d.group(id)
		except:
			return "*"

	def CreateMaskString(self,strin,server=False):
		if strin[0] == "&":
			if "!" in strin or "@" in strin: 
				return -1
			else:
				if strin.lower()[1:] in Nickserv or server == True:
					return strin
				else:
					for groupnicks in Nickserv.values():
						if strin.lower()[1:] in groupnicks._groupnick:
							return strin

					return -2

		if strin.count("!") > 1 or strin.count("$") > 1 or strin.count("@") > 1: return -1
		prefix, suffix,term,chars = "","",0,"[a-z0-9A-Z\_\@\$\!-\^\|\`\'\[\]\>\~\{\}\x7F-\xFF]{0,32}"

		if "!" in strin:
			if "@" in strin:
				if "$" in strin:
					term = 5
					smatch = "^(" + chars + ")\!(" + chars + ")\@(" + chars + ")\$(" + chars + ")$"
				else:
					term = 1
					smatch = "^(" + chars + ")\!(" + chars + ")\@(" + chars + ")$"
					suffix = "$*"
			else:
				if "$" in strin:
					term = 6
					smatch = "^(" + chars + ")\!(" + chars + ")\$(" + chars + ")$"
					suffix = "@*$"
				else:
					term = 2
					smatch = "^(" + chars + ")\!(" + chars + ")$"
					suffix = "@*$*"

		elif "@" in strin:
			prefix = "*!"
			if "$" in strin:
				term = 7
				smatch = "^(" + chars + ")\@(" + chars + ")\$(" + chars + ")$"
			else:
				term = 3
				smatch = "^(" + chars + ")\@(" + chars + ")$"
				suffix = "$*"

		elif "$" in strin:

			svr = re.compile("(" + chars + "|)\$(" + chars + "|)") # lol$lol
			m = svr.match(strin)
			if m == None: return -1
			if len(m.groups()) == 2:
				return "*!*@" + self.getgroup(m,1) + "$" + self.getgroup(m,2)
		else:
			term = 4
			smatch = "^(" + chars + ")$"
			suffix = "!*@*$*"

		p = re.compile(smatch)
		if p == None: return -1
		else:
			g = p.match(strin)
			if g == None: return -1
			try:
				if term == 0: return -1
				if term == 1: return (self.getgroup(g,1) + "!" + self.getgroup(g,2) + "@" + self.getgroup(g,3) + suffix).replace(":","")
				if term == 2: return (self.getgroup(g,1) + "!" + self.getgroup(g,2) + suffix).replace(":","")
				if term == 3: return (prefix + self.getgroup(g,1) + "@" + self.getgroup(g,2) + suffix).replace(":","")
				if term == 4: return (self.getgroup(g,1) + suffix).replace(":","")
				if term == 5: return (self.getgroup(g,1) + "!" + self.getgroup(g,2) + "@" + self.getgroup(g,3) + "$" + self.getgroup(g,4)).replace(":","")
				if term == 6: return (self.getgroup(g,1) + "!" + self.getgroup(g,2) + suffix + self.getgroup(g,3)).replace(":","")
				if term == 7: return (prefix + self.getgroup(g,1) + "@" + self.getgroup(g,2) + "$" + self.getgroup(g,3)).replace(":","")
				if term == 8: return (prefix + self.getgroup(g,1)).replace(":","")
			except:
				return "*!*@*$*"

	def ClearRecords(self,object,cid,level=""):
		_securitymsg = False
		if object == "*":
			opid = opers[cid._nickname.lower()]
			for each in list(ServerAccess):

				if level == "" or level.upper() == each._level.upper():
					if (opid.operlevel+2) < each._oplevel:
						_securitymsg = True
					else:
						ServerAccess.remove(each)
#						self.records.remove(each)
			
			if _securitymsg: raw(cid,"922",cid._nickname,"*")
			else:
				if level == "": level = "*"
				raw(cid,"820",cid._nickname,"*",level)

		elif object[0] == "#" or object[0] == "%" or object[0] == "&":
			chanid = channels[object.lower()]
			_operlevel = 0
			if cid._nickname.lower() in chanid._op: _operlevel = 1
			if cid._nickname.lower() in chanid._owner: _operlevel = 2
			if cid._nickname.lower() in opers:
				opid = opers[cid._nickname.lower()]
				_operlevel=opid.operlevel+2

			if _operlevel < 1:
				raw(cid,"913",cid._nickname,chanid.channelname)
				return -1

			for each in list(chanid.ChannelAccess):
				if level == "" or level.upper() == each._level.upper():
					if _operlevel < each._oplevel:
						_securitymsg = True
					else:
						chanid.ChannelAccess.remove(each)
#						self.records.remove(each)

			if _securitymsg: raw(cid,"922",cid._nickname,chanid.channelname)
			else:
				if level == "": level = "*"
				raw(cid,"820",cid._nickname,chanid.channelname,level)
		
		else:
			for each in list(cid._access):
				 if level == "" or level.upper() == each._level.upper():
					cid._access.remove(each)
#					self.records.remove(each)
			
			if level == "": level = "*"
			raw(cid,"820",cid._nickname,cid._nickname,level)
				

	def DelRecord(self,cid,object,level,mask):
		if object[0] == "*":
			opid = opers[cid._nickname.lower()]
			for each in list(ServerAccess):
				if each._mask.lower() == mask.lower() and each._level.lower() == level.lower():
					if (opid.operlevel+2) < each._oplevel: return -2
					ServerAccess.remove(each)
#					self.records.remove(each)
					return 1

		elif object[0] == "#" or object[0] == "%" or object[0] == "&":
			chanid = channels[object.lower()]
			_operlevel = 0
			if cid._nickname.lower() in chanid._op: _operlevel = 1
			if cid._nickname.lower() in chanid._owner: _operlevel = 2
			if cid._nickname.lower() in opers:
				opid = opers[cid._nickname.lower()]
				_operlevel=opid.operlevel+2

			if cid._nickname.lower() not in chanid._op and cid._nickname.lower() not in chanid._owner and cid._nickname.lower() not in opers:
				return -2 #not op - return no access
			if level.upper() == "OWNER" and cid._nickname.lower() not in chanid._owner and cid._nickname.lower() not in opers:
				return -2 #not owner - return no access

			CopyChannelAccess = list(chanid.ChannelAccess)
			for each in CopyChannelAccess:
				if each._mask.lower() == mask.lower() and each._level.lower() == level.lower():
					if _operlevel < each._oplevel: return -2
					chanid.ChannelAccess.remove(each)
#					self.records.remove(each)
					return 1
		
		else:
			CopyAccess = list(cid._access)
			for each in CopyAccess:
				if each._mask.lower() == mask.lower() and each._level.lower() == level.lower():
					cid._access.remove(each)
#					self.records.remove(each)
					return 1
			
		return -1

	def AddRecord(self,cid,object,level,mask,expires,tag):	   # .AddRecord(self,"*","DENY",_mask,0,tag)
		_list = None
		objid = None
		if object == "*":
			if cid == "": _operlevel = 6
			else:
				opid = opers[cid._nickname.lower()]
				_operlevel = opid.operlevel + 2

			_list = ServerAccess

		elif object[0] == "#" or object[0] == "%" or object[0] == "&":
			objid = channels[object.lower()]
			_operlevel = 0
			if cid == "": _operlevel = 5
			else:
				if cid._nickname.lower() in objid._op: _operlevel = 1
				if cid._nickname.lower() in objid._owner: _operlevel = 2
				if cid._nickname.lower() in opers:
					opid = opers[cid._nickname.lower()]
					_operlevel=opid.operlevel+2

				if cid._nickname.lower() not in objid._op and cid._nickname.lower() not in objid._owner and cid._nickname.lower() not in opers:
					return -2 #not op - return no access
				if level.upper() == "OWNER" and cid._nickname.lower() not in objid._owner and cid._nickname.lower() not in opers:
					return -2 #not owner - return no access

			_list = objid.ChannelAccess
		
		else:
			objid = nicknames[object.lower()]
			_list = objid._access
			_operlevel = 0

		for each in _list:
			if each._mask.lower() == mask.lower():
				return -1 # Duplicate access entry
		
		entry = None
		if cid == "": setby = ServerName
		else: setby = cid._username + "@" + cid._hostmask

		if object == "*":
			entry = AccessInformation("*",level,mask,setby,expires,tag,_operlevel)
			ServerAccess.append(entry)
		elif object[0] == "#" or object[0] == "%" or object[0] == "&":
			entry = AccessInformation(objid.channelname,level,mask,setby,expires,tag,_operlevel)
			objid.ChannelAccess.append(entry)
		else:
			entry = AccessInformation(objid._nickname,level,mask,setby,expires,tag,_operlevel)
			objid._access.append(entry)

		return 1

_Access = Access()	


class PropResetChannel(threading.Thread):
	def __init__(self,chanid):
		self.chanid = chanid
		threading.Thread.__init__(self)

	def run(self):
		try:
			exptime = int(GetEpochTime())+self.chanid._prop.reset

			while int(GetEpochTime()) <= exptime and self.chanid.channelname != "":
				if len(self.chanid._users) != 0:
					return

				time.sleep(0.1)

			if len(self.chanid._users) == 0:
				self.chanid._users = {}
				self.chanid._watch = []
				self.chanid._prop = None
				self.chanid._topic = ""
				self.chanid.ChannelAccess = []
				delGlobalChannel(self.chanid.channelname.lower())
				self.chanid.channelname = ""
		except:
			pass

def setupModes(self,creationmodes_full):
	creationmodes = creationmodes_full.split(" ")[0]
	if "Z" in creationmodes: self.MODE_noircx = True
	if "m" in creationmodes: self.MODE_moderated = True
	if "d" in creationmodes: self.MODE_createclone = True
	if "K" in creationmodes: self.MODE_noclones = True
	if "e" in creationmodes: self.MODE_cloneroom = True
	if "M" in creationmodes and self.MODE_noircx == False: self.MODE_ownersetmode = True
	if "G" in creationmodes: self.MODE_gagonban = True
	if "Q" in creationmodes and self.MODE_noircx == False: self.MODE_ownerkick = True
	if "A" in creationmodes: self.MODE_Adminonly = True
	if "f" in creationmodes: self.MODE_profanity = True
	if "N" in creationmodes: self.MODE_servicechan = True
	if "P" in creationmodes and self.MODE_noircx == False: self.MODE_ownersetprop = True
	if "X" in creationmodes: self.MODE_ownersetaccess = True
	if "R" in creationmodes: self.MODE_registeredonly = True
	if "w" in creationmodes: self.MODE_whisper = True
	if "s" in creationmodes: self.MODE_secret = True
	if "S" in creationmodes: self.MODE_nomodechanges = True
	if "h" in creationmodes and "s" not in creationmodes and "p" not in creationmodes: self.MODE_hidden = True
	if "T" in creationmodes and self.MODE_noircx == False: self.MODE_ownertopic = True
	if "t" in creationmodes and "T" not in creationmodes: self.MODE_optopic = True
	if "n" in creationmodes: self.MODE_externalmessages = True
	if "r" in creationmodes: self.MODE_registered = True
	if "x" in creationmodes: self.MODE_auditorium = True
	if "a" in creationmodes: self.MODE_authenticatedclients = True
	if "p" in creationmodes and "s" not in creationmodes and "h" not in creationmodes: self.MODE_private = True
	if "c" in creationmodes: self.MODE_nocolour = True
	if "C" in creationmodes and "c" not in creationmodes: self.MODE_stripcolour = True
	if "u" in creationmodes: self.MODE_knock = True
	if "l" in creationmodes or "k" in creationmodes:
		data_limit = str(myint(creationmodes_full.split(" ")[1]))
		data_key = creationmodes_full.split(" ")[1]
		if "l" in creationmodes and "k" in creationmodes:
			if creationmodes.find("l") > creationmodes.find("k"):
				data_key = creationmodes_full.split(" ")[1]
				data_limit = str(myint(creationmodes_full.split(" ")[2]))
			else:
				data_key = creationmodes_full.split(" ")[2]
				data_limit = str(myint(creationmodes_full.split(" ")[1]))

		if "l" in creationmodes:
			self.MODE_limit = True
			self.MODE_limitamount = data_limit

		if "k" in creationmodes: self.MODE_key = data_key


class Channel(ChannelBaseClass):

	def __validate(self,channelname,joinuser):
		chanprefix = "(" + "|".join(ChanPrefix.split(",")) + ")"
		p = re.compile("^" + chanprefix + "[\x21-\x2B\x2D-\xFF]{0,128}$")
		if p.match(channelname) == None or _filter(nicknames[joinuser.lower()],channelname,"chan") == False:
			return False
		else:
			return True

	def __init__ (self,channelname,joinuser,creationmodes=""):
		ChannelBaseClass.__init__(self)
		self.channelname = channelname
		if joinuser != "" and self.__validate(channelname,joinuser) == False:
			if joinuser != "":
				cclientid = nicknames[joinuser.lower()]
				cclientid.send(":%s 706 %s :Channel name is not valid\r\n" % (ServerName,cclientid._nickname))

			delGlobalChannel(self.channelname.lower())

			self.channelname = ""
		else:
			cclientid = None
			if creationmodes == "": creationmodes = DefaultModes
			
			if "Z" in creationmodes: self.MODE_noircx = True

			if joinuser != "":
				self._users[joinuser.lower()] = nicknames[joinuser.lower()]
				cclientid = nicknames[joinuser.lower()]

			if joinuser != "":
				if self.MODE_noircx == False: self._owner = [cclientid._nickname.lower()]
				else: self._op = [cclientid._nickname.lower()]

			if joinuser != "": self._prop = Prop(channelname,cclientid) # create instance of prop class
			else: self._prop = Prop(channelname,ServerName)

			if self.channelname[0] == "&": self.localChannel = True
			if len(self.channelname) >= 2:
				if self.channelname[0] + self.channelname[1] == "%&":
					self.localChannel = True

			setupModes(self,creationmodes)

			if joinuser != "":
				cclientid._channels.append(self.channelname)
				cclientid.send(":%s!%s@%s JOIN :%s\r\n" % (cclientid._nickname,cclientid._username,cclientid._hostmask,channelname))
				self.sendnames(cclientid._nickname,True)

Noop = False


def getGlobalUserCount():
	m = len(nicknames)
	for allservers in linkedServers:
		m += len(allservers._nicknames)

	return m

_lastError = []

def getGlobalChannels():
	for each in channels: yield channels[each]
	for server in linkedServers:
		for eachserver in server._channels:
			if server._channels[eachserver].localChannel == False:
				yield server._channels[eachserver]

def delGlobalChannel(chan_name):
	if chan_name.lower() in channels:
		del channels[chan_name.lower()]
	else:
		for server in linkedServers:
			if chan_name.lower() in server._channels:
				del server._channels[chan_name.lower()]


def getLinkUsers():
	for server in linkedServers:
		for eachserver in server._nicknames:
			yield eachserver

def getUserOBJ(nick):
	if nick.lower() in nicknames:
		return nicknames[nick.lower()]
	else:
		for each in linkedServers:
			if nick.lower() in each._nicknames:
				return each._nicknames[nick.lower()]

	return None

def getOperOBJ(nick):
	if nick.lower() in opers:
		return opers[nick.lower()]
	else:
		for each in linkedServers:
			if nick.lower() in each._opers:
				return each._opers[nick.lower()]

	return None

def getChannelOBJ(chan):
	schannels = copy(channels)
	if chan.lower() in schannels:
		return schannels[chan.lower()]
	else:
		for each in linkedServers:
			if chan.lower() in each._channels:
				return each._channels[chan.lower()]

	return None

def sendWatchOpers(details):
	for each in opers:
		opid = opers[each.lower()]
		if opid.watchserver:
			scid = nicknames[each.lower()]
			scid.send(":%s NOTICE %s :*** %s" % (ServerName,scid._nickname,details))


def sendNickservOpers(details):
	for each in opers:
		opid = opers[each.lower()]
		if opid.watchnickserv:
			scid = nicknames[each.lower()]
			scid.send(":%s NOTICE %s :*** %s" % (ServerName,scid._nickname,details))
		
def sendAdminOpers(details):
	for each in opers:
		opid = opers[each.lower()]
		if opid.operlevel >= 3:
			scid = nicknames[each.lower()]
			scid.send(details)
			

class ClientConnecting(threading.Thread,ClientBaseClass):

	def __init__ (self,client,details,port):

		ClientBaseClass.__init__(self)

		self._server = ServerName
		self.die = False
		self.client = client
		self.details = details
		self.flooding = 0
		self.lastcommand = int(GetEpochTime())
		self.pmflooding = 0
		self.pmlastcommand = int(GetEpochTime())
		self.port = port
		self.quittype = 0
		self._pingr = int(GetEpochTime()+30)
		self._rping = 1
		self._ptries = 0
		self._server = ServerName
		self._signontime = int(GetEpochTime())
		self._welcome = False
		self._flashclient = False
		self._idletime = int(GetEpochTime())

		threading.Thread.__init__(self)

	def close(self):
		try:
			self.client.shutdown(1)
		except:
			pass

	def send(self,data):
		try:
			if self._flashclient:
				self.client.sendall("\x00" + data.replace("<","&lt;"))
				self.client.sendall("\x00\r\n")
			else:
				r,w,e = select([],[self.client],[],1)
				if w:
					self.client.sendall(data)
		except:
			pass

	def _reportError(self,tuError):
		for each in _lastError:
			if str([each[2][0]]) == str(extract_tb(tuError[2])):
				self.send(":%s NOTICE LINK :*** Bug found and has already been reported, if this becomes a problem, please alert an administrator\r\n" % (ServerName))
				return



		_lastError.append([tuError,[time.strftime("%a %b %d %H:%M:%S %Y GMT",time.localtime()),self._nickname + "!" + self._username + "@" + self._hostmask +"/" + self.details[0]],extract_tb(tuError[2])])
		self.send(":%s NOTICE LINK :*** Bug found, please report the following:\r\n:%s NOTICE LINK :*** %s\r\n:%s NOTICE LINK :*** %s\r\n:%s NOTICE LINK *** End of bug report\r\n" % (ServerName,ServerName,str(tuError[0]),ServerName,str(tuError[1]),ServerName))

	def selfaccess(self,cclientid):
		_Access.CheckSelfExpiry(cclientid)
		if self._nickname.lower() in opers: return True # can't ignore opers!!!
		for each in cclientid._access:
			if each._level == "DENY":
				ret = _Access.MatchAccess(each._mask,self)
				if ret == 1:
					for findgrant in cclientid._access:
						if findgrant._level == "GRANT":
							gret = _Access.MatchAccess(findgrant._mask,self)
							if gret == 1:
								return True
					return False
		return True


	def _validate(self,text):
		if self._flashclient == True: flashallowed = "\>" # only guest clients can use the >, they can't however use it if they are registered, the > just means guest
		else: flashallowed = ""
		check = re.compile("^[a-z0-9A-Z\_\-\^\|\`\'\[\]" + flashallowed + "\\\~\{\}\x7F-\xFF]{1,32}$")
		if check.match(text) == None:
			return False
		else:
			return True

	def _validatefullname(self,text):
		check = re.compile("^[\x01-\xFF]{1,256}$")
		if check.match(text) == None:
			return False
		else:
			return True

	def _sendlusers(self):
		raw(self,"251",self._nickname)
		raw(self,"252",self._nickname)
		raw(self,"253",self._nickname)
		raw(self,"254",self._nickname)
		raw(self,"255",self._nickname)
		raw(self,"265",self._nickname)
		raw(self,"266",self._nickname)

	def _sendmotd(self,filename):
		
		try:
			myfile = open(filename, 'r')
		except:
			raw(self,"422",self._nickname)
			return False

		raw(self,"375",self._nickname)

		for lineStr in myfile.readlines():
			raw(self,"372",self._nickname,lineStr)
			lineStr = myfile.readline()
		
		raw(self,"376",self._nickname)

		myfile.close()

		return True

	def _sendwelcome(self):
		CheckServerAccess()
		grantfound = False
		for each in ServerAccess:
			if each._level == "DENY":
				ret = _Access.MatchAccess(each._mask,self)
				if ret == 1:
					for findgrant in ServerAccess:
						if findgrant._level == "GRANT":
							gret = _Access.MatchAccess(findgrant._mask,self)
							if gret == 1:
								grantfound = True
								break

					if grantfound: break

					raw(self,"465",self._nickname,each._reason[1:])
					self.die = True
					self.quittype = 9
					self.close()
					return 1
			

		sendWatchOpers("Notice -- User Connecting on port %s (%s!%s@%s) [%s] \r\n" % (self.port,self._nickname,self._username,self._hostmask,self.details[0]))
			
		unknownConnections.remove(self)

		global MaxLocal,MaxGlobal

		if len(nicknames) >= int(MaxGlobal):
			MaxLocal = len(nicknames)
			MaxGlobal = len(nicknames)

		
		for allservers in linkedServers:	# Send all the servers a message to tell them that a user is connecting
			allservers.sendUserConnect(self)
		

		raw(self,"001",self._nickname)
		raw(self,"002",self._nickname,ServerName)
		raw(self,"003",self._nickname)
		raw(self,"004",self._nickname,NetworkName)
		raw(self,"005",self._nickname)
		self._sendlusers()
		self._sendmotd("./motd.conf")

		if self._MODE_register:
			self._MODE_register = False
			self._MODE_.replace("r","")
			self.send(":%s!%s@%s MODE %s -r\r\n" % ("NickServ","NickServ",NetworkName,self._nickname))
			if self._username[0] != PrefixChar and self._nickname.lower() not in opers: self._username = PrefixChar + self._username

		is_groupednick = False

		for groupnicks in Nickserv.values():
			if self._nickname.lower() in groupnicks._groupnick:
				is_groupednick = True
				break

		if self._nickname.lower() in Nickserv and self._nickname.lower() in nicknames and self._nosendnickserv == False:
			self.send(":%s!%s@%s NOTICE %s :That nickname is owned by somebody else\r\n:%s!%s@%s NOTICE %s :If this is your nickname, you can identify with \x02/nickserv IDENTIFY \x1Fpassword\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,self._nickname,"NickServ","NickServ",NetworkName,self._nickname))
			is_groupednick = False

		if is_groupednick:
			self.send(":%s!%s@%s NOTICE %s :That nickname is owned by somebody else\r\n:%s!%s@%s NOTICE %s :If this is your nickname, you can identify with \x02/nickserv IDENTIFY \x1Fpassword\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,self._nickname,"NickServ","NickServ",NetworkName,self._nickname))

		# UserDefaultModes

		Mode_function(self,["MODE",self._nickname,UserDefaultModes])
			

	def _logoncheck(self):
		if self._username != "" and self._nickname != "" and self._welcome == False and self._nickname.lower() not in nicknames:
			if ServerPassword != "" and self._password == False:
				return False

			self._welcome = True
			nicknames[self._nickname.lower()] = self #update entry from dictionary

			if self._nickname.lower() in nickmute:
				del nickmute[self._nickname.lower()] # log on affirmed, now nicknames can take over

			return True
		else:
			return False

	def _isDisabled(self,command):
		if command in Disabled:
			
			val = myint(Disabled[command])
			operlevel = 0
			if self._nickname.lower() in opers: 
				opid = opers[self._nickname.lower()]
				operlevel = opid.operlevel

			if val == 0: return -1
			
			if operlevel == 0:
				raw(self,"481",self._nickname,"Permission Denied - You're not a System Operator")
				return -2

			if val == 1:
				if operlevel < 1:
					raw(self,"481",self._nickname,"Permission Denied - You're not a System Operator")
					return -2
				else:
					return 1
			
			if val == 2:
				if operlevel < 2:
					raw(self,"481",self._nickname,"Permission Denied - You're not a System Chat Manager")
					return -2
				else:
					return 1

			if val == 3:
				if operlevel < 3:
					raw(self,"481",self._nickname,"Permission Denied - You're not a Server Administrator")
					return -2
				else:
					return 1

			if val == 4:
				if operlevel < 3:
					raw(self,"481",self._nickname,"Permission Denied - You're not the Network Administrator")
					return -2
				else:
					return 1

		else:
			return 1
		
	def run(self):
		unknownConnections.append(self)
		connections.append(self)
		print "*** Connection accepted from '",self.details[0],"' users[",str(len(connections)),"/",MaxUsers,"]"

		if str(len(connections)-1) == str(MaxUsers):
			print "*** Connection closed '",self.details[0],"', server is full"
			self.send(":" + ServerName + " NOTICE AUTH :*** Sorry, this server is full, you can try reconnecting\r\n")
			self.send("ERROR :Closing Link: %s (Server is full)\r\n" % (self.details[0]))
			self.close()
			connections.remove(self)
			unknownConnections.remove(self)
		else:
			calcuseramount=-1
			for v in connections:
				if v.details[0] == self.details[0]:
					calcuseramount+=1

			userdetails = self.details[0] # store their ip in here
			
			if self.details[0] == "127.0.0.1":
				userdetails = ipaddress

			exemptFromConnectionKiller = False

			try:
				for each in globals()["connectionsExempt"]:
					if each == "":
						continue

					chk = re.compile("^" + each + "$")
					if chk.match(userdetails) != None:
						exemptFromConnectionKiller = True
						break
			except:
				print sys.exc_info()

			if str(MaxUsersPerConnection) == str(calcuseramount) and ipaddress != userdetails and exemptFromConnectionKiller == False:   #bots run from localhost, can't limit to 3 bots!!!
				unknownConnections.remove(self)
				print "*** Connection closed '",self.details[0],"', too many connections"
				
				self.send(":" + ServerName + " NOTICE AUTH :*** Sorry, your client is restricted to %d clones\r\n" % (MaxUsersPerConnection))
				
				self.send("ERROR :Closing Link: %s (Too many connections)\r\n" % (self.details[0]))

				self.quittype = 10
			else:
				if str(HostMasking) == "2":
					self.send(":" + ServerName + " NOTICE AUTH :*** Looking up your hostname...\r\n")
					
					try:
						self._hostname = socket.gethostbyaddr(self.details[0])[0]
						if socket.gethostbyname(self._hostname) == self.details[0]:
							self.send(":" + ServerName + " NOTICE AUTH :*** Found your hostname\r\n")
						else:
							someerror
					except:
						self._hostname = self.details[0]
						self.send(":" + ServerName + " NOTICE AUTH :*** Could not find your hostname, using your IP instead\r\n")

				if str(HostMasking) == "0": self._hostmask = self.details[0]
				elif str(HostMasking) == "1":
					self._hostmask = self.details[0].split(".")[0] + "." + self.details[0].split(".")[1] + ".XXX.XXX"
				
				elif str(HostMasking) == "2":
					if self._hostname == self.details[0]:			 # 127.0.0.1 - 127.0.A4EFF
						maskstart = self._hostname.split(".",2)[2]
						m = sha.new()
						m.update(self.details[0] + HostMaskingParam)
						shortmask = m.hexdigest().upper()[:5]

						self._hostmask = maskstart + "." + shortmask
					else:
						maskstart = self._hostname.split(".",1)[0]
						m = sha.new()
						m.update(self.details[0] + HostMaskingParam)
						shortmask = m.hexdigest().upper()[:5]
						try:
							self._hostmask = shortmask + "." + self._hostname.split(".",1)[1]
						except:
							self._hostmask = shortmask

				elif str(HostMasking) == "3":			
					self._hostmask = HostMaskingParam
				
				elif str(HostMasking) == "4":
					m = sha.new()
					m.update(self.details[0] + HostMaskingParam)
					self._hostmask = m.hexdigest().upper()[:16]
							
				elif str(HostMasking) == "5":
					self._hostmask = HostMaskingParam

				elif str(HostMasking) == "6":
					m = sha.new()
					m.update(self.details[0] + HostMaskingParam)
					shastring = m.hexdigest().upper()
					self._hostmask = self.details[0].split(".")[0] + "." + self.details[0].split(".")[1] + "." + shastring[0:3] + "." + shastring[3:6]
				else:
					self._hostmask = self.details[0] 
					
				if ServerPassword != "":
					self.send(":" + ServerName + " NOTICE AUTH :*** " + passmsg + "\r\n")

				self.send("PING :" + ServerName + "\r\n")
				self.client.setblocking(0)

				while True:
						# read line code
						c = ""
						strdata = ""
						closesock = False
						while True:
							if int(GetEpochTime()) >= self._pingr:
								if self._rping != 0 and self._welcome:
									self.send("PING :" + ServerName + "\r\n")
									self._rping-=1
									self._pingr = (int(GetEpochTime())+10)
								else:
									if self._welcome: self.send("ERROR :Closing Link: " + self.details[0] + " (Ping timeout)\r\n")
									else: self.send("ERROR :Closing Link: " + self.details[0] + " (Log on failed)\r\n")
									self.quittype = 3
									self.die = True

							r,w,e = select([self.client],[],[self.client],1)
							try:
								if r:
									c = self.client.recv(1)
									if not c:
										self.quittype = 1
										closesock = True
										break

									elif c == "\n" or c == "\r":
										c = ""
										# read a line
										break

									else:
										strdata+=c
									
							except socket.error, (value,message):
								if errno.ECONNABORTED == value or errno.ECONNRESET == value:
									self.quittype = 0
									closesock = True
									break

							if e:
								self.quittype = 0
								closesock = True
							
							if self.die:
								closesock = True
								break



						#end of readline code


						if closesock:
							print "breaking lol"
							break


						if len(strdata) >= 480:
							strdata = ""
							raw(self,"263",self._nickname)

						try:
							if strdata == "":
								param = [""]
							else:
								while strdata[0] == " ": strdata = strdata[1:]
								param = strdata.replace("\r","").replace("\n","").split(" ") #don't need both
								while "" in param: param.remove("")
								if param != []:
									param[0] = param[0].upper()
								else:
									param = [""]

						except:
							pass

						#print "data" + strdata

						#print "message starts"
						print param
						#print "message ends"
						_sleep = "%.4f" % (random()/9)
						_disabled = self._isDisabled(param[0])
						if param[0].upper() != "NOTICE" and param[0].upper() != "PRIVMSG" and param[0].upper() != "JOIN" and param[0] != "":

							if param[0] == "MODE" and len(param) == 2:
								pass
							else:

								if param[0] not in FloodingExempt:

									# if current time - time the last command was sent = 0, meaning data is being sent far too fast, add, 
									if int((int(GetEpochTime()) - self.lastcommand)*1000) <= 500:	# let's work in ms shall we?
										self.flooding+=1
									else:
										self.flooding = 0
									
									self.lastcommand = int(GetEpochTime())

									if self.flooding == 20: # 15 commands per 1000 miliseconds, anymore than that will kill the user
										print "Input flooding!!"
										self.quittype = 4
										self.send("ERROR :Closing Link: " + self.details[0] + " (Input flooding)\r\n")
										self.die = True
										self.close()
										

							#end flooding protection
						
							#time.sleep(0.04)

						try:

							if param[0] == "": pass

							elif _disabled < 1:
								if _disabled == -1:
									raw(self,"446",self._nickname,param[0])

							elif param[0] == "AUTH":
								try:
									if param[1] == "FLASH":
										self._flashclient = True
									else:
										raw(self,"912",self._nickname,param[1])
								except:
									raw(self,"461",self._nickname,param[0])

							elif param[0] == "NICK":
								Nick_function(self,param)


							elif param[0] == "PASS": # PASS password
								if ServerPassword != "":
									if self._password: raw(self,"462",self._nickname)
									else:
										if param[1] == ServerPassword:
											self._password = True
											self.send(":" + ServerName + " NOTICE AUTH :*** Password accepted\r\n")
											if self._logoncheck(): self._sendwelcome()
										else:
											self.send(":" + ServerName + " NOTICE AUTH :*** Invalid password\r\n")
											self._ptries +=1
											if self._ptries == 3:
												if self._nickname != "": self.send(":" + ServerName + " KILL " + self._nickname + " :Too many invalid passwords\r\n")
												else: self.send(":" + ServerName + " NOTICE AUTH :*** Too many invalid passwords\r\n")
												break
								else:
									self.send(":" + ServerName + " NOTICE AUTH :*** PASS has been disabled\r\n")

							elif param[0] == "PONG":
								if self._rping < 2 and self._welcome:
									self._rping += 1
								
							elif param[0] == "USER": # USER ident mode[8] unused :fullname	
								if self._username != "":
									raw(self,"462",self._nickname)
								else:
									ustr = self._validate(param[1].replace(".",""))
									if ustr == False:
										param[1] = self._nickname
									
									if self._validate(param[1].replace(".","")) and param[4]:

										if len(strdata.split(":",1)) == 2: _fn = strdata.split(":",1)[1][:256]
										else: _fn = ""
										if self._validatefullname(_fn.replace(" ","")) or _fn == "":
											self._fullname = _fn
											if str(HostMasking) != "5":
												self._username = PrefixChar + param[1].replace(PrefixChar,"")

											elif str(HostMasking) == "5":
												m = sha.new()
												m.update(self.details[0] + HostMaskingParam)
												self._username = PrefixChar + m.hexdigest().upper()[:16]

											if self._logoncheck():
												self._sendwelcome()
										else:
											raw(self,"434",self._nickname,param[1].replace(':',''))
									else:
										raw(self,"434",self._nickname,param[1].replace(':',''))

							elif param[0] == "QUIT":	#QUIT :die reasons
								try:
									msg = param[1]
									if msg[0] == ":": msg = strdata.split(" ",1)[1][1:]
								except:
									msg = ":"

								if msg == ":":
									self.quittype = 2
									self.quitmsg = ""
								else:
									self.quittype = 2
									self.quitmsg = msg

								try:	       # sometimes the client exits too fast
									self.send("ERROR :Closing Link: " + self.details[0] + " (Client Quit)\r\n")
									break
									#self.client = None
								except:
									pass

							elif param[0] == "PING":
								try:
									ret = param[1]
									if ret[0] == ":": ret = strdata.split(" ",1)[1][1:]
									self.send(":%s PONG %s :%s\r\n" % (ServerName,ServerName,ret))
								except:
									raw(self,"409",self._nickname)

							elif param[0] == "IRCX":
								if self._IRCX == False:
									for allservers in linkedServers: allservers.sendUserMode(self._nickname,"\x01")

								raw(self,"800",self._nickname,"1")
								self._IRCX = True

							elif param[0] == "ISIRCX":
								raw(self,"800",self._nickname,"0")

							else:
								if self._welcome:
									self._pingr = (int(GetEpochTime())+100)
									
									opid,chanid,copid = None,None,None
									try:
										chanid = getChannelOBJ(param[1].lower())
										cid = getUserOBJ(param[1].lower())
										if cid: copid = getOperOBJ(cid._nickname.lower())

									except IndexError: pass

									if self._nickname.lower() in opers: opid = opers[self._nickname.lower()]

									if param[0] == "NOOPER": # Any admin can disable the oper command 
										global Noop,temp_noopers

										if len(param) == 2:
											if param[1] == AdminPassword:
												Noop = False
												self.send(":" + ServerName + " NOTICE SERVER :*** Oper is now enabled\r\n")
										else:
											if opid:
												if opid.operlevel >= 3:
													if Noop == False:
														Noop = True
														odict = dict(opers)
														for each in nicknames:
															cid = nicknames[each]
															if cid._nickname.lower() in odict:
																opid2 = odict[cid._nickname.lower()]
																if opid2.operlevel < opid.operlevel:
																	temp_noopers.append(cid)
																	cid.send(":%s MODE %s -%s\r\n" % (ServerName,cid._nickname,opid2.flags))
																	cid.send(":" + ServerName + " NOTICE SERVER :*** Your o-line has been disabled temporarily\r\n")
																	del opers[each]
														
														self.send(":" + ServerName + " NOTICE SERVER :*** All opers have been disabled\r\n")
														
													else:
														Noop = False
														self.send(":" + ServerName + " NOTICE SERVER :*** Oper is now enabled\r\n")
														for each in temp_noopers:
															each.send(":" + ServerName + " NOTICE SERVER :*** Your o-line has been enabled, please re-oper\r\n")
														
														temp_noopers = []
														
												else:
													raw(self,"481",self._nickname,"Permission Denied - You're not the Network Administrator")
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not a System Operator")

									elif param[0] == "WATCH":
										if opid:
											if chanid:
												self._watch.append(chanid.channelname)
												chanid.join(self._nickname)
												self.send(":" + ServerName + " NOTICE WATCH :*** You are now watching " + chanid.channelname + ", to join the conversation, part and re-join\r\n")
											else:
												raw(self,"403",self._nickname,param[1])
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "KILL":
										msg = param[2]
										if msg[0] == ":": msg = strdata.split(" ",2)[2][1:]

										if opid:
											if cid:
												if copid:
													copid = opers[cid._nickname.lower()]
													if copid.operlevel > opid.operlevel and param[1].lower() != self._nickname.lower(): # I don't want opers wars now
														raw(self,"481",self._nickname,"Permission Denied - You do not have the correct privileges to kill this oper")
													else:
														cid.quittype = -1
														cid.quitmsg = " by " + self._nickname
														cid.die = True
														SendComChan(cid._channels,self,cid,":%s!%s@%s KILL %s :%s\r\n" % (self._nickname,self._username,self._hostmask,cid._nickname,msg),msg)
												else:
													cid.quittype = -1
													cid.die = True
													cid.quitmsg = " by " + self._nickname
													SendComChan(cid._channels,self,cid,":%s!%s@%s KILL %s :%s\r\n" % (self._nickname,self._username,self._hostmask,cid._nickname,msg),msg)

											elif chanid:
												if opid.operlevel > 1:
													if chanid.MODE_registered or chanid.MODE_servicechan:
														raw(self,"481",self._nickname,"Permission Denied - You cannot kill a registered channel")
													else:
														if self._IRCX: self.send(":%s!%s@%s KILL %s :%s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,msg))
														else: self.send(":" + ServerName + " NOTICE SERVER :*** Killed channel " + chanid.channelname + " (" + strdata.split(" ",2)[2] + ")\r\n")

														for each in chanid._users:
															cid = nicknames[each]
															cid._channels.remove(chanid.channelname)
															raw(cid,"934",cid._nickname,chanid.channelname)

														chanid._users = {}
														chanid.resetchannel(True)
												else:	
													raw(self,"481",self._nickname,"Permission Denied - You do not have the correct privileges to kill a channel")
													
											else:
												raw(self,"401",self._nickname,param[0])
											
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "DIE":
										if opid:
											if opid.operlevel == 4:
												if param[1] == AdminPassword:
													for each in nicknames:
														e = nicknames[each]
														e.send(":" + ServerName + " NOTICE SERVER :*** This Server has been closed by the Network Administrator\r\n")
														e.client.shutdown(1)

													os._exit(1)
												else:	
													raw(self,"908",self._nickname)
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not the Network Administrator")

									elif param[0] == "STATS":
										if param[1] == "G":
											self.send(":" + ServerName + " NOTICE STATS :*** Viewing Online guides '" + param[1][0] + "' \r\n")
											foundguide = False
											for each in nicknames:
												nickid = nicknames[each.lower()]
												if nickid._nickname.lower() in opers:
													opid = opers[nickid._nickname.lower()]
													if opid.guide:
														foundguide = True
														self.send(":" + ServerName + " NOTICE STATS :*** " + nickid._nickname + " is available for help\r\n")

											if foundguide == False:
												self.send(":" + ServerName + " NOTICE STATS :*** Sorry, there are no guides available\r\n")

										elif opid:
											if opid.operlevel < 3:
												raw(self,"481",self._nickname,"Permission Denied - You're not a Server Administrator")
											else:
												if param[1] == "U":
													self.send(":" + ServerName + " NOTICE STATS :*** Viewing User statistics '" + param[1][0] + "' \r\n")
													self.send(":" + ServerName + " 212 " + self._nickname + " :Max Users: " + MaxUsers + "\r\n")
													self.send(":" + ServerName + " 212 " + self._nickname + " :Max Users per connection: " + str(MaxUsersPerConnection) + "\r\n")

												elif param[1] == "E":
													self.send(":" + ServerName + " NOTICE STATS :*** Viewing Error statistics '" + param[1][0] + "' \r\n")
													for every in _lastError:
														self.send(":" + ServerName + " NOTICE STATS :*** Error found on " + every[1][0] + " by " + every[1][1] + "\r\n")
														self.send(":" + ServerName + " 212 " + self._nickname + " :%s\r\n" % (str(every[2][0])))
														self.send(":" + ServerName + " 212 " + self._nickname + " :%s\r\n" % (str(every[0][0])))
														self.send(":" + ServerName + " 212 " + self._nickname + " :%s\r\n" % (str(every[0][1])))

													self.send(":" + ServerName + " NOTICE STATS :*** Finished listing\r\n")

												elif param[1] == "O":
													self.send(":" + ServerName + " NOTICE STATS :*** Viewing Operator statistics '" + param[1][0] + "' \r\n")
													for oline in operlines:
														if "A" in oline.flags: self.send(":" + ServerName + " 212 " + self._nickname + " :[A] - " + oline.username + " - " + oline.flags  + " (Network Administrator)\r\n")
														elif "O" in oline.flags: self.send(":" + ServerName + " 212 " + self._nickname + " :[O] - " + oline.username + " - " + oline.flags  + " (Server Administrator)\r\n")
														elif "a" in oline.flags: self.send(":" + ServerName + " 212 " + self._nickname + " :[a] - " + oline.username + " - " + oline.flags  + " (System Chat Manager)\r\n")
														elif "o" in oline.flags: self.send(":" + ServerName + " 212 " + self._nickname + " :[o] - " + oline.username + " - " + oline.flags  + " (System Operator)\r\n")

												elif param[1] == "P":
													self.send(":" + ServerName + " NOTICE STATS :*** Viewing Port statistics '" + param[1][0] + "' \r\n")
													for each in currentports.keys():
														self.send(":" + ServerName + " 212 " + self._nickname + " :Running server on: " + each + "\r\n")

												elif param[1] == "F":
													self.send(":" + ServerName + " NOTICE STATS :*** Viewing Filter statistics '" + param[1][0] + "' \r\n")
													for f in Filter:
														if f.level == "chan": self.send(":" + ServerName + " 212 " + self._nickname + " :Channel filter - '" + f.filterword + "' - Level " + f.override + " overrides\r\n")
														elif f.level == "nick": self.send(":" + ServerName + " 212 " + self._nickname + " :Nickname filter - '" + f.filterword + "' - Level " + f.override + " overrides\r\n")
														elif f.level == "profanity": self.send(":" + ServerName + " 212 " + self._nickname + " :Profanity filter - '" + f.filterword + "' - Level " + f.override + " overrides\r\n")

												elif param[1] == "D":
													self.send(":" + ServerName + " NOTICE STATS :*** Viewing Disabled statistics '" + param[1][0] + "' \r\n")
													for each in Disabled:
														self.send(":" + ServerName + " 212 " + self._nickname + " :" + each + "\r\n")

												elif param[1] == "C":
													self.send(":" + ServerName + " NOTICE STATS :*** Viewing Channel statistics '" + param[1][0] + "' \r\n")
													self.send(":" + ServerName + " 212 " + self._nickname + " :Creation Modes: " + DefaultModes + "\r\n")
													self.send(":" + ServerName + " 212 " + self._nickname + " :Max Channels: " + MaxChannels + "\r\n")
													self.send(":" + ServerName + " 212 " + self._nickname + " :Max Channels per User: " + MaxChannelsPerUser + "\r\n")

												else:
													self.send(":" + ServerName + " NOTICE STATS :*** No statistics available for '" + param[1][0] + "' \r\n")

										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "REHASH":
										if opid:
											if opid.operlevel >= 4:
												sendAdminOpers(":" + ServerName + " NOTICE CONFIG :*** " + self._nickname + " is rehashing the server config file\r\n")
												rehash()
												sendAdminOpers(":" + ServerName + " NOTICE CONFIG :*** The server has been rehashed\r\n")
									
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not the Network Administrator")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System Operator")

									elif param[0] == "CONNECT":
										try:
											if opid:
												if opid.operlevel == 4:
													linkclose = False
													try:
														if param[2].upper() == "STOP":
															linkclose = True
													except:
														pass

													linked = False
													for each in servers:
														if each._serverName == param[1]:
															if each._use == False or linkclose == True:
																linked = True
																for op in opers:
																	opid1 = opers[op]
																	e = nicknames[op.lower()]
																	if opid1.operlevel >= 3: # Send to admins or above
																		if linkclose:
																			if each._use:
																				each._use = False
																				each._close = True
																			else:
																				e.send(":" + ServerName + " NOTICE LINK :*** There is currently no link to this server\r\n")
																				break

																			e.send(":" + ServerName + " NOTICE LINK :*** " + self._nickname + " has terminated the link to " + each._serverName + "@" + each._serverAddress + "\r\n")
																		else:
																			Link(each).start()
																
															else:
																self.send(":" + ServerName + " NOTICE LINK :*** There is already a link or an attempt to link to " + param[1] + ", duplicate links are invalid\r\n")
																linked = True
																break

																
															break
												
													if linked == False:
														self.send(":" + ServerName + " NOTICE LINK :*** Could not find the server named " + param[1] + "\r\n")
											
												else:
													raw(self,"481",self._nickname,"Permission Denied - You're not the Network Administrator")
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not a System Operator")

										except IndexError:
											self.send(":" + ServerName + " NOTICE LINK :*** Not enough parameters to link\r\n")

									elif param[0] == "GAG":
										if opid:
											if cid:
												if cid in opers:
													raw(self,"481",self._nickname,"Permission Denied - Can't /GAG another Operator")
												else:
													cid.send(":%s MODE %s +z\r\n" % (ServerName,cid._nickname))
													self.send(":" + ServerName + " NOTICE GAG :*** " + self._nickname + " Added " + cid._nickname + " to the GAG list\r\n")
													cid._MODE_gag = True
													if "z" not in cid._MODE_: cid._MODE_ = cid._MODE_ + "z"
													for allservers in linkedServers: allservers.sendUserMode(cid._nickname,"+z")
											else:
												raw(self,"401",self._nickname,param[1])
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "UNGAG":
										if opid:
											if cid:
												if cid in opers:
													raw(self,"481",self._nickname,"Permission Denied - Can't use /UNGAG with another Operator")	
												else:
													cid.send(":%s MODE %s -z\r\n" % (ServerName,cid._nickname))
													self.send(":" + ServerName + " NOTICE GAG :*** " + self._nickname + " Removed " + cid._nickname + " from the GAG list\r\n")
													cid._MODE_gag = False
													cid._MODE_.replace("z","")
													for allservers in linkedServers: allservers.sendUserMode(cid._nickname,"-z")
											else:
												raw(self,"401",self._nickname,param[1])
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "GLOBAL":
										if opid:
											if opid.operlevel > 2:
												for each in nicknames:
													cid = nicknames[each.lower()]
													cid.send(":" + NetworkName + " NOTICE " + cid._nickname + " :" + strdata.split(" ",1)[1] + "\r\n")
													for allservers in linkedServers: allservers.sendMessage(NetworkName,"NOTICE",strdata.split(" ",1)[1])
													
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "SNAME":
										if opid:
											if cid:
												if copid and copid != opid:
													self.send(":" + ServerName + " NOTICE SERVER :*** Cannot use /SNAME on another operator\r\n")
												else:
													if len(param) == 2:
														cid._friendlyname = ""
														self.send(":" + ServerName + " NOTICE SERVER :*** Removed friendly name of " + cid._nickname + "\r\n")
														cid.send(":%s MODE %s -X\r\n" % (ServerName,cid._nickname))
														cid._MODE_ = cid._MODE_.replace("X","")
														for allservers in linkedServers: allservers.sendUserMode(cid._nickname,"-X")
													else:
														cid._friendlyname = " ".join(param).split(" ",2)[2]
														cid.send(":%s MODE %s +X\r\n" % (ServerName,cid._nickname))
														self.send(":" + ServerName + " NOTICE SERVER :*** Changed the friendly name of " + cid._nickname + " to '" + cid._friendlyname + "'\r\n")
														if "X" not in cid._MODE_: cid._MODE_ = cid._MODE_ + "X"
														for allservers in linkedServers: allservers.sendUserMode(cid._nickname,"+X " + cid._friendlyname)
													
											else:
												raw(self,"401",self._nickname,param[1])
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "CHGIDENT":
										if opid:
											if opid.operlevel > 2:
												if cid:
													if self._validate(param[2]):
														if copid:
															self.send(":" + ServerName + " NOTICE SERVER :*** Cannot use /CHGIDENT on another operator\r\n")
														else:
															cid._username = param[2]
															self.send(":" + ServerName + " NOTICE SERVER :*** Changed the username of " + cid._nickname + " to '" + param[2] + "'\r\n")
															for allservers in linkedServers: allservers.sendHostIdentNameChange(cid._nickname,cid._username,0,0)
													else:
														raw(self,"434",self._nickname,param[1])
												else:
													raw(self,"401",self._nickname,param[1])
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "CHGHOST":
										if opid:
											if opid.operlevel > 2:
												if cid:
													if self._validate(param[2].replace(".","a").replace("/","a")):
														if copid:
															self.send(":" + ServerName + " NOTICE SERVER :*** Cannot use /CHGHOST on another operator\r\n")
														else:
															cid._hostmask = param[2]
															self.send(":" + ServerName + " NOTICE SERVER :*** Changed the hostmask of " + cid._nickname + " to '" + param[2] + "'\r\n")
															for allservers in linkedServers: allservers.sendHostIdentNameChange(cid._nickname,0,cid._hostmask,0)
													else:
														self.send(":" + ServerName + " NOTICE SERVER :Invalid hosname, hostname must contain only letters and numbers\r\n")
												else:
													raw(self,"401",self._nickname,param[1])
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "CHGNAME":
										if opid:
											if opid.operlevel > 2:
												if cid:
													if self._validatefullname(strdata.split(" ",2)[2].replace(".","a")):
														if copid:
															self.send(":" + ServerName + " NOTICE SERVER :*** Cannot use /CHGNAME on another operator\r\n")
														else:
															cid._fullname = strdata.split(" ",2)[2].replace("  ","")
															self.send(":" + ServerName + " NOTICE SERVER :*** Changed the fullname of " + cid._nickname + " to '" + strdata.split(" ",2)[2] + "'\r\n")
															for allservers in linkedServers: allservers.sendHostIdentNameChange(cid._nickname,0,0,cid._fullname)
													else:
														self.send(":" + ServerName + " NOTICE SERVER :Invalid fullname\r\n")
												else:
													raw(self,"401",self._nickname,param[1])
											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "SETIDENT":
										if opid:
											if self._validate(param[1]):
												self._username = param[1]
												for allservers in linkedServers: allservers.sendHostIdentNameChange(self._nickname,self._username,0,0)
												self.send(":" + ServerName + " NOTICE SERVER :*** Your username is now '" + param[1] + "'\r\n")
											else:
												raw(self,"434",self._nickname,param[1])
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "SETHOST":
										if opid:
											if self._validate(param[1].replace(".","a").replace("/","a")):
												self._hostmask = param[1]
												for allservers in linkedServers: allservers.sendHostIdentNameChange(self._nickname,0,self._hostmask,0)
												self.send(":" + ServerName + " NOTICE SERVER :*** Your hostname is now '" + param[1] + "'\r\n")
											else:
												self.send(":" + ServerName + " NOTICE SERVER :Invalid hosname, hostname must contain only letters and numbers\r\n")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "SETNAME":
										if opid:
											if self._validatefullname(strdata.split(" ",1)[1].replace(" ","a").replace("/","a")):
												self._fullname = strdata.split(" ",1)[1].replace("  ","")
												self.send(":" + ServerName + " NOTICE SERVER :*** Your fullname is now '" + strdata.split(" ",1)[1] + "'\r\n")
												for allservers in linkedServers: allservers.sendHostIdentNameChange(self._nickname,0,0,self._fullname)
											else:
												self.send(":" + ServerName + " NOTICE SERVER :Invalid fullname, please choose a more suitable fullname\r\n")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

									elif param[0] == "MODE":
										Mode_function(self,param,strdata)

									elif param[0] == "TOPIC":
										if len(param) == 2:
											if chanid:
												if isSecret(chanid,"private") and self._nickname.lower() not in opers and self._nickname.lower() not in chanid._users:
													raw(self,"331",self._nickname,chanid.channelname)
												else:
													if chanid._topic != "":
														raw(self,"332",self._nickname,chanid.channelname,chanid._topic)
														raw(self,"333",self._nickname,chanid.channelname,chanid._topic_nick,chanid._topic_time)

													else: raw(self,"331",self._nickname,chanid.channelname)
											else:
												raw(self,"403",self._nickname,param[1])
												
										else:
											if chanid:
												if self._nickname.lower() in chanid._users:
													dotopic = False

													if chanid.MODE_optopic == False or self._nickname.lower() in chanid._op or self._nickname.lower() in chanid._owner: dotopic = True

													if dotopic:
														if chanid.MODE_ownertopic and self._nickname.lower() not in chanid._owner:
															raw(self,"485",self._nickname,chanid.channelname)
														else:	
															chanid._topic = param[2]
															if chanid._topic[0] == ":": chanid._topic = strdata.split(" ",2)[2][1:]

															if chanid._topic == "":
																chanid._topic = ""
															else:
																chanid._topic_nick = self._nickname
																chanid._topic_time = GetEpochTime()

															for each in chanid._users:
																clientid = nicknames[each]
																clientid.send(":%s!%s@%s TOPIC %s :%s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,chanid._topic))
													else:
														raw(self,"482",self._nickname,chanid.channelname)
												else:
													raw(self,"442",self._nickname,chanid.channelname)
											else:
												raw(self,"403",self._nickname,param[1])

									elif param[0] == "OPER":
										Oper_function(self,param)

									elif param[0] == "WHISPER":
										if chanid:
											if self._nickname.lower() in chanid._users:
												if cid:
													if param[2].lower() in chanid._users:
														wmsg = param[3]
														if wmsg[0] == ":": wmsg = strdata.split(" ",3)[3][1:]
														if wmsg != ":":

															if self.selfaccess(cid) == True:
																if chanid.MODE_whisper:
																	if cid._nickname.lower() in chanid._op or cid._nickname.lower() in chanid._owner or self._nickname.lower() in chanid._op or self._nickname.lower() in chanid._owner:
																		if self._MODE_nowhisper and self._nickname.lower() not in opers:
																			self.send(":" + ServerName + " NOTICE SERVER :*** You cannot whisper if +P is set\r\n")
																		else:
																			if cid._MODE_nowhisper:
																				self.send(":" + ServerName + " NOTICE SERVER :*** This user has chosen not to receive whispers\r\n")
																			else:
																				cid.send(":%s!%s@%s WHISPER %s %s :%s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,cid._nickname,wmsg))
																	else:
																		raw(self,"923",self._nickname,chanid.channelname)
																else:
																	if self._MODE_nowhisper and self._nickname.lower() not in opers:
																		self.send(":" + ServerName + " NOTICE SERVER :*** You cannot whisper if +P is set\r\n")
																	else:
																		if cid._MODE_nowhisper:
																			self.send(":" + ServerName + " NOTICE SERVER :*** This user has chosen not to receive whispers\r\n")
																		else:
																			cid.send(":%s!%s@%s WHISPER %s %s :%s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,cid._nickname,wmsg))
														else:
															raw(self,"412",self._nickname,param[0])
													else:
														raw(self,"441",self._nickname,chanid.channelname)
												else:
													raw(self,"401",self._nickname,param[2])
											else:
												raw(self,"442",self._nickname,chanid.channelname)
										else:
											raw(self,"403",self._nickname,param[1])


									elif param[0] == "PRIVMSG" or param[0] == "NOTICE":
										try:
											if len(param) == 2:
												raw(self,"412",self._nickname,param[0])    # no text to send
											elif param[2] == ":" and len(param) == 3:
												raw(self,"412",self._nickname,param[0])    # no text to send
											
											elif param[1].upper() == "NICKSERV": # support for /msg nickserv
												Nickserv_function(self,param[1:],param[0])
											else:

												iloop=0
												chans = []
												if param[1].lower() not in channels and param[1].lower() not in nicknames: self.pmflooding+=1

												while iloop < len(param[1].split(",")):
													if iloop == 32: break
													recipient = param[1].split(",")[iloop].lower()

													if recipient not in opers and self._MODE_gag:
														self.send(":" + ServerName + " NOTICE GAG :*** You are unable to participate because you are on the server GAG list\r\n")
													else:

														recip = getUserOBJ(recipient.lower())

														if recipient.lower() not in chans:
															chans.append(recipient.lower())
															self._idletime = GetEpochTime()
															msg = param[2]
															if msg[0] == ":": msg = strdata.split(" ",2)[2][1:]

															if recipient.lower() in channels: #channel exists
																chanclass = channels[recipient]
																chanclass.communicate(self._nickname,param[0],msg)
																if self._nickname.lower() not in opers:
																	if isOp(self._nickname.lower(),chanclass.channelname):
																		floodtime = 1000
																	else:
																		floodtime = 2000

																	if int((GetEpochTime() - self.pmlastcommand)*1000) <= floodtime:	# let's work in ms shall we?
																		if param[1].lower() in channels: self.pmflooding+=1

																	else:
																		self.pmflooding = 0
																	
																	self.pmlastcommand = GetEpochTime()

																	if isOp(self._nickname.lower(),chanclass.channelname):
																		floodlimit = 50
																	else:
																		floodlimit = 30
																	
																	if self.pmflooding == floodlimit and "PRIVMSG" not in FloodingExempt: # 15 commands per 1000 miliseconds, anymore than that will kill the user
																		print "Input flooding!!"
																		self.quittype = 4
																		self.send("ERROR :Closing Link: " + self.details[0] + " (Input flooding)\r\n")
																		self.die = True
																		self.close()

																	if myint(chanclass._prop.lag) != 0 and isOp(self._nickname.lower(),chanclass.channelname)== False:
																		time.sleep(chanclass._prop.lag)

															
															elif recipient[0] == "*" or recipient[0] == "$":  # cannot ignore server messages using access
																if opid:
																	if recipient[0] == "$":
																		for n in nicknames:
																			cclientid = nicknames[n.lower()]
																			cclientid.send(":%s!%s@%s %s %s :%s\r\n" % (self._nickname,self._username,self._hostmask,param[0].upper(),cclientid._nickname,msg))
																	else:
																		if opid.operlevel > 2:
																			for n in nicknames:
																				cclientid = nicknames[n.lower()]
																				cclientid.send(":%s!%s@%s %s %s :%s\r\n" % (self._nickname,self._username,self._hostmask,param[0].upper(),cclientid._nickname,msg))

																			for allservers in linkedServers: allservers.sendMessage(self._nickname,param[0],msg)

																		else:
																			raw(self,"481",self._nickname,"Permission Denied - You're not an Administratorr")
																else:
																	raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

															elif recip:
																floodtime = 1000
																if int((GetEpochTime() - self.pmlastcommand)*1000) <= floodtime:	# let's work in ms shall we?
																	if param[1].lower() in nicknames:
																		self.pmflooding+=1
																else:
																	self.pmflooding = 0
																
																self.pmlastcommand = GetEpochTime()

																floodlimit = 20
																
																if self.pmflooding == floodlimit: # 15 commands per 1000 miliseconds, anymore than that will kill the user
																	print "Input flooding!!"
																	self.quittype = 4
																	self.send("ERROR :Closing Link: " + self.details[0] + " (Input flooding)\r\n")
																	self.die = True
																	self.close()

																if self._MODE_private and self._nickname.lower() not in opers:
																	self.send(":" + ServerName + " NOTICE SERVER :*** You cannot send private messages if +p is set\r\n")
																else:
																	if recip._MODE_private == False or self._nickname.lower() in opers: # opers can send messages to users with private set
																		sendprivmsg = True
																		if self.selfaccess(recip) == False: sendprivmsg = False
																		if recip._MODE_filter:
																			foundprofanity=False
																			for all in profanity:
																				tmsg = re.compile(all.lower().replace(".",r"\.").replace("*","(.+|)"))
																				if tmsg.match(msg.lower()):
																					foundprofanity = True
																					break

																			if foundprofanity:
																				self.send(":" + ServerName + " NOTICE SERVER :*** This user has chosen not to receive filtered content\r\n")
																				sendprivmsg = False

																		if sendprivmsg:

																			if recip._MODE_registerchat and self._MODE_register == False and self._nickname.lower() not in opers and self != recip:
																				self.send(":" + ServerName + " NOTICE SERVER :*** Cannot send a message to this user, you must register or identify your nickname to services first\r\n")
																			else:
																				if recipient.lower() in nicknames:
																					recip.send(":%s!%s@%s %s %s :%s\r\n" % (self._nickname,self._username,self._hostmask,param[0].upper(),recip._nickname,msg))
																				else:
																					for each in linkedServers:
																						if recipient in each._nicknames:
																							each.sendUserPrivmsg(self._nickname.lower(),recipient.lower(),param[0],msg)
																							break

																	else:
																		self.send(":" + ServerName + " NOTICE SERVER :*** This user has chosen not to receive  filtered content\r\n")

															else:
																raw(self,"401",self._nickname,recipient)
															
													iloop+=1

												del chans

										except IndexError:
											raw(self,"411",self._nickname,param[0])

																	
									elif param[0] == "INVITE":
										if self._MODE_inviteblock:
											raw(self,"998",self._nickname,self._nickname,"*")
										else:
											if param[2].lower() in channels:
												chanid = channels[param[2].lower()]
												if self._nickname.lower() in chanid._users:
													if param[1].lower() in nicknames:
														if self._nickname.lower() in chanid._op or self._nickname.lower() in chanid._owner:
															cid = nicknames[param[1].lower()]
															if cid._MODE_inviteblock:
																raw(self,"998",self._nickname,cid._nickname,chanid.channelname)
															else:
																if param[1].lower() in chanid._users and param[1].lower() not in chanid._watch:
																	raw(self,"443",self._nickname,cid._nickname,chanid.channelname)
																else:

																	sendinvite = True
																	if self.selfaccess(cid) == False: sendinvite = False

																	if sendinvite:
																		raw(self,"341",self._nickname,cid._nickname,chanid.channelname)
																		cid.send(":%s!%s@%s INVITE %s :%s\r\n" % (self._nickname,self._username,self._hostmask,cid._nickname,chanid.channelname))
																		cid._invites.append(chanid.channelname.lower())	
														else:
															raw(self,"482",self._nickname,chanid.channelname)
													else:
														raw(self,"401",self._nickname,param[1])
												else:
													raw(self,"442",self._nickname,chanid.channelname)
											else:
												raw(self,"403",self._nickname,param[2])


									elif param[0] == "PART":
										iloop = 0
										while iloop < len(param[1].split(",")):
											chan = getChannelOBJ(param[1].split(",")[iloop].lower())
											if chan:
												chan.part(self._nickname)
											else:
												raw(self,"403",self._nickname,param[1].split(",")[iloop])
										
											iloop+=1

									elif param[0] == "NAMES":
										if chanid: chanid.sendnames(self._nickname) # send when requested
										elif param[1][0] == "*": raw(self,"481",self._nickname,"Permission Denied")
										else: raw(self,"403",self._nickname,param[1])

									elif param[0] == "LISTC":
										raw(self,"321",self._nickname)
										for chanid in getGlobalChannels():
											chanusers = str(len(chanid._users) - len(chanid._watch))
											if chanid.MODE_auditorium and self._nickname.lower() not in opers and isOp(self._nickname.lower(),chanid.channelname) == False:
												chanusers = str((len(chanid._op) + len(chanid._owner)))
											if len(param) == 2:
												sub = param[1]
											else:
												sub = ""
											
											if chanid._prop.subject.upper() == sub.upper():
												if isSecret(chanid,"hidden"):
													if self._nickname.lower() in chanid._users or self._nickname.lower() in opers:
														raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)
												else:
													raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)	
											
										raw(self,"323",self._nickname)

									elif param[0] == "LIST" or param[0] == "LISTX":
										try:
											raw(self,"321",self._nickname)
											for chanid in getGlobalChannels():
												print chanid.channelname
												#chanid = channels[each.lower()]
												chanusers = str(len(chanid._users) - len(chanid._watch))
												if chanid.MODE_auditorium and self._nickname.lower() not in opers and isOp(self._nickname.lower(),chanid.channelname) == False:
													chanusers = str((len(chanid._op) + len(chanid._owner)))

												if isSecret(chanid,"hidden"):
													if self._nickname.lower() in chanid._users or self._nickname.lower() in opers:
														raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)
												else:
													if param[0] == "LISTX" and len(param) == 2:

														if "<" in param[1]:
															if len(param[1].split("<")) == 2: lowerthanparam = param[1].split("<")[1].split(",")[0]
															if myint(chanusers) < myint(lowerthanparam):
																raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)

														elif ">" in param[1]:
															if len(param[1].split(">")) == 2: lowerthanparam = param[1].split(">")[1].split(",")[0]
															if myint(chanusers) > myint(lowerthanparam):
																raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)
														elif "R=0" == param[1]:
															if chanid.MODE_registered == False:
																raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)

														elif "IRCX=0" == param[1]:
															if chanid.MODE_noircx:
																raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)

														elif "IRCX=1" == param[1]:
															if chanid.MODE_noircx == False:
																raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)


														elif "R=1" == param[1]:
															if chanid.MODE_registered:
																raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)

														elif "N=" in param[1]:
															try:
																matchstring = param[1].split("=",1)[1].lower()
																if matchstring in chanid.channelname.lower():
																	raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)

															except:
																pass

														elif "T=" in param[1]:
															try:
																matchstring = param[1].split("=",1)[1].lower()
																if matchstring in chanid._topic.lower():
																	raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)

															except:
																pass
															
														else:
															raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)
															
													else:
														raw(self,"322",self._nickname,chanid.channelname,chanusers,chanid._topic)
										except:
											pass

										raw(self,"323",self._nickname)
									
									elif param[0] == "ACCESS":
										if chanid:
											_Access.CheckChannelExpiry(chanid)
											if len(param) == 2:
												if chanid.MODE_noircx and self._nickname.lower() not in opers:
													raw(self,"997",self._nickname,chanid.channelname,param[0])
												else:
													if isOp(self._nickname,chanid.channelname) == False:
														raw(self,"913",self._nickname,chanid.channelname)
													else:
														raw(self,"803",self._nickname,chanid.channelname)
														for each in chanid.ChannelAccess:
															if each._deleteafterexpire == False:
																exp = 0
															else:
																exp = (each._expires - GetEpochTime()) / 60
																if exp < 1: exp = 0

															stringinf = "%s %s %s %d %s %s" % (chanid.channelname,each._level,each._mask,exp,each._setby,each._reason)
															raw(self,"804",self._nickname,stringinf)

														raw(self,"805",self._nickname,chanid.channelname)
											else:
												try:
													if chanid.MODE_noircx and self._nickname.lower() not in opers:
														raw(self,"997",self._nickname,chanid.channelname,param[0])

													elif chanid.MODE_ownersetaccess and self._nickname.lower() not in chanid._owner and self._nickname.lower() not in opers:
														raw(self,"485",self._nickname,chanid.channelname)
													
													elif param[2].upper() == "ADD":
														if param[3].upper() == "DENY" or param[3].upper() == "GRANT"  or param[3].upper() == "VOICE"  or param[3].upper() == "HOST"  or param[3].upper() == "OWNER":
															if len(chanid.ChannelAccess) > myint(MaxChannelEntries):
																raw(self,"916",self._nickname,chanid.channelname)
															else:				    # ACCESS # ADD OWNER
																if len(param) == 4: param.append("*!*@*$*")
																_mask = _Access.CreateMaskString(param[4])
																if _mask == -1: raw(self,"906",self._nickname,param[4])
																elif _mask == -2: raw(self,"909",self._nickname)
																else:
																	tag,exp = "",0
																	if len(param) >= 6: exp = myint(param[5])
																	if len(param) >= 7:
																		if param[6][0] == ":":
																			tag = strdata.split(" ",6)[6]
																		else:
																			tag = param[6]
																	
																	_addrec = _Access.AddRecord(self,chanid.channelname,param[3].upper(),_mask,exp,tag)
																	if  _addrec == 1:
																		stringinf = "%s %s %s %d %s %s" % (chanid.channelname,param[3].upper(),_mask,exp,self._hostmask,tag)
																		raw(self,"801",self._nickname,stringinf)

																	elif _addrec == -1:
																		raw(self,"914",self._nickname,chanid.channelname)

																	elif _addrec == -2:
																		raw(self,"913",self._nickname,chanid.channelname)
																	else:
																		pass
														else:
															raw(self,"903",self._nickname,chanid.channelname)

													elif param[2].upper() == "DELETE":
														if len(param) < 4:
															raw(self,"903",self._nickname,chanid.channelname)
														else:
															if param[3].upper() == "DENY" or param[3].upper() == "GRANT" or param[3].upper() == "VOICE" or param[3].upper() == "HOST" or param[3].upper() == "OWNER":
																if len(param) == 4: param.append("*!*@*$*")
																_mask = _Access.CreateMaskString(param[4])
																if _mask == -1: raw(self,"906",self._nickname,param[4])
																elif _mask == -2: raw(self,"909",self._nickname)
																else:
																	_delrec = _Access.DelRecord(self,chanid.channelname,param[3].upper(),_mask)
																	if _delrec == 1:
																		stringinf = "%s %s %s" % (chanid.channelname,param[3].upper(),_mask)
																		raw(self,"802",self._nickname,stringinf)
		
																	elif _delrec == -1:
																		raw(self,"915",self._nickname,chanid.channelname)
																	elif _delrec == -2:
																		raw(self,"913",self._nickname,chanid.channelname)
															else:
																raw(self,"903",self._nickname,chanid.channelname)

													elif param[2].upper() == "CLEAR":
														if len(param) > 3:
															if param[3].upper() != "DENY" and param[3].upper() != "GRANT"  and param[3].upper() != "VOICE"  and param[3].upper() != "HOST"  and param[3].upper() != "OWNER":
																raw(self,"900",self._nickname,param[3])
															else:	
																_Access.ClearRecords(chanid.channelname,self,param[3].upper())

														elif len(param) > 2: _Access.ClearRecords(chanid.channelname,self)

													elif param[2].upper() == "LIST":
														if isOp(self._nickname,chanid.channelname) == False:
															raw(self,"913",self._nickname,chanid.channelname)
														else:
															raw(self,"803",self._nickname,chanid.channelname)
															for each in chanid.ChannelAccess:
																if each._deleteafterexpire == False:
																	exp = 0
																else:
																	exp = (each._expires - GetEpochTime()) / 60
																	if exp < 1: exp = 0

																stringinf = "%s %s %s %d %s %s" % (chanid.channelname,each._level,each._mask,exp,each._setby,each._reason)
																raw(self,"804",self._nickname,stringinf)

															raw(self,"805",self._nickname,chanid.channelname)

													elif param[2].upper() == "REGISTER":
														operuser = isAdmin(self._nickname)
														if operuser != "":
															if chanid.MODE_registered == False:
																chanid.MODE_registered = True
																chanid._prop.registered = operuser
																_founder = ""
																if len(param) == 4:
																	_founder = _Access.CreateMaskString(param[3])
																	if _founder == -1:
																		_founder = ""
																		raw(self,"906",self._nickname,param[4])
																	elif _founder == -2:
																		_founder = ""
																		raw(self,"909",self._nickname)

																	else:
																		_addrec = _Access.AddRecord("",chanid.channelname.lower(),"OWNER",_founder,0,"")
																		stringinf = "%s %s %s %d %s %s" % (chanid.channelname,"FOUNDER",_founder,0,ServerName,"")
																		raw(self,"801",self._nickname,stringinf)

																#Channel=#testModes=ntfrdSl 25Subject=AdultTopic=Chat related difficultiesfounderaccess=&chris

																chanid._founder = _founder

																for each in chanid._users:
																	cclientid = nicknames[each]
																	cclientid.send(":%s MODE %s +r\r\n" % (ServerName,chanid.channelname))

																sendWatchOpers("Notice -- The channel, '%s' has been registered (%s!%s@%s) [%s] \r\n" % (chanid.channelname,self._nickname,self._username,self._hostmask,self.details[0]))

																WriteUsers(MaxLocal,MaxGlobal,False,True)
															else:
																self.send(":%s NOTICE %s :*** Notice -- Channel is already registered\r\n" % (ServerName,self._nickname))
														else:
															raw(self,"908",self._nickname)

													elif param[2].upper() == "UNREGISTER":
														operuser = isAdmin(self._nickname)
														if operuser != "":
															if chanid.MODE_registered == True:
																chanid.MODE_registered = False
																chanid._prop.registered = ""
																chanid._founder = ""

																_Access.ClearRecords(chanid.channelname,self,"OWNER")

																for each in chanid._users:
																	cclientid = nicknames[each]
																	cclientid.send(":%s MODE %s -r\r\n" % (ServerName,chanid.channelname))
																
																sendWatchOpers("Notice -- The channel, '%s' has been unregistered (%s!%s@%s) [%s] \r\n" % (chanid.channelname,self._nickname,self._username,self._hostmask,self.details[0]))

																if len(chanid._users) == 0:
																	chanid.resetchannel()
																
																WriteUsers(MaxLocal,MaxGlobal,False,True)
															else:
																self.send(":%s NOTICE %s :*** Notice -- Channel is not registered\r\n" % (ServerName,self._nickname))


														else:
															raw(self,"908",self._nickname)
													else:
														raw(self,"900",self._nickname,param[1])
												except:
													raw(self,"903",self._nickname,param[1])

										elif param[1] == "*" or param[1] == "$" or param[1].upper() == self._nickname.upper():

											if param[1] != "*" and param[1] != "$":
												ret = self._nickname
												_list = self._access
											else:
												CheckServerAccess()
												ret = "*"
												_list = ServerAccess
											
											_Access.CheckSelfExpiry(self)

											if opid or param[1] != "*":
												operlvl = False
												if param[1] == "*":
													if opid.operlevel > 1:
														operlvl = True

												if operlvl == False and param[1] == "*":
													raw(self,"913",self._nickname,param[1])
												else:
													if len(param) == 2:
														raw(self,"803",self._nickname,ret)
														for each in _list:
															if each._deleteafterexpire == False:
																exp = 0
															else:
																exp = (each._expires - GetEpochTime()) / 60
																if exp < 1: exp = 0
														
															stringinf = "%s %s %s %d %s %s" % (ret,each._level,each._mask,exp,each._setby,each._reason)
															raw(self,"804",self._nickname,stringinf)

														raw(self,"805",self._nickname,ret)
													
													else:

														try:
															if param[2].upper() == "ADD": # access * add deny test
																if len(param) < 4:
																	raw(self,"903",self._nickname,ret)
																else:
																	if param[3].upper() == "DENY" or param[3].upper() == "GRANT":
																		if ret == "*":
																			_entries = MaxServerEntries
																		else:
																			_entries = MaxUserEntries

																		if len(_list) > myint(_entries):
																			raw(self,"916",self._nickname,ret)
																		else:
																			_mask = _Access.CreateMaskString(param[4])
																			if _mask == -1: raw(self,"906",self._nickname,param[4])
																			elif _mask == -2: raw(self,"909",self._nickname)
																			else:
																				tag,exp = "",0
																				if len(param) >= 6: exp = myint(param[5])
																				if len(param) >= 7:
																					if param[6][0] == ":":
																						tag = strdata.split(" ",6)[6]
																					else:
																						tag = param[6]
																				
																				_addrec = _Access.AddRecord(self,ret,param[3].upper(),_mask,exp,tag)
																				if _addrec == 1:
																					stringinf = "%s %s %s %d %s %s" % (ret,param[3].upper(),_mask,exp,self._hostmask,tag)
																					raw(self,"801",self._nickname,stringinf)	
																					if ret == "*":
																						sendWatchOpers("Notice -- The record, '%s %s' has been added to server access by (%s!%s@%s) [%s] \r\n" % (param[3].upper(),_mask,self._nickname,self._username,self._hostmask,self.details[0]))

																					WriteUsers(MaxLocal,MaxGlobal,False,False,True)

																				elif _addrec == -1:
																					raw(self,"914",self._nickname,param[1])
																				else:
																					pass

																	else:
																		raw(self,"903",self._nickname,ret)

															elif param[2].upper() == "DELETE":
																if len(param) < 4:
																	raw(self,"903",self._nickname,ret)
																else:
																	if param[3].upper() == "DENY" or param[3].upper() == "GRANT":
																		_mask = _Access.CreateMaskString(param[4])
																		if _mask == -1: raw(self,"906",self._nickname,param[4])
																		elif _mask == -2: raw(self,"909",self._nickname)
																		else:
																			_delrec = _Access.DelRecord(self,ret,param[3].upper(),_mask)
																			if _delrec == 1:
																				stringinf = "%s %s %s" % (ret,param[3].upper(),_mask)
																				raw(self,"802",self._nickname,stringinf)
																				if ret == "*":
																					sendWatchOpers("Notice -- The record, '%s %s' was requested to be deleted (%s!%s@%s) [%s] \r\n" % (param[3].upper(),_mask,self._nickname,self._username,self._hostmask,self.details[0]))

																				WriteUsers(MaxLocal,MaxGlobal,False,False,True)

																			elif _delrec == -1:
																				raw(self,"915",self._nickname,ret)
																			elif _delrec == -2:
																				raw(self,"913",self._nickname,ret)
																	else:
																		raw(self,"903",self._nickname,ret)


															elif param[2].upper() == "CLEAR": #access # clear [deny]
																if len(param) > 3:
																	if param[3].upper() != "DENY" and param[3].upper() != "GRANT":
																		raw(self,"900",self._nickname,param[3])
																	else:	
																		_Access.ClearRecords(ret,self,param[3].upper())
																		if ret == "*":
																			sendWatchOpers("Notice -- Server access clear, '%s' has been cleared by (%s!%s@%s) [%s] \r\n" % (param[3].upper(),self._nickname,self._username,self._hostmask,self.details[0]))

																		WriteUsers(MaxLocal,MaxGlobal,False,False,True)

																elif len(param) > 2:
																	_Access.ClearRecords(ret,self)
																	if ret == "*":
																		sendWatchOpers("Notice -- Server access has been cleared (%s!%s@%s) [%s] \r\n" % (self._nickname,self._username,self._hostmask,self.details[0]))

																	WriteUsers(MaxLocal,MaxGlobal,False,False,True)
																
															elif param[2].upper() == "LIST":
																raw(self,"803",self._nickname,ret)
																for each in _list:
																	if each._deleteafterexpire == False:
																		exp = 0
																	else:
																		exp = (each._expires - GetEpochTime()) / 60
																		if exp < 1: exp = 0

																	stringinf = "%s %s %s %d %s %s" % (ret,each._level,each._mask,exp,each._setby,each._reason)
																	raw(self,"804",self._nickname,stringinf)

																raw(self,"805",self._nickname,ret)
															else:
																raw(self,"900",self._nickname,ret)
														except:
															raw(self,"903",self._nickname,ret)
											else:
												raw(self,"913",self._nickname,ret)

										elif cid:
											raw(self,"925",self._nickname,param[1])

										else:
											raw(self,"924",self._nickname,param[1])

									elif param[0] == "PROP":
										if len(param) > 2:
											if chanid:
												if chanid.MODE_noircx and self._nickname.lower() not in opers:
													raw(self,"997",self._nickname,chanid.channelname,param[1])

												elif param[2].upper() == "*":
													if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
														raw(self,"818",self._nickname,"%s OID :0" % (chanid.channelname))
														raw(self,"818",self._nickname,"%s Name :%s" % (chanid.channelname,chanid.channelname))

														if self._nickname.lower() in opers:
															if chanid._prop.account:
																raw(self,"818",self._nickname,"%s Account :%s!%s@%s (%s)" % (chanid.channelname,chanid._prop.account_name,chanid._prop.account_user,chanid._prop.account_hostmask,chanid._prop.account_address))
															else:
																raw(self,"818",self._nickname,"%s Account :%s" % (chanid.channelname,ServerName))
														
														if self._nickname.lower() in opers and chanid.MODE_registered:
															raw(self,"818",self._nickname,"%s Registered :%s" % (chanid.channelname,chanid._prop.registered))
														

														raw(self,"818",self._nickname,"%s Creation :%s" % (chanid.channelname,chanid._prop.creation))
														if chanid._prop.ownerkey != "" and self._nickname.lower() in chanid._owner or self._nickname.lower() in opers and chanid._prop.ownerkey != "" : raw(self,"818",self._nickname,"%s Ownerkey :%s" % (chanid.channelname,chanid._prop.ownerkey))
														if chanid._prop.hostkey != "" and self._nickname.lower() in chanid._owner or self._nickname.lower() in opers and chanid._prop.hostkey != "" : raw(self,"818",self._nickname,"%s Hostkey :%s" % (chanid.channelname,chanid._prop.hostkey))
														if chanid.MODE_key != "" and self._nickname.lower() in chanid._users: raw(self,"818",self._nickname,"%s Memberkey :%s" % (chanid.channelname,chanid.MODE_key))
														
														if chanid._prop.reset != 0:
															raw(self,"818",self._nickname,"%s Reset :%d" % (chanid.channelname,chanid._prop.reset))

														if chanid._prop.language != "":
															raw(self,"818",self._nickname,"%s Language :%s" % (chanid.channelname,chanid._prop.language))

														if chanid._topic != "":
															if chanid._topic[0] == ":":
																raw(self,"818",self._nickname,"%s Topic %s" % (chanid.channelname,chanid._topic))
															else:
																raw(self,"818",self._nickname,"%s Topic :%s" % (chanid.channelname,chanid._topic))
														if chanid._prop.client != "":
															raw(self,"818",self._nickname,"%s Client :%s" % (chanid.channelname,chanid._prop.client))
														if chanid._prop.lag != "" and myint(chanid._prop.lag) != 0: 
															raw(self,"818",self._nickname,"%s Lag :%s" % (chanid.channelname,chanid._prop.lag))
														if chanid._prop.onjoin != "": 
															raw(self,"818",self._nickname,"%s Onjoin :%s" % (chanid.channelname,chanid._prop.onjoin))
														if chanid._prop.onpart != "": 
															raw(self,"818",self._nickname,"%s Onpart :%s" % (chanid.channelname,chanid._prop.onpart))
														if chanid._prop.subject != "": 
															raw(self,"818",self._nickname,"%s Subject :%s" % (chanid.channelname,chanid._prop.subject))

													raw(self,"819",self._nickname,chanid.channelname)

												#add elif for if prop is disabled for owners

												elif chanid.MODE_ownersetprop and self._nickname.lower() not in chanid._owner and len(param) > 3 and self._nickname.lower() not in opers:
													raw(self,"485",self._nickname,chanid.channelname)

												elif param[2].upper() == "CLIENT":
													if len(param) == 3:
														if chanid._prop.client != "":
															if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
																raw(self,"818",self._nickname,"%s Client :%s" % (chanid.channelname,chanid._prop.client))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._client(chanid,self,param[3])

												elif param[2].upper() == "SUBJECT":
													if len(param) == 3:
														if chanid._prop.subject != "":
															if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
																raw(self,"818",self._nickname,"%s Subject :%s" % (chanid.channelname,chanid._prop.subject))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._subject(chanid,self,param[3])

												elif param[2].upper() == "LAG":
													if len(param) == 3:
														if myint(chanid._prop.lag) != 0:
															if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
																raw(self,"818",self._nickname,"%s Lag :%s" % (chanid.channelname,chanid._prop.lag))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._lag(chanid,self,param[3])

												elif param[2].upper() == "LANGUAGE":
													if len(param) == 3:
														if chanid._prop.language != "":
															if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
																raw(self,"818",self._nickname,"%s Language :%s" % (chanid.channelname,chanid._prop.language))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._language(chanid,self,param[3])

												elif param[2].upper() == "ACCOUNT":
													if len(param) == 3:
														if self._nickname.lower() in opers:
															if chanid._prop.account:
																raw(self,"818",self._nickname,"%s Account :%s!%s@%s (%s)" % (chanid.channelname,chanid._prop.account_name,chanid._prop.account_user,chanid._prop.account_hostmask,chanid._prop.account_address))
															else:
																raw(self,"818",self._nickname,"%s Account :%s" % (chanid.channelname,ServerName))

															raw(self,"819",self._nickname,chanid.channelname)
														else:
															raw(self,"908",self._nickname)
													else:
														raw(self,"908",self._nickname)
													
												elif param[2].upper() == "TOPIC":
													if len(param) == 3:
														if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
															if chanid._topic != "": 
																raw(self,"332",self._nickname,chanid.channelname,chanid._topic)
																raw(self,"333",self._nickname,chanid.channelname,chanid._topic_nick,chanid._topic_time)

															else: raw(self,"331",self._nickname,chanid.channelname)

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._topic(chanid,self,param[3],strdata.split(" ",3)[3][1:])

												elif param[2].upper() == "MEMBERKEY":
													if len(param) == 3:
														if self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
															raw(self,"818",self._nickname,"%s Memberkey :%s" % (chanid.channelname,chanid.MODE_key))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._memberkey(chanid,self,param[3])
													
												elif param[2].upper() == "HOSTKEY":
													if len(param) == 3:
														if chanid._prop.hostkey != "":
															if self._nickname.lower() in opers or self._nickname.lower() in chanid._owner:
																raw(self,"818",self._nickname,"%s Hostkey :%s" % (chanid.channelname,chanid._prop.hostkey))
																raw(self,"819",self._nickname,chanid.channelname)
															else:
																raw(self,"908",self._nickname)
																pass
													else:
														chanid._prop._hostkey(chanid,self,param[3])

												elif param[2].upper() == "OWNERKEY":
													if len(param) == 3:	
														if chanid._prop.ownerkey != "":
															if self._nickname.lower() in opers or self._nickname.lower() in chanid._owner:
																raw(self,"818",self._nickname,"%s Ownerkey :%s" % (chanid.channelname,chanid._prop.ownerkey))
																raw(self,"819",self._nickname,chanid.channelname)														
															else:
																raw(self,"908",self._nickname)
																pass
													else:
														chanid._prop._ownerkey(chanid,self,param[3])
												
												elif param[2].upper() == "REGISTERED":
													if len(param) == 3:
														if self._nickname.lower() in opers:
															raw(self,"818",self._nickname,"%s Registered :%s" % (chanid.channelname,chanid._prop.registered))
														else:
															raw(self,"908",self._nickname)
													else:
														raw(self,"908",self._nickname)
												
												elif param[2].upper() == "NAME":
													if len(param) == 3:
														if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
															raw(self,"818",self._nickname,"%s Name :%s" % (chanid.channelname,chanid.channelname))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._name(chanid,self,param[3])

												elif param[2].upper() == "RESET":
													if len(param) == 3:
														if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
															raw(self,"818",self._nickname,"%s Reset :%d" % (chanid.channelname,chanid._prop.reset))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._reset(chanid,self,param[3])

												elif param[2].upper() == "OID":
													if len(param) == 3:
														if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
															raw(self,"818",self._nickname,"%s OID :0" % (chanid.channelname))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														raw(self,"908",self._nickname)

												elif param[2].upper() == "CREATION":
													if len(param) == 3:
														if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
															raw(self,"818",self._nickname,"%s Creation :%s" % (chanid.channelname,chanid._prop.creation))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														raw(self,"908",self._nickname)
													
												elif param[2].upper() == "ONJOIN":
													if len(param) == 3:
														if chanid._prop.onjoin != "":
															if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
																raw(self,"818",self._nickname,"%s Onjoin :%s" % (chanid.channelname,chanid._prop.onjoin))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._onmessage(chanid,self,param[3],strdata.split(" ",3)[3],"ONJOIN")

												elif param[2].upper() == "ONPART":
													if len(param) == 3:
														if chanid._prop.onpart != "":
															if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
																raw(self,"818",self._nickname,"%s Onpart :%s" % (chanid.channelname,chanid._prop.onpart))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														chanid._prop._onmessage(chanid,self,param[3],strdata.split(" ",3)[3],"ONPART")

												elif param[2].upper() == "PICS":
													if len(param) == 3:
														if isSecret(chanid,"private") == False or self._nickname.lower() in opers or self._nickname.lower() in chanid._users:
															raw(self,"818",self._nickname,"%s PICS :0" % (chanid.channelname))

														raw(self,"819",self._nickname,chanid.channelname)
													else:
														raw(self,"908",self._nickname)	

												else:
													raw(self,"905",self._nickname,chanid.channelname)
											else:
												raw(self,"403",self._nickname,param[1])
										else:
											raw(self,"461",self._nickname,param[0])


									elif param[0] == "IDENTIFY":
										if chanid:
											okey = chanid._prop.ownerkey
											if self._nickname.lower() in chanid._users:
												isop = False
												isowner = False
												if okey == param[2]:
													if self._nickname.lower() not in chanid._owner: chanid._owner.append(self._nickname.lower())
													if self._nickname.lower() in chanid._op:
														chanid._op.remove(self._nickname.lower())
														isop = True

													for each in chanid._users:
														cid = nicknames[each]
														if isop:
															cid.send(":%s!%s@%s MODE %s -o %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))														

														cid.send(":%s!%s@%s MODE %s +q %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))

												elif chanid._prop.hostkey == param[2]:
													if self._nickname.lower() not in chanid._op: chanid._op.append(self._nickname.lower())
													if self._nickname.lower() in chanid._owner: 
														chanid._owner.remove(self._nickname.lower())
														isowner = True

													for each in chanid._users:
														cid = nicknames[each]
														if isowner:
															cid.send(":%s!%s@%s MODE %s -q %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))

														cid.send(":%s!%s@%s MODE %s +o %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))
												
												else:
													raw(self,"908",self._nickname)
											else:
												raw(self,"442",self._nickname,chanid.channelname)
										else:
											raw(self,"403",self._nickname,param[1])

									elif param[0] == "AWAY":  # note : add to WHO, send to all on channel once
										try:
											if len(param) == 1:
												raw(self,"305",self._nickname)
												self._away = ""
												for allservers in linkedServers: allservers.sendUserAway(self._nickname,self._away)

											else:
												if strdata.split(" ",1)[1].__len__() > 128:
													raw(self,"906",self._nickname,param[0])
												else:
													self._away = param[1]
													if self._away[0] == ":": self._away = strdata.split(" ",1)[1][1:]
													raw(self,"306",self._nickname)
													for allservers in linkedServers: allservers.sendUserAway(self._nickname,self._away)

											#sendto = []
											#for each in self._channels:
											#	chan = channels[each.lower()]
											#	i = 0
											#	for copyn in chan._users:
											#		if copyn in nicknames:
											#			nick = nicknames[copyn]
											#			if self._nickname.lower() not in chan._watch:
											#				if nick not in sendto and nick._nickname.lower() != self._nickname.lower():
											#					if chan.MODE_auditorium == False or isOp(nick._nickname,chan.channelname) or isOp(self._nickname,chan.channelname):
											#						sendto.append(nick)
											#						if self._away == "": 
											#							raw(nick,"821",self)
											#						else:
											#							raw(nick,"822",self)
											  #
												#chan.updateuser(self._nickname,temp_nick)

		#									sendto = []

										except:
											pass
										

									elif param[0] == "KICK":
										if chanid:
											if self._nickname.lower() in chanid._users:
												iloop = 0

												if len(param) > 3: 				  
													kickmsg = param[3]
													if kickmsg[0] == ":":
														kickmsg = strdata.split(" ",3)[3][1:]
												else: 
													kickmsg = ""

												while iloop < len(param[2].split(",")):
													_kicknick = param[2].split(",")[iloop].lower()

													if _kicknick in nicknames:
														if _kicknick in chanid._users:

															if len(kickmsg) < 128: 
																cid = nicknames[_kicknick]

																if cid._nickname.lower() in opers and self._nickname.lower() not in opers:
																	raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")
																elif cid._nickname.lower() in opers and self._nickname.lower() in opers:
																	opid = opers[self._nickname.lower()]
																	sopid = opers[cid._nickname.lower()]
																	if opid.operlevel >= sopid.operlevel:
																		chanid.kick(self,cid._nickname,kickmsg)
																	else:
																		raw(self,"481",self._nickname,"Permission Denied - Insufficient oper priviledges")
																	#opers can kick other opers but they have to be equal levels or higher
																else:
																	if self._nickname.lower() in chanid._op:
																		if cid._nickname.lower() in chanid._owner or chanid.MODE_ownerkick:
																			raw(self,"485",self._nickname,chanid.channelname)
																		else:
																			chanid.kick(self,cid._nickname,kickmsg)

																	elif self._nickname.lower() in chanid._owner:
																		chanid.kick(self,cid._nickname,kickmsg)
																	else:
																		if cid._nickname.lower() in chanid._owner:
																			raw(self,"485",self._nickname,chanid.channelname)
																		else:
																			raw(self,"482",self._nickname,chanid.channelname)
															else:
																raw(self,"906",self._nickname,chanid.channelname)
														else:
															raw(self,"441",self._nickname,chanid.channelname)
													else:
														raw(self,"401",self._nickname,param[2])

													iloop+=1
											else:
												raw(self,"442",self._nickname,chanid.channelname)
										else:
											raw(self,"403",self._nickname,param[1])

									elif param[0] == "CREATE":
										_sleep = "%.4f" % (random()/9)

										if param[1].lower() in channels:
											raw(self,"705",self._nickname,param[1])
										else:
											if len(self._channels) >= myint(MaxChannelsPerUser):
												raw(self,"405",self._nickname,param[1])
											else:
												if len(channels) >= myint(MaxChannels):
													raw(self,"710",self._nickname)
												else:
													if len(param) == 2: creationmodes = "0"
													else: creationmodes = strdata.split(" ",2)[2]

													if self._nickname.lower() in opers:
														creationmodes = creationmodes.replace("r","").replace("e","")
													else:
														creationmodes = creationmodes.replace("r","").replace("N","").replace("A","").replace("a","").replace("d","").replace("e","")

													
													if param[1].lower() not in createmute:
														createmute[param[1].lower()] = self
														chanclass = Channel(param[1],self._nickname,creationmodes) #create
														if chanclass.channelname != "":
															channels[param[1].lower()] = chanclass
														
														del createmute[param[1].lower()]
													else:
														raw(self,"705",self._nickname,param[1])

									elif param[0] == "JOIN": 
										_sleep = "%.4f" % (random()/9)
										time.sleep(float(_sleep))
										iloop = 0
										while iloop < len(param[1].split(",")):
											if len(self._channels) >= myint(MaxChannelsPerUser):
												raw(self,"405",self._nickname,param[1].split(",")[iloop])
											else:

												chanclass = getChannelOBJ(param[1].split(",")[iloop].lower())
												if chanclass:
													if chanclass.MODE_key != "":
														if len(param) > 2:
															if param[2] == chanclass.MODE_key:
																chanclass.join(self._nickname,param[2])
															elif param[2] == chanclass._prop.ownerkey:
																if self._nickname.lower() not in chanclass._owner: 
																	if self._nickname.lower() not in chanclass._users: chanclass._owner.append(self._nickname.lower())

																chanclass.join(self._nickname,param[2])
															
															elif param[2] == chanclass._prop.hostkey:
																if self._nickname.lower() not in chanclass._op and self._nickname.lower() not in chanclass._users: chanclass._op.append(self._nickname.lower())
																chanclass.join(self._nickname,param[2])

															else:
																raw(self,"475",self._nickname,chanclass.channelname) # send error to  user
																if chanclass.MODE_knock:
																	for each in chanclass._users:	 # need to check for knock mode
																		cclientid = getUserOBJ(each)
																		cclientid.send(":%s!%s@%s KNOCK %s 475\r\n" % (self._nickname,self._username,self._hostmask,chanclass.channelname))

														elif self._nickname.lower() in opers:
															chanclass.join(self._nickname)

														else:
															raw(self,"475",self._nickname,chanclass.channelname) # send error to  user
															if chanclass.MODE_knock:
																for each in chanclass._users:	 # need to check for knock mode
																	cclientid = getUserOBJ(each)
																	cclientid.send(":%s!%s@%s KNOCK %s 475\r\n" % (self._nickname,self._username,self._hostmask,chanclass.channelname))
													elif len(param) > 2:
														if param[2] == chanclass._prop.ownerkey:
															if self._nickname.lower() not in chanclass._owner and self._nickname.lower() not in chanclass._users: chanclass._owner.append(self._nickname.lower())

														elif param[2] == chanclass._prop.hostkey:
															if self._nickname.lower() not in chanclass._op and self._nickname.lower() not in chanclass._users: chanclass._op.append(self._nickname.lower())
														
														chanclass.join(self._nickname,param[2])
													else:
														chanclass.join(self._nickname)
												else:
													if len(channels) >= myint(MaxChannels):
														raw(self,"710",self._nickname)

													elif ChanLockDown == 1:
														raw(self,"702",self._nickname)
													else:
														
														if param[1].lower() not in createmute:
															createmute[param[1].lower()] = self
															chanclass = Channel(param[1].split(",")[iloop],self._nickname) #create
															if chanclass.channelname != "":
																channels[param[1].split(",")[iloop].lower()] = chanclass
															
															del createmute[param[1].lower()]
														else:
															time.sleep(0.1)
															chanclass = getChannelOBJ(param[1].split(",")[iloop].lower())
															if chanclass:
																chanclass.join(self._nickname)
											iloop+=1

									elif param[0] == "FINDS":
										if chanid:
											raw(self,"613",self._nickname,chanid.channelname,"")
										else:
											raw(self,"702",self._nickname,param[1])

									elif param[0] == "ISON":
										ison_nicknames = ""
										iloop = 1
										while iloop < len(strdata.split(" ")):

											t_nick = getUserOBJ(strdata.split(" ")[iloop].lower())
											if t_nick:
												ison_nicknames+=" " + t_nick._nickname
										
											iloop+=1

										raw(self,"303",self._nickname,ison_nicknames[1:])

									elif param[0] == "USERHOST" or param[0] == "USERIP":
										iloop = 1
										while iloop < len(strdata.split(" ")):
											t_nick = strdata.split(" ")[iloop].lower()
											if self._nickname.lower() == t_nick:
												raw(self,"302",self._nickname,self,True)	
											else:
												cid = getUserOBJ(t_nick)
												if cid:
													boolShowIP = False
													if opid:
														topid = 0
														if t_nick in opers:
															_topid = opers[t_nick]
															topid = _topid.operlevel

														if opid.operlevel > topid: boolShowIP = True

													raw(self,"302",self._nickname,nicknames[t_nick],boolShowIP)
												else:
													self.send(":" + ServerName + " 302 " + self._nickname + " :\r\n")

											iloop+=1
												

									elif param[0] == "CREDITS":
										raw(self,"955",self._nickname)

									elif param[0] == "TIME":
										raw(self,"391",self._nickname)

									elif param[0] == "INFO":
										raw(self,"371",self._nickname)
										raw(self,"374",self._nickname)
							
									elif param[0] == "GENPASS":
										secPass = ""
										while len(secPass) < 64:
											c = 33
											print len(secPass)
											while c > 32:
												c = int(random()*255)
												secPass += chr(c)
												break

										mkshapass = sha.new()
										mkshapass.update(secPass)

										self.send(":" + ServerName + " NOTICE GENPASS :*** Your securely generated password is: %s\r\n" % (mkshapass.hexdigest()))

									elif param[0] == "WHO":
										_who = param[1].lower()
										if _who[0] == "#" or _who[0] == "%" or _who[0] == "&":
											if _who in channels:
												chanid = channels[_who]
												if isSecret(chanid,"private","hidden") == False or self._nickname.lower() in chanid._users or self._nickname.lower() in opers:
													for each in chanid._users:
														_whouser = nicknames[each]
														whostring = Whouser(_whouser,chanid.channelname.lower(),self)
														if whostring != "":
															raw(self,"352",self._nickname,whostring)
										
										else:
											_whouser = getUserOBJ(_who)
											if _whouser:
												if _whouser._MODE_invisible == False or self._nickname.lower() in opers or InChannel(self,_whouser) or self == _whouser:
													whostring = Whouser(_whouser,"",self)
													if whostring != "":
														raw(self,"352",self._nickname,whostring)
											
											else:
												useIP = True
												if self._nickname.lower() in opers: useIP = False
												who_count = 0
												tempAccessObj = Access()
												param[1] = tempAccessObj.CreateMaskString(_who)
												for each in nicknames:
													nickid = nicknames[each]
													if tempAccessObj.MatchAccess(param[1],nickid,useIP):
														who_count += 1
														if who_count == 20 and self._nickname.lower() not in opers:
															raw(self,"416",self._nickname,"WHO")
															break

														if nickid._MODE_invisible == False or self._nickname.lower() in opers or InChannel(self,nickid) or self == nickid:
															whostring = Whouser(nickid,"",self)
															if whostring != "": raw(self,"352",self._nickname,whostring)

										raw(self,"315",self._nickname,param[1])

									elif param[0] == "KILLMASK":
										if opid:
											if opid.operlevel >= 3:
												msg = param[2]
												if msg[0] == ":": msg = strdata.split(" ",2)[2][1:]
												kill_count = 0
												tempAccessObj = Access()
												param[1] = tempAccessObj.CreateMaskString(param[1].lower())
												for each in nicknames:
													nickid = nicknames[each]
													if tempAccessObj.MatchAccess(param[1],nickid):
														kill_count += 1
														if kill_count == 5:
															raw(self,"416",self._nickname,"KILLMASK")
															break
														else:
															if nickid._nickname.lower() in opers:
																opnickid = opers[nickid._nickname.lower()]
																if opid.operlevel < opnickid.operlevel:
																	kill_count -= 1
																	continue

															if nickid == self:
																self.send(":" + ServerName + " NOTICE KILLMASK :*** You cannot kill yourself using KILLMASK\r\n")
																kill_count -=1
																continue

															nickid.quitmsg = " by " + self._nickname
															SendComChan(nickid._channels,self,nickid,":%s!%s@%s KILL %s :%s\r\n" % (self._nickname,self._username,self._hostmask,nickid._nickname,msg),msg)
															nickid.quittype = -1
															nickid.die = True

												
												sendAdminOpers(":" + ServerName + " NOTICE KILLMASK :*** " + self._nickname + " has just used KILLMASK to kill " + str(kill_count) + " connections with parameter \"" + param[1] + "\"\r\n")

											else:
												raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
										else:
											raw(self,"481",self._nickname,"Permission Denied - You're not a System Operator")

										

									elif param[0] == "LINKS":
										for eachserver in linkedServers:
											raw(self,"364",self._nickname,eachserver.link._serverName,eachserver.link._info)
										
										raw(self,"365",self._nickname)

									elif param[0] == "LOLLER":
										pass

									elif param[0] == "WHOIS":
										iloop = 0
										while iloop < len(param[1].split(",")):
											_whois = param[1].split(",")[iloop]
											_whoisuser = getUserOBJ(_whois.lower())
											if _whoisuser:
												if _whoisuser._MODE_invisible == False or self._nickname.lower() in opers or InChannel(self,_whoisuser) or self == _whoisuser:
													raw(self,"311",self._nickname,_whoisuser)
													raw(self,"378",self._nickname,_whoisuser)
													raw(self,"319",self._nickname,_whoisuser)
													if _whoisuser._MODE_register: raw(self,"307",self._nickname,_whoisuser)
													if "z" in _whoisuser._MODE_: raw(self,"316",self._nickname,_whoisuser._nickname)
													raw(self,"313",self._nickname,_whoisuser)
													raw(self,"320",self._nickname,_whoisuser)
													raw(self,"312",self._nickname,_whoisuser)
													if _whoisuser._away != "": raw(self,"301",self._nickname,_whoisuser,_whoisuser._away)
													raw(self,"317",self._nickname,_whoisuser)

											elif _whois.lower() == "nickserv":
												self.send(":%s!%s@%s %s %s :\x02pyRCX nickname services\x02 (currently %d registered users)\r\n:%s!%s@%s %s %s :Type \x1F/nickserv HELP\x1F for more information\r\n" % ("NickServ","NickServ",NetworkName,"NOTICE",self._nickname,len(Nickserv),"NickServ","NickServ",NetworkName,"NOTICE",self._nickname))

											else:
												raw(self,"401",self._nickname,_whois)

											iloop+=1

										raw(self,"318",self._nickname,param[1])

									elif param[0] == "ADMIN":
										raw(self,"258",self._nickname)
										raw(self,"259",self._nickname)

									elif param[0] == "VERSION":
										raw(self,"256",self._nickname)
										raw(self,"257",self._nickname)

									elif param[0] == "LUSERS":
										self._sendlusers()

									elif param[0] == "MOTD":
										try:
											self._sendmotd("./motd.conf")
										except:
											pass

									elif param[0] == "DATA" or param[0] == "REPLY" or param[0] == "REQUEST":
										if self._MODE_gag:
											raw(self,"908",self._nickname)
										else:
											recips = []
											tag = param[2]
											data = param[3]
											if data[0] == ":": data = strdata.split(" ",3)[3][1:]
											if data == "":
												raw(self,"412",self._nickname,param[0])
											else:
												iloop = 0
												while iloop < len(param[1].split(",")):
													_recipient = param[1].split(",")[iloop].lower()
													if _recipient.lower() not in recips:
														recips.append(_recipient.lower())
														if _recipient in nicknames:
															nick = nicknames[_recipient]
															if self.selfaccess(nick):
																nick.send(":%s!%s@%s %s %s %s :%s\r\n" % (self._nickname,self._username,self._hostmask,param[0],_recipient,tag,data))

														elif _recipient in channels:
															chan = channels[_recipient]
															if chan.isBanned(self) and chan.MODE_gagonban:
																raw(self,"404",self._nickname,_recipient,"Cannot send to channel whilst banned")
															else:
																if self._nickname.lower() in chan._users or chan.MODE_externalmessages == False:
																	if chan.MODE_moderated == False or isOp(self._nickname.lower(),chan.channelname.lower()) or self._nickname.lower() in chan._voice:
																		for each in chan._users:
																			cid = nicknames[each.lower()]
																			if cid != self:  # x  ! x  @ x DATA target 
																				cid.send(":%s!%s@%s %s %s %s :%s\r\n" % (self._nickname,self._username,self._hostmask,param[0],_recipient,tag,data))
																else:
																	raw(self,"404",self._nickname,_recipient,"Cannot send to channel")
																
														else:
															raw(self,"401",self._nickname,_recipient)
														
													iloop+=1

									elif param[0] == "NICKSERV" or param[0] == "NS": #ns register <email> <password>
										Nickserv_function(self,param)

									else:
										if self._nickname == "":
											raw(self,"421","*",param[0])
										else:
											raw(self,"421",self._nickname,param[0])
							
								else:
									raw(self,"451",self._nickname)

						except IndexError:
							raw(self,"461",self._nickname,param[0])

						#except:
						#	tuError = sys.exc_info()
						#	self._reportError(tuError)
				
						
		try:
			print "*** Connection closed from '",self.details[0],"'",self._nickname,"left the server"
			quit = ""
			if self.quittype != 9 and self.quittype != 10:
				for allservers in linkedServers: allservers.sendUserDisconnect(self)


			if self.quittype == 0:
				quit = "Connection reset by peer"
			elif self.quittype == 1:
				quit = "Client exited"
			elif self.quittype == 2:
				quit = "Quit"
			elif self.quittype == 3:
				quit = "Ping timeout"
			elif self.quittype == 4:
				quit = "Flooding"
			elif self.quittype == 5:
				quit = "Nickname collision on server link"
			elif self.quittype == -1:
				quit = "Killed" + self.quitmsg

			if self.quittype != -1:

				sendto = []
				for each in copy(self._channels):
					try:
						chan = channels[each.lower()]
						temp = dict(chan._users)
						for n in temp:
							if n in nicknames:
								nick = nicknames[n.lower()]
								if nick not in sendto and nick._nickname.lower() != self._nickname.lower():
									if self._nickname.lower() not in chan._watch:
										if chan.MODE_auditorium == False or isOp(nick._nickname,chan.channelname) or isOp(self._nickname,chan.channelname):
											sendto.append(nick)
											try:	     # keep this here, some clients exit too fast
												if self.quittype == 0:
													nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " QUIT :Connection reset by peer\r\n")
												elif self.quittype == 1:
													nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " QUIT :Client exited\r\n")
												elif self.quittype == 2:
													if self.quitmsg == "":
														nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " QUIT :Quit\r\n")
													else:
														nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " QUIT :Quit: " + self.quitmsg + "\r\n")

												elif self.quittype == 3:
													nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " QUIT :Ping timeout\r\n")
													
												elif self.quittype == 4:
													nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " QUIT :Flooding\r\n")

												elif self.quittype == 5:
													nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " QUIT :Nickname collision on server link\r\n")

											except:
												pass
						del temp
					except:
						print "uh oh bug"

				del sendto

			temp_opers = dict(opers)
			for each in temp_opers:
				opid = temp_opers[each.lower()]
				if opid.watchserver or opid.watchbans:
					cid = nicknames[each.lower()]
					try:
						if self.quittype == 9:
							if opid.watchbans:
								cid.send(":%s NOTICE %s :*** Notice -- User tried connecting but is banned (%s!%s@%s) [%s] \r\n" % (ServerName,cid._nickname,self._nickname,self._username,self._hostmask,self.details[0]))
						else:
							if self._nickname != "" and opid.watchserver and quit != "":
								cid.send(":%s NOTICE %s :*** Notice -- User Disconnected (%s!%s@%s) [%s] (%s)\r\n" % (ServerName,cid._nickname,self._nickname,self._username,self._hostmask,self.details[0],quit))
					except:
						pass

			del temp_opers

			# remove all existance of this user in channels

		except:
			tuError = sys.exc_info()
			print tuError

		for each in copy(self._channels):
			try:
				channels[each.lower()].quit(self._nickname)
			except:
				print "some channel error"

		if self in invisible: invisible.remove(self)
		if self._nickname.lower() in opers: 
			opid = opers[self._nickname.lower()]
			opid.usage = False
			del opers[self._nickname.lower()]

		if self._nickname.lower() in nickmute: del nickmute[self._nickname.lower()] # log on affirmed, now nicknames can take over
		if self._nickname.lower() in nicknames: del nicknames[self._nickname.lower()]

		if self in connections: connections.remove(self)
		if self in unknownConnections: unknownConnections.remove(self)
		if self in temp_noopers: temp_noopers.remove(self)
		if self in opersecret: opersecret.remove(self)
		try:
			del self._watch,self._access
			self.close()
		except:
			pass

		del self


def Oper_function(self,param):
	if self._nickname.lower() in opers:
		raw(self,"381",self._nickname,"You are already logged in")
	else:
		if str(len(param)) != str(3):
			raw(self,"461",self._nickname,param[0])
		else:
			if globals()["Noop"]:
				self.send(":" + ServerName + " NOTICE SERVER :*** OPER has been disabled\r\n")
			else:
				_login = False
				for k in operlines:
					
					if k.username == param[1] and k.password == param[2]:
						if k.usage:
							_login = "inuse"
						else:
							# opers dictionary file [ nickname ] 
							opers[self._nickname.lower()] = k
							_login = True

				if _login == True:
					opid = opers[self._nickname.lower()]
					opid.guide = False
					opid.hidden = False
					opid.usage = True
					opid.watchserver = False
					opid.watchbans = False
					if self._MODE_register == False: #oper does not need to display whether he/she is oper
						self._username  = self._username[1:]

					if "s" not in opid.flags:
						self._hostmask = NetworkName
						self._username = opid.username
					
					self._sendmotd("./" + opid.filename)
			
					self.send(":%s!%s@%s MODE %s +%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,opid.flags))

					if "A" in opid.flags:
						if "A" not in self._MODE_: self._MODE_ = self._MODE_ + "aAoO"
						opid.operlevel = 4
						raw(self,"381",self._nickname,"You are now a Network Administrator")
					elif "O" in opid.flags:
						if "O" not in self._MODE_: self._MODE_ = self._MODE_ + "aoO"
						opid.operlevel = 3
						raw(self,"381",self._nickname,"You are now an Administrator")
					elif "a" in opid.flags:
						if "a" not in self._MODE_: self._MODE_ = self._MODE_ + "ao"
						opid.operlevel = 2
						raw(self,"381",self._nickname,"You are now a System Chat Manager")
					elif "o" in opid.flags:
						if "o" not in self._MODE_: self._MODE_ = self._MODE_ + "o"
						opid.operlevel = 1
						raw(self,"381",self._nickname,"You are now a System Operator")

					if "w" in opid.flags: opid.watchserver = True
					if "g" in opid.flags: opid.guide = True
					if "b" in opid.flags: opid.watchbans = True
					if "n" in opid.flags: opid.watchnickserv = True
					if "s" in opid.flags:
						opid.hidden = True
						return

					sendWatchOpers("Notice -- Oper signed in (%s!%s@%s) [%s] \r\n" % (self._nickname,self._username,self._hostmask,self.details[0]))

					for allservers in linkedServers:
						allservers.sendUserOper(self._nickname,dumps(opid))
						allservers.sendHostIdentNameChange(self._nickname,self._username,self._hostmask,0)
						allservers.sendUserMode(self._nickname,opid.flags.replace("o","").replace("a","").replace("O","").replace("A",""))
				

				elif _login == "inuse":
					raw(self,"481",self._nickname,"Permission Denied - You're login is already in use")
				else:
					sendWatchOpers("Notice -- Oper attempt failed (%s!%s@%s) [%s] \r\n" % (self._nickname,self._username,self._hostmask,self.details[0]))
					
					raw(self,"491",self._nickname,"No O-lines for your host")

def Nick_function(self,param):

	if self._validate(param[1].replace(':','')) and _filter(self,param[1].replace(':',''),"nick"):

		if int((GetEpochTime() - self._nickflood)*1000) <= 10000:
			self._nickamount += 1
		else:
			self._nickamount = 0

		self._nickflood = GetEpochTime()
		if self._nickamount == NickfloodAmount: # nick changes
			self._nicklock = int(GetEpochTime() + NickfloodWait)
			self._nickamount = 0

		if self._nicklock == 0 or int(GetEpochTime()) >= self._nicklock or NickfloodAmount == 0 or NickfloodWait == 0:
			if self._nicklock != 0: 
				self._nicklock = 0
				self._nickamount = 0

			found_deny = False
			found_grant = False

			schannels = copy(self._channels)

			for gagcheck in schannels:
				gagchan = channels[gagcheck.lower()]
				if gagchan.MODE_gagonban and self._nickname.lower() in gagchan._users:
					for each in gagchan.ChannelAccess:
						ret = Access().MatchAccess(each._mask,self)
						if ret == 1:
							if each._level.upper() == "DENY":
								found_deny = True
							else:
								found_grant = True
								break
					
					if found_deny == True and found_grant == False:
						raw(self,"437",self._nickname,gagchan.channelname)
						return

			temp_nick = param[1].replace(':','')
			nickobj = getUserOBJ(temp_nick.lower())
			if nickobj:
				if nickobj == self:
					if temp_nick == self._nickname:
						pass
					else:
						self.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " NICK :" + temp_nick + "\r\n")
						
						for allservers in linkedServers: allservers.sendUserNick(self._nickname,temp_nick)

						sendto = []
						
						for each in schannels:
							chan = channels[each.lower()]
							copyn = dict(chan._users)
							for copyn in chan._users:
								nick = getUserOBJ(copyn)
								if nick:
									if self._nickname.lower() not in chan._watch:
										if nick not in sendto and nick._nickname.lower() != self._nickname.lower():
											if chan.MODE_auditorium == False or isOp(nick._nickname,chan.channelname) or isOp(self._nickname,chan.channelname):
												sendto.append(nick)
												nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " NICK :" + temp_nick + "\r\n")


							chan.updateuser(self._nickname,temp_nick)

						del sendto
						self._nickname = temp_nick
				else:
					raw(self,"433",self._nickname,param[1].replace(':',''))
			else:
				
				# start of nickname checks
				
				if self._nickname.lower() in nickmute:
					del nickmute[self._nickname.lower()] # remove last name from nickmute if not removed yet

				if temp_nick.lower() not in nickmute:
					nickmute[temp_nick.lower()] = self

					if self._nickname != "":
						self.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " NICK :" + temp_nick + "\r\n")
						for allservers in linkedServers: allservers.sendUserNick(self._nickname,temp_nick)

					sendto = []
					for each in schannels:
						chan = getChannelOBJ(each.lower())
						i = 0
						for copyn in chan._users:
							nick = getUserOBJ(copyn)
							if nick:
								if self._nickname.lower() not in chan._watch:
									if nick not in sendto and nick._nickname.lower() != self._nickname.lower():
										if chan.MODE_auditorium == False or isOp(nick._nickname,chan.channelname) or isOp(self._nickname,chan.channelname):
											sendto.append(nick)
											nick.send(":" + self._nickname + "!" + self._username + "@" + self._hostmask + " NICK :" + temp_nick + "\r\n")

						chan.updateuser(self._nickname,temp_nick)

					del sendto

					if self._nickname.lower() in opers:
						opers[temp_nick.lower()] = opers[self._nickname.lower()]
						del opers[self._nickname.lower()]

					if self._nickname.lower() in nicknames: del nicknames[self._nickname.lower()]

					temp_oldnick = self._nickname

					self._nickname = temp_nick
					

					if self._welcome == True:
						nicknames[self._nickname.lower()] = self #update entry from dictionary

					if self._logoncheck():
						self._sendwelcome()

					if self._nickname.lower() in nicknames:

						is_groupednick = False

						for groupnicks in Nickserv.values():
							if self._nickname.lower() in groupnicks._groupnick or self._nickname.lower() == groupnicks._nickname.lower():
								if temp_oldnick.lower() in groupnicks._groupnick or temp_oldnick.lower() == groupnicks._nickname.lower():
									if self._MODE_register:
										is_groupednick = True
										break


						if self._MODE_register and is_groupednick == False:
							self._MODE_register = False
							self._MODE_.replace("r","")
							for allservers in linkedServers: allservers.sendUserMode(self._nickname,"-r")
							self.send(":%s!%s@%s MODE %s -r\r\n" % ("NickServ","NickServ",NetworkName,self._nickname))
							if self._username[0] != PrefixChar and self._nickname.lower() not in opers: self._username = PrefixChar + self._username
					
						if temp_nick.lower() in Nickserv or is_groupednick:
							if self._MODE_register == False:
								self.send(":%s!%s@%s NOTICE %s :That nickname is owned by somebody else\r\n:%s!%s@%s NOTICE %s :If this is your nickname, you can identify with \x02/nickserv IDENTIFY \x1Fpassword\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,self._nickname,"NickServ","NickServ",NetworkName,self._nickname))

				else:
					raw(self,"433",self._nickname,temp_nick)
				## end of after nickname checks

		else:
			raw(self,"438",self._nickname)
	else:
		raw(self,"432",self._nickname,param[1].replace(':',''))

def Mode_function(self,param,strdata=""):
	if param[1][0] == "#" or param[1][0] == "%" or param[1][0] == "&": # is a channel
		schannels = copy(channels)
		if param[1].lower() in schannels:
			chan = schannels[param[1].lower()]
			if len(param) == 2:
				if isSecret(chan,"private") == False or self._nickname.lower() in chan._users or self._nickname.lower() in opers:
					raw(self,"324",self._nickname,chan.channelname,chan.GetChannelModes(self._nickname.lower()))
				else:
					self.send(":" + ServerName + " 324 " + self._nickname + " " + chan.channelname + " +\r\n")
			else:
				if self._nickname.lower() in chan._users:
					iloop = 0
					paramloop = 2
					param[2] = compilemodestr(param[2],True)
					SetMode = True
					Override = False
					if self._nickname.lower() in opers:
						opid = opers[self._nickname.lower()]
						if opid.operlevel >= 3: Override = True

					while iloop < len(param[2]):
						szModestr = ""
						if param[2][iloop] == "+": SetMode = True
						elif param[2][iloop] == "-": SetMode = False
						
						elif chan.MODE_nomodechanges and self._nickname.lower() not in opers and param[2][iloop] != "b" and param[2][iloop] != "q" and param[2][iloop] != "o" and param[2][iloop] != "v":
							raw(self,"908",self._nickname)

						elif chan.MODE_ownersetmode and self._nickname.lower() not in chan._owner and param[2][iloop] != "b":
							raw(self,"485",self._nickname,chan.channelname)

						elif param[2][iloop] == "b" or param[2][iloop] == "l" or param[2][iloop] == "k" or param[2][iloop] == "q" or param[2][iloop] == "o" or param[2][iloop] == "v":
							paramloop+=1 # now param[paramloop] is the parameter for each of the modes
							try:
								if self._nickname.lower() in chan._op or self._nickname.lower() in chan._owner or Override:
									if param[2][iloop] == "k":
										if SetMode:
											if len(param[paramloop]) <= 16:
												chan.MODE_key = str(param[paramloop])
												szModestr = ":%s!%s@%s MODE %s +k %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,param[paramloop])
											else:
												raw(self,"906",self._nickname,"MODE +%s" % (param[2][iloop]))
										else:
											chan.MODE_key = ""
											szModestr = ":%s!%s@%s MODE %s -k\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname)

										for each in chan._users:
											cclientid = nicknames[each]
											cclientid.send(szModestr)

									elif param[2][iloop] == "l":
										if SetMode:
											if myint(param[paramloop]) <= 65535 and myint(param[paramloop]) > 0:
												chan.MODE_limit = True
												chan.MODE_limitamount = str(myint(param[paramloop]))
												szModestr = ":%s!%s@%s MODE %s +l %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,param[paramloop])
											else:
												raw(self,"906",self._nickname,"MODE +%s" % (param[2][iloop]))
										else:
											chan.MODE_limit = False
											szModestr = ":%s!%s@%s MODE %s -l\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname)

										for each in chan._users:
											cclientid = nicknames[each]
											cclientid.send(szModestr)

									elif param[2][iloop] == "o":
										isowner=False
										if param[paramloop].lower() in nicknames:
											cid = nicknames[param[paramloop].lower()]
											if cid._nickname.lower() in chan._users:
												if self._nickname.lower() in chan._op and cid._nickname.lower() in chan._owner and cid != self:
													raw(self,"485",self._nickname,chan.channelname)
												else:	
													opid = 0
													copid = 0
													operok = True
													if cid._nickname.lower() in opers: copid = opers[cid._nickname.lower()]
													if self._nickname.lower() in opers: opid = opers[self._nickname.lower()]

													if copid != 0 and opid == 0:
														raw(self,"908",self._nickname)
													else:
														if copid != 0 and opid != 0:
															if opid >= copid: operok = True
															else: operok = False
														
														if operok:
															if chan.MODE_auditorium:
																for x in chan._users:
																	if x.lower() in chan._op: pass
																	elif x.lower() in chan._owner: pass
																	else:
																		nickid = nicknames[x]
																		if cid != nickid:
																			if isOp(cid._nickname,chan.channelname) == False and SetMode:
																				cid.send(":%s!%s@%s JOIN :%s\r\n" % (nickid._nickname,nickid._username,nickid._hostmask,chan.channelname))

																			elif isOp(cid._nickname,chan.channelname) and SetMode == False: # if opnick is op and they are deoping then
																				cid.send(":%s!%s@%s PART :%s\r\n" % (nickid._nickname,nickid._username,nickid._hostmask,chan.channelname))

																			if isOp(nickid._nickname,chan.channelname) == False and SetMode:
																				if isOp(cid._nickname,chan.channelname) == False:
																					nickid.send(":%s!%s@%s JOIN :%s\r\n" % (cid._nickname,cid._username,cid._hostmask,chan.channelname))

																			elif isOp(nickid._nickname,chan.channelname) == False and SetMode == False:
																				if isOp(cid._nickname,chan.channelname):
																					nickid.send(":%s!%s@%s PART :%s\r\n" % (cid._nickname,cid._username,cid._hostmask,chan.channelname))

															if cid._nickname.lower() in chan._owner: isowner = True

															for each in chan._users:
																cclientid = nicknames[each.lower()]
																#if chan.MODE_auditorium == False or isOp(cclientid._nickname,chan.channelname) or cid == cclientid:
																if chan.MODE_auditorium and SetMode == False and isOp(cclientid._nickname,chan.channelname) == False:
																	pass
																else:
																	if isowner and cclientid._IRCX:
																		cclientid.send(":%s!%s@%s MODE %s -q %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,cid._nickname))

																	cclientid.send(":%s!%s@%s MODE %s %so %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),cid._nickname))

															if isowner: chan._owner.remove(cid._nickname.lower())
															if SetMode:
																if cid._nickname.lower() not in chan._op: chan._op.append(cid._nickname.lower()) # channel now knows that cid is a channel operator
															else:	
																if cid._nickname.lower() in chan._op: chan._op.remove(cid._nickname.lower())

											else:
												raw(self,"441",self._nickname,chan.channelname)
										else:
											raw(self,"401",self._nickname,param[paramloop])

									elif param[2][iloop] == "v":
										if param[paramloop].lower() in nicknames:
											cid = nicknames[param[paramloop].lower()]
											if cid._nickname.lower() in chan._users:
												if self._nickname.lower() in chan._op and cid._nickname.lower() in chan._owner and SetMode == False:
													raw(self,"485",self._nickname,chan.channelname)
												else:
													if SetMode:
														if cid._nickname.lower() not in chan._voice: chan._voice.append(cid._nickname.lower()) # channel now knows that cid is a channel voice
													else:	
														if cid._nickname.lower() in chan._voice: chan._voice.remove(cid._nickname.lower())

													for each in chan._users:
														cclientid = nicknames[each.lower()]
														if chan.MODE_auditorium == False or isOp(cclientid._nickname,chan.channelname) or cclientid == cid:
															cclientid.send(":%s!%s@%s MODE %s %sv %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),cid._nickname))
											else:
												raw(self,"441",self._nickname,chan.channelname)	
										else:
											raw(self,"401",self._nickname,param[paramloop])

									elif param[2][iloop] == "q" and self._IRCX:
										if chan.MODE_noircx:
											raw(self,"997",self._nickname,chan.channelname,"MODE %sq" % (iif(SetMode,"+","-")))
										else:
											isop = False
											if self._nickname.lower() in chan._owner or Override:
												if param[paramloop].lower() in nicknames:
													cid = nicknames[param[paramloop].lower()]
													if cid._nickname.lower() in chan._users:
														opid = 0
														copid = 0
														operok = True
														if cid._nickname.lower() in opers: 
															copid = opers[cid._nickname.lower()]
															copid = copid.operlevel


														if self._nickname.lower() in opers:
															opid = opers[self._nickname.lower()]
															opid = opid.operlevel

														if copid != 0 and opid == 0:
															raw(self,"908",self._nickname)
														else:
															if copid != 0 and opid != 0:
																if opid >= copid: operok = True
																else:
																	operok = False
																	raw(self,"908",self._nickname)
																	
															if operok:
																if chan.MODE_auditorium:
																	for x in chan._users:
																		if x.lower() in chan._op: pass
																		elif x.lower() in chan._owner: pass
																		else:
																			nickid = nicknames[x]
																			if cid != nickid:
																				if isOp(cid._nickname,chan.channelname) == False and SetMode:
																					cid.send(":%s!%s@%s JOIN :%s\r\n" % (nickid._nickname,nickid._username,nickid._hostmask,chan.channelname))

																				elif isOp(cid._nickname,chan.channelname) and SetMode == False: # if opnick is op and they are deoping then
																					cid.send(":%s!%s@%s PART :%s\r\n" % (nickid._nickname,nickid._username,nickid._hostmask,chan.channelname))

																				if isOp(nickid._nickname,chan.channelname) == False and SetMode:
																					if isOp(cid._nickname,chan.channelname) == False:
																						nickid.send(":%s!%s@%s JOIN :%s\r\n" % (cid._nickname,cid._username,cid._hostmask,chan.channelname))

																				elif isOp(nickid._nickname,chan.channelname) == False and SetMode == False:
																					if isOp(cid._nickname,chan.channelname):
																						nickid.send(":%s!%s@%s PART :%s\r\n" % (cid._nickname,cid._username,cid._hostmask,chan.channelname))

																if cid._nickname.lower() in chan._op: isop = True

																for each in chan._users:
																	cclientid = nicknames[each]
																	if chan.MODE_auditorium and SetMode == False and isOp(cclientid._nickname,chan.channelname) == False:
																		pass
																	else:	
																		if isop and cclientid._IRCX:
																			cclientid.send(":%s!%s@%s MODE %s -o %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,cid._nickname))
																				
																		if cclientid._IRCX:
																			cclientid.send(":%s!%s@%s MODE %s %sq %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),cid._nickname))
																		else:
																			cclientid.send(":%s!%s@%s MODE %s %so %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),cid._nickname))

																if isop: chan._op.remove(cid._nickname.lower())
																if SetMode:
																	if cid._nickname.lower() not in chan._owner: chan._owner.append(cid._nickname.lower()) # channel now knows that cid is a channel operator
																else:	
																	if cid._nickname.lower() in chan._owner: 
																		chan._owner.remove(cid._nickname.lower())

																	if cid._nickname.lower() in chan._op: chan._op.remove(cid._nickname.lower())
													else:
														raw(self,"441",self._nickname,chan.channelname)
												else:
													raw(self,"401",self._nickname,param[paramloop])
											else:
												raw(self,"485",self._nickname,chan.channelname)

									elif param[2][iloop] == "b":
										_rec = ""
										if SetMode:
											_mask = _Access.CreateMaskString(param[paramloop].lower())
											if _mask == -1: raw(self,"906",self._nickname,param[paramloop].lower())
											elif _mask == -2: raw(self,"909",self._nickname)
											else:
												tag,exp = "",0
												_rec = _Access.AddRecord(self,chan.channelname,"DENY",_mask,exp,tag)
												if _rec == 1:
													stringinf = "%s %s %s %d %s %s" % (chan.channelname,"DENY",_mask,exp,self._hostmask,tag)
													raw(self,"801",self._nickname,stringinf)

												elif _rec == -1:
													raw(self,"914",self._nickname,chan.channelname)

												elif _rec == -2:
													raw(self,"913",self._nickname,chan.channelname)
												else:
													pass
										else:
											_mask = _Access.CreateMaskString(param[paramloop].lower())
											if _mask == -1: raw(self,"906",self._nickname,param[paramloop].lower())
											elif _mask == -2: raw(self,"909",self._nickname)
											else:
												_rec = _Access.DelRecord(self,chan.channelname,"DENY",_mask)
												if _rec == 1:
													stringinf = "%s %s %s" % (chan.channelname,"DENY",_mask)
													raw(self,"802",self._nickname,stringinf)

												elif _rec == -1:
													raw(self,"915",self._nickname,chan.channelname)
												elif _rec == -2:
													raw(self,"913",self._nickname,chan.channelname)
										if _rec == 1:
											for each in chan._users:
												cclientid = nicknames[each]
												cclientid.send(":%s!%s@%s MODE %s %sb %s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),_mask))

								else:
									raw(self,"482",self._nickname,chan.channelname)

							except IndexError:
								if param[2][iloop] == "b" and SetMode:
									for each in chan.ChannelAccess:
										if each._level == "DENY":
											if each._deleteafterexpire == False:
												exp = 0
											else:
												exp = (each._expires - int(GetEpochTime())) / 60
												if exp < 1: exp = 0

											raw(self,"367",self._nickname,chan.channelname,each._mask,each._setby,str(each._setat))

									raw(self,"368",self._nickname,chan.channelname)
								else:
									raw(self,"461",self._nickname,"MODE %s%s" % (iif(SetMode,"+","-"),param[2][iloop]))




						elif param[2][iloop] == "X":
							if chan.MODE_noircx:
								raw(self,"997",self._nickname,chan.channelname,"MODE %sX" % (iif(SetMode,"+","-")))
							else:
								if self._nickname.lower() in chan._owner or Override:
									if SetMode:
										chan.MODE_ownersetaccess = True
									else:
										chan.MODE_ownersetaccess = False

									for each in chan._users:
										cclientid = nicknames[each]
										cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
								else:
									raw(self,"485",self._nickname,chan.channelname)

						elif param[2][iloop] == "Z":
							raw(self,"472",self._nickname,"Z")

						elif param[2][iloop] == "M":
							if chan.MODE_noircx:
								raw(self,"997",self._nickname,chan.channelname,"MODE %sM" % (iif(SetMode,"+","-")))
							else:
								if self._nickname.lower() in chan._owner or Override:
									if SetMode:
										chan.MODE_ownersetmode = True
									else:
										chan.MODE_ownersetmode = False

									for each in chan._users:
										cclientid = nicknames[each]
										cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
								else:
									raw(self,"485",self._nickname,chan.channelname)

						elif param[2][iloop] == "P":
							if chan.MODE_noircx:
								raw(self,"997",self._nickname,chan.channelname,"MODE %sP" % (iif(SetMode,"+","-")))
							else:
								if self._nickname.lower() in chan._owner or Override:
									if SetMode:
										chan.MODE_ownersetprop = True
									else:
										chan.MODE_ownersetprop = False

									for each in chan._users:
										cclientid = nicknames[each]
										cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
								else:
									raw(self,"485",self._nickname,chan.channelname)

						elif param[2][iloop] == "T":
							if chan.MODE_noircx:
								raw(self,"997",self._nickname,chan.channelname,"MODE %sT" % (iif(SetMode,"+","-")))
							else:
								if self._nickname.lower() in chan._owner or Override:
									unsetother = ""
									if SetMode:
										if chan.MODE_optopic:
											unsetother = "-t"
											chan.MODE_optopic = False
										
										chan.MODE_ownertopic = True
									else:
										chan.MODE_ownertopic = False

									for each in chan._users:
										cclientid = nicknames[each]
										cclientid.send(":%s!%s@%s MODE %s %s%s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,unsetother,iif(SetMode,"+","-"),param[2][iloop]))
								else:
									raw(self,"485",self._nickname,chan.channelname)

						elif param[2][iloop] == "r" or param[2][iloop] == "x" or param[2][iloop] == "S" or param[2][iloop] == "e":
							raw(self,"468",self._nickname,chan.channelname)
								
						elif param[2][iloop] == "Q":
							if chan.MODE_noircx:
								raw(self,"997",self._nickname,chan.channelname,"MODE %sQ" % (iif(SetMode,"+","-")))
							else:
								if self._nickname.lower() in chan._owner or Override:
									if SetMode:
										chan.MODE_ownerkick = True
									else:
										chan.MODE_ownerkick = False

									for each in chan._users:
										cclientid = nicknames[each]
										cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
								else:
									raw(self,"485",self._nickname,chan.channelname)	

						elif param[2][iloop] == "d":
							if self._nickname.lower() in opers:
								if SetMode:
									chan.MODE_createclone = True
								else:
									chan.MODE_createclone = False

								for each in chan._users:
									cclientid = nicknames[each]
									cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
							else:
								raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

						elif param[2][iloop] == "a":
							if self._nickname.lower() in opers:
								
								if SetMode:
									chan.MODE_authenticatedclients = True
								else:
									chan.MODE_authenticatedclients = False

								for each in chan._users:
									cclientid = nicknames[each]
									cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
							else:
								raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

						elif param[2][iloop] == "N": # Service channel
							if self._nickname.lower() in opers:
								
								if SetMode:
									chan.MODE_servicechan = True
								else:
									chan.MODE_servicechan = False

								for each in chan._users:
									cclientid = nicknames[each]
									cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
							else:
								raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")
				
						elif param[2][iloop] == "A": # Service channel
							if self._nickname.lower() in opers:
								opid = opers[self._nickname.lower()]
								if opid.operlevel >= 3:
									if SetMode:
										chan.MODE_Adminonly = True
									else:
										chan.MODE_Adminonly = False

									for each in chan._users:
										cclientid = nicknames[each]
										cclientid.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop]))
								else:
									raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
							else:
								raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")
						else:
							if self._nickname.lower() in chan._op or self._nickname.lower() in chan._owner or Override:
								if param[2][iloop] == "c":
									unsetother = ""
									if SetMode:
										if chan.MODE_stripcolour: unsetother = "-C"
										chan.MODE_nocolour = True
										chan.MODE_stripcolour = False
									else:
										chan.MODE_nocolour = False

									szModestr = ":%s!%s@%s MODE %s %s%s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,unsetother,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "C":
									unsetother = ""
									if SetMode:
										if chan.MODE_nocolour: unsetother = "-c"
										chan.MODE_stripcolour = True
										chan.MODE_nocolour = False
									else:
										chan.MODE_stripcolour = False

									szModestr = ":%s!%s@%s MODE %s %s%s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,unsetother,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "e":
									if SetMode: raw(self,"472",self._nickname,"e")

								elif param[2][iloop] == "f":
									if SetMode: chan.MODE_profanity = True
									else: chan.MODE_profanity = False
									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "G":
									if SetMode: chan.MODE_gagonban = True
									else: chan.MODE_gagonban = False
									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "h":
									extra = ""
									if SetMode:
										chan.MODE_hidden = True
										if chan.MODE_secret: 
											extra = "-s"
											chan.MODE_secret = False

										elif chan.MODE_private:
											extra = "-p"
											chan.MODE_private = False
									else:
										chan.MODE_hidden = False

									szModestr = ":%s!%s@%s MODE %s %s%s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,extra,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "i":
									if SetMode: chan.MODE_inviteonly = True
									else: chan.MODE_inviteonly = False
									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "I":
									if SetMode: raw(self,"472",self._nickname,"I")

								elif param[2][iloop] == "K":
									if SetMode:
										chan.MODE_noclones = True
									else:
										chan.MODE_noclones = False

									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "m":
									if SetMode: chan.MODE_moderated = True
									else: chan.MODE_moderated = False
									szModestr =":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "n":
									if SetMode: chan.MODE_externalmessages = True
									else: chan.MODE_externalmessages = False

									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "p":
									extra = ""
									if SetMode:
										chan.MODE_private = True
										if chan.MODE_hidden: 
											extra = "-h"
											chan.MODE_hidden = False

										elif chan.MODE_secret:
											extra = "-s"
											chan.MODE_secret = False
									else:
										chan.MODE_private = False

									szModestr = ":%s!%s@%s MODE %s %s%s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,extra,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "R":
									if SetMode: chan.MODE_registeredonly = True
									else: chan.MODE_registeredonly = False
									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "s":
									extra = ""
									if SetMode:
										if chan.MODE_hidden: 
											extra = "-h"
											chan.MODE_hidden = False
										
										elif chan.MODE_private: 
											extra = "-p"
											chan.MODE_private = False
										
										chan.MODE_secret = True
									else: chan.MODE_secret = False
									szModestr = ":%s!%s@%s MODE %s %s%s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,extra,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "t":
									oTopic = True
									unsetother = ""
									if SetMode:
										if chan.MODE_ownertopic:
											if self._nickname.lower() in chan._owner:
												unsetother = "-T"
												chan.MODE_ownertopic = False
											else:
												oTopic = False
												raw(self,"485",self._nickname,chan.channelname)

										chan.MODE_optopic = True
									else: chan.MODE_optopic = False
									if oTopic: szModestr = ":%s!%s@%s MODE %s %s%s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,unsetother,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "u":
									if SetMode: chan.MODE_knock = True
									else: chan.MODE_knock = False

									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								elif param[2][iloop] == "w":
									if SetMode: chan.MODE_whisper = True
									else: chan.MODE_whisper = False
									szModestr = ":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,chan.channelname,iif(SetMode,"+","-"),param[2][iloop])

								if szModestr:
									for each in chan._users:
										cclientid = nicknames[each]
										cclientid.send(szModestr)

							else:
								raw(self,"482",self._nickname,chan.channelname)

							if szModestr == "":
								raw(self,"501",self._nickname)

						iloop+=1

					time.sleep(0.3)
				else:
					raw(self,"442",self._nickname,chan.channelname)
		else:
			raw(self,"403",self._nickname,param[1])

	elif param[1].lower() == self._nickname.lower():

		if len(param) == 2:
			raw(self,"221",self._nickname,self._MODE_)
		else:
			iloop = 0
			param[2] = compilemodestr(param[2])
			SetMode = True
			while iloop < len(param[2]):
				if param[2][iloop] == "+":
					SetMode = True

				elif param[2][iloop] == "-":
					SetMode = False

				elif param[2][iloop] == "i":
					if SetMode:
						if "i" not in self._MODE_: self._MODE_ = self._MODE_ + "i"
						if self not in invisible: invisible.append(self)
						self._MODE_invisible = True
						
					else:
						self._MODE_ = self._MODE_.replace("i","")
						if self in invisible: invisible.remove(self)
						self._MODE_invisible = False

					for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "i")
					self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))

				elif param[2][iloop] == "f":
					if SetMode:
						if "f" not in self._MODE_: self._MODE_ = self._MODE_ + "f"
						self._MODE_filter = True
					else:
						self._MODE_ = self._MODE_.replace("f","")
						self._MODE_filter = False

					for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "f")
					self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))

				elif param[2][iloop] == "R":
					if SetMode:
						if "R" not in self._MODE_: self._MODE_ = self._MODE_ + "R"
						self._MODE_registerchat = True
					else:
						self._MODE_ = self._MODE_.replace("R","")
						self._MODE_registerchat = False

					for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "R")
					self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))

				elif param[2][iloop] == "p":
					if SetMode:
						if "p" not in self._MODE_: self._MODE_ = self._MODE_ + "p"
						self._MODE_private = True
					else:
						self._MODE_ = self._MODE_.replace("p","")
						self._MODE_private = False
					for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "p")
					self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))

				elif param[2][iloop] == "P":
					if SetMode:
						if "P" not in self._MODE_: self._MODE_ = self._MODE_ + "P"
						self._MODE_nowhisper = True
					else:
						self._MODE_ = self._MODE_.replace("P","")
						self._MODE_nowhisper = False
					for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "P")
					self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))

				elif param[2][iloop] == "z":
					raw(self,"908",self._nickname)

				elif param[2][iloop] == "I":
					if SetMode:
						if "I" not in self._MODE_: self._MODE_ = self._MODE_ + "I"
						self._MODE_inviteblock = True
					else:
						self._MODE_ = self._MODE_.replace("I","")
						self._MODE_inviteblock = False

					for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "I")
					self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))

				elif param[2][iloop] == "z":
					raw(self,"908",self._nickname)


				elif param[2][iloop] == "h": # MODE <nick> +h <pass>
					if len(param) >= 4:
						if SetMode:
							identify = False
							for each in channels:
								isowner = False
								isop = False
								chanid = channels[each.lower()] # we need to scan through each channel to check if they are oper
								if self._nickname.lower() in chanid._owner: isowner = True
								if self._nickname.lower() in chanid._op: isop = True
								if param[3] == chanid._prop.ownerkey:
									if self._IRCX == False:
										pass
									else:
										if self._nickname.lower() in chanid._op: chanid._op.remove(self._nickname.lower())
										if self._nickname.lower() not in chanid._owner: chanid._owner.append(self._nickname.lower())
										identify = True
										for nick in chanid._users:
											nickid = nicknames[nick]
											if isop:
												nickid.send(":%s!%s@%s MODE %s -o %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))

											nickid.send(":%s!%s@%s MODE %s +q %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))

								elif param[3] == chanid._prop.hostkey:
									if self._nickname.lower() in chanid._owner: chanid._owner.remove(self._nickname.lower())
									if self._nickname.lower() not in chanid._op: chanid._op.append(self._nickname.lower())
									identify = True
									for nick in chanid._users:
										nickid = nicknames[nick]
										if isowner:
											nickid.send(":%s!%s@%s MODE %s -q %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))

										nickid.send(":%s!%s@%s MODE %s +o %s\r\n" % (self._nickname,self._username,self._hostmask,chanid.channelname,self._nickname))

							if identify == False:

								raw(self,"908",self._nickname)
					else:
						raw(self,"461",self._nickname,"MODE +h")

				elif param[2][iloop] == "g":
					if self._nickname.lower() in opers:
						opid = opers[self._nickname.lower()]
						if SetMode:
							opid.guide = True
							if "g" not in self._MODE_: self._MODE_ = self._MODE_ + "g"
							self._username = "Guide"
						else:
							self._username = opid.username
							opid.guide = False
							self._MODE_ = self._MODE_.replace("g","")

						for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "g")
						self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))
					else:
						raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

				elif param[2][iloop] == "X":
					if self._nickname.lower() in opers:
						if SetMode:
							if "X" not in self._MODE_: self._MODE_ = self._MODE_ + "X"
							self._friendlyname = " ".join(param).split(" ",3)[3]
							for allservers in linkedServers: allservers.sendUserMode(self._nickname,"+X " + self._friendlyname)
						else:
							self._friendlyname= ""
							self._MODE_ = self._MODE_.replace("X","")
							for allservers in linkedServers: allservers.sendUserMode(self._nickname,"-X")

						self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))
					else:
						raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")


				elif param[2][iloop] == "w":
					if self._nickname.lower() in opers:
						opid = opers[self._nickname.lower()]
						if opid.operlevel >= 2:
							if SetMode:
								opid.watchserver = True	
								if "w" not in self._MODE_: self._MODE_ = self._MODE_ + "w"
							else:
								opid.watchserver = False
								self._MODE_ = self._MODE_.replace("w","")

							for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "w")
							self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))
						else:
							raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
					else:
						raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")

				elif param[2][iloop] == "b":
					if self._nickname.lower() in opers:
						opid = opers[self._nickname.lower()]
						if opid.operlevel >= 2:
							if SetMode:
								opid.watchbans = True
								if "b" not in self._MODE_: self._MODE_ = self._MODE_ + "b"
							else:
								self._MODE_ = self._MODE_.replace("b","")
								opid.watchbans = False

							for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "b")
							self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))
						else:
							raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
					else:
						raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")

				elif param[2][iloop] == "n":
					if self._nickname.lower() in opers:
						opid = opers[self._nickname.lower()]
						if opid.operlevel >= 2:
							if SetMode:
								opid.watchnickserv = True
								if "n"not in self._MODE_: self._MODE_ = self._MODE_ + "n"
							else:
								self._MODE_ = self._MODE_.replace("n","")
								opid.watchnickserv = False

							for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "n")
							self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))
						else:
							raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")
					else:
						raw(self,"481",self._nickname,"Permission Denied - You're not an Administrator")

				elif param[2][iloop] == "s":
					if self._nickname.lower() in opers:
						opid = opers[self._nickname.lower()]
						if SetMode:
							opid.hidden = True
							if self not in opersecret: opersecret.append(self)
							if "s" not in self._MODE_: self._MODE_ = self._MODE_ + "s"
						else:
							opid.hidden = False	
							if self in opersecret: opersecret.remove(self)
							self._MODE_ = self._MODE_.replace("s","")

						for allservers in linkedServers: allservers.sendUserMode(self._nickname,iif(SetMode,"+","-") + "s")
						self.send(":%s!%s@%s MODE %s %s%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,iif(SetMode,"+","-"),param[2][iloop]))
					else:
						raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")

				elif param[2][iloop] == "o" or param[2][iloop] == "O" or param[2][iloop] == "a" or param[2][iloop] == "A":
					if self._nickname.lower() in opers:
					
						opid = opers[self._nickname.lower()]

						if SetMode:
							if param[2][iloop] in opid.flags: 
								self.send(":" + ServerName + " NOTICE SERVER :*** Cannot modify usermode '" + param[2][iloop] + "'\r\n")
							else: 
								raw(self,"491",self._nickname,"Permission denied - Not enough priviledges")
						else:
							if param[2][iloop] == "o":
								if opid.hidden: self.send(":%s!%s@%s MODE %s -s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname))
								if opid.watchserver: self.send(":%s!%s@%s MODE %s -w\r\n" % (self._nickname,self._username,self._hostmask,self._nickname))
								if opid.guide: self.send(":%s!%s@%s MODE %s -g\r\n" % (self._nickname,self._username,self._hostmask,self._nickname))
								if opid.watchbans: self.send(":%s!%s@%s MODE %s -b\r\n" % (self._nickname,self._username,self._hostmask,self._nickname))
								if opid.watchnickserv: self.send(":%s!%s@%s MODE %s -n\r\n" % (self._nickname,self._username,self._hostmask,self._nickname))

								self.send(":%s!%s@%s MODE %s -%s\r\n" % (self._nickname,self._username,self._hostmask,self._nickname,opid.flags))
								self.send(":" + ServerName + " NOTICE SERVER :*** You are no longer an operator on this server\r\n")
								for mode in opid.flags:
									self._MODE_ = self._MODE_.replace(mode,"")
									
								self._MODE_ = self._MODE_.replace("g","")
								self._MODE_ = self._MODE_.replace("s","")
								self._MODE_ = self._MODE_.replace("w","")
								self._MODE_ = self._MODE_.replace("b","")
								self._MODE_ = self._MODE_.replace("n","")
								if self._MODE_register == False: # no longer oper, conform to nickserv modes
									self._username = PrefixChar + self._username

								if self in opersecret: opersecret.remove(self)
								opid.guide = False
								opid.usage = False
								opid.hidden = False
								opid.watchserver = False
								opid.watchban = False
								opid.watchnickserv = False

								del opers[self._nickname.lower()]
								for allservers in linkedServers: allservers.sendUserMode(self._nickname,"-o")
							else:
								if param[2][iloop].lower() in opid.flags:
									self.send(":" + ServerName + " NOTICE SERVER :*** Cannot remove usermode '" + param[2][iloop] + "', please use the conf\r\n")
								else:
									raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")
					else:
						raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")
						
				else:
					raw(self,"501",self._nickname)	

				iloop+=1

	elif param[1].lower() in nicknames:
		if len(param) == 2:
			if self._nickname.lower() in opers:
				raw(self,"221",nicknames[param[1].lower()]._nickname,nicknames[param[1].lower()]._MODE_)
			else:
				raw(self,"481",self._nickname,"Permission Denied - You're not a System operator")
		else:
			raw(self,"502",self._nickname)

	else:
		raw(self,"401",self._nickname,param[1])

def Nickserv_function(self,param,msgtype=""):
	try:

		replyType = "NOTICE"

		if msgtype != "":
			if param[1][0] == ":":
				param[1] = param[1][1:]
				replyType = msgtype

		param[1] = param[1].upper()

		if param[1] == "REGISTER":
			try:
				if self._MODE_register == True:
					self.send(":%s!%s@%s %s %s :Error: You are already registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
				elif self._nickname.lower() not in opers and ((self._signontime - GetEpochTime()) < -300) == False and defconMode == 2:
					self.send(":%s!%s@%s %s %s :Error: NickServ requires you to stay on this server a minimum amount of time before registering your nickname\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					sendNickservOpers("Notice -- \x02NickServ\x02 - (%s!%s@%s) [%s] has tried to registered their nickname (not online long enough, defcon 2 is active)\r\n" % (self._nickname,self._username,self._hostmask,self.details[0]))
				elif self._nickname.lower() not in opers and defconMode == 3:
					self.send(":%s!%s@%s %s %s :Error: NickServ will not allow nicknames to be registered at this time\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					sendNickservOpers("Notice -- \x02NickServ\x02 - (%s!%s@%s) [%s] has tried to registered their nickname (nickserv disabled, defcon 3 is active)\r\n" % (self._nickname,self._username,self._hostmask,self.details[0]))
				else:

					passw = param[2]
					emaila = param[3]
					checkemail = emaila.split("@")[1].split(".")[1]
					toomanynicks = 0
					exemptFromConnectionKiller = False
					for regnicks in Nickserv:
						mydetails_obj = Nickserv[regnicks.lower()]
						mydetails = mydetails_obj._details
						if mydetails == self.details[0]:
							toomanynicks+=1

					try:
						for each in globals()["connectionsExempt"]:
							if each == "":
								continue

							chk = re.compile("^" + each + "$")
							if chk.match(self.details[0]) != None:
								exemptFromConnectionKiller = True
								break
					except:
						print sys.exc_info()

					if NickservIPprotection == False: exemptFromConnectionKiller = True

					grouped_nick = False
					for groupnicks in Nickserv.values():
						if self._nickname.lower() in groupnicks._groupnick:
							grouped_nick = True
							break

					if self._nickname.lower() in Nickserv or grouped_nick == True:
						self.send(":%s!%s@%s %s %s :Error: That nickname has already been registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

					elif toomanynicks >= 1 and exemptFromConnectionKiller == False:
						self.send(":%s!%s@%s %s %s :Error: You can only register one nickname, you can group nicknames though\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					else:
						olevel = 0
						if self._nickname.lower() in opers:
							opid = opers[self._nickname.lower()]
							olevel = opid.operlevel
						
						writehash = sha.new()
						writehash.update(passw + NickservParam)

						Nickserv[self._nickname.lower()] = NickServ(self._nickname,writehash.hexdigest(),emaila,GetEpochTime(),self.details[0],"",olevel,False) #add to the nickname database
						self.send(":%s!%s@%s %s %s :\x02Registration complete\x02\r\n:%s!%s@%s %s %s :Your nickname has been registered with the address *@%s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname,self._hostmask))
						self.send(":%s!%s@%s %s %s :Your password is \x02%s\x02, please remember to keep this safe\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,passw))
						self._MODE_register = True
						for allservers in linkedServers: allservers.sendUserMode(self._nickname,"+r")
						WriteUsers(MaxLocal,MaxGlobal,True,False)
						if self._username[0] == PrefixChar: self._username = self._username[1:]
						if "r" not in self._MODE_: self._MODE_ += "r"
						self.send(":%s!%s@%s MODE %s +r\r\n" % ("NickServ","NickServ",NetworkName,self._nickname))
						sendNickservOpers("Notice -- \x02NickServ\x02 - (%s!%s@%s) [%s] has registered their nickname\r\n" % (self._nickname,self._username,self._hostmask,self.details[0]))
							
			except:
				self.send(":%s!%s@%s %s %s :Syntax: \x02REGISTER \x1Fpassword\x1F \x1Femail\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
		
		elif param[1] == "HELLO":
			self.send(":%s!%s@%s %s %s :hello to you too! does your mummy know you're on IRC?\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

		elif param[1] == "IPLOCK":
			if len(param) == 2:
				if globals()["NickservIPprotection"] == False:
					methodIS = "\x02Off\x02"
				else:
					methodIS = "\x02On\x02"

				self.send(":%s!%s@%s %s %s :IPLOCK is currently %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,methodIS))
			else:
				if self._nickname.lower() in opers:
					opid = opers[self._nickname.lower()]
					if opid.operlevel > 2:
						if param[2].upper() == "ON":
							globals()["NickservIPprotection"] = True
							defconDesc = "disallow nicknames to be registered by duplicate IP addresses \x02(high protection)\x02"
						elif param[2].upper() == "OFF":
							globals()["NickservIPprotection"] = False
							defconDesc = "allow nicknames to be registered regardless of whether their IP has registered before \x02(low protection)\x02"
						else:
							self.send(":%s!%s@%s %s %s :No such IPLOCK mode\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
							return
						
						self.send(":%s!%s@%s %s %s :NickServ will now %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,defconDesc))
						sendNickservOpers("Notice -- \x02NickServ\x02 - IPLOCK changed by %s, NickServ will now %s\r\n" % (self._nickname,defconDesc))
					else:
						self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
				else:
					self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))			
		
		elif param[1] == "DEFCON":
			if len(param) == 2:
				self.send(":%s!%s@%s %s %s :DEFCON is currently operating on level %d\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,globals()["defconMode"]))
			else:
				if self._nickname.lower() in opers:
					opid = opers[self._nickname.lower()]
					if opid.operlevel > 2:
						if param[2] == "1":
							globals()["defconMode"] = 1
							defconDesc = "allow nicknames to be registered at any time with no restrictions \x02(low protection)\x02"
						elif param[2] == "2":
							globals()["defconMode"] = 2
							defconDesc = "allow nicknames to be registered after the user has been online for 5 minutes \x02(high protection)\x02"
						elif param[2] == "3":
							globals()["defconMode"] = 3
							defconDesc = "disallow any new registrations \x02(disabled)\x02"
						else:
							self.send(":%s!%s@%s %s %s :No such DEFCON level available\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
							return
						
						self.send(":%s!%s@%s %s %s :NickServ will now %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,defconDesc))
						sendNickservOpers("Notice -- \x02NickServ\x02 - DEFCON changed by %s, NickServ will now %s\r\n" % (self._nickname,defconDesc))
					else:
						self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
				else:
					self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
			

		elif param[1] == "IDENTIFY":
			try:
				if self._MODE_register == True:
					self.send(":%s!%s@%s %s %s :Error: You are already identified\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
				else:
					passw = param[2]
					grouped_nick = None
					for groupnicks in Nickserv.values():
						if self._nickname.lower() in groupnicks._groupnick:
							grouped_nick = groupnicks
							break

					if self._nickname.lower() in Nickserv or grouped_nick != None:
						if grouped_nick != None:
							ns = grouped_nick
						else:
							ns = Nickserv[self._nickname.lower()]

						writehash1 = sha.new()
						writehash1.update(passw + NickservParam)

						if writehash1.hexdigest() == ns._password:
							self._MODE_register = True
							if "r" not in self._MODE_: self._MODE_ += "r"
							for allservers in linkedServers: allservers.sendUserMode(self._nickname,"+r")
							if self._username[0] == PrefixChar: self._username = self._username[1:]
							self.send(":%s!%s@%s MODE %s +r\r\n" % ("NickServ","NickServ",NetworkName,self._nickname))
							self.send(":%s!%s@%s %s %s :Welcome back %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,self._nickname))
							
							if ns._vhost != "":
								self._hostmask = ns._vhost
								self.send(":%s!%s@%s %s %s :Your \x02vhost\x02 has been activated\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
							
						else:
							self.send(":%s!%s@%s %s %s :Error: Invalid password\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					else:
						self.send(":%s!%s@%s %s %s :Error: Your nick isn't registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

			except:
				self.send(":%s!%s@%s %s %s :Syntax: \x02IDENTIFY \x1Fpassword\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
		
		elif param[1] == "GHOST":
			try:
				nickn = param[2]
				passw = param[3]

				groupnick = None
				for groupnicks in Nickserv.values():
					if nickn.lower() in groupnicks._groupnick:
						groupnick = groupnicks
						break

				if nickn.lower() in Nickserv or groupnick:
					if groupnick:
						ns = groupnick
					else:
						ns = Nickserv[nickn.lower()]

					writehash1 = sha.new()
					writehash1.update(passw + NickservParam)

					if writehash1.hexdigest() == ns._password:
						if nickn.lower() in nicknames:

							cid = nicknames[nickn.lower()]

							sendto = [cid]

							cid.send(":%s!%s@%s %s %s :A ghost command has been used on your nickname, it may be because someone has already registered your name\r\n" % ("NickServ","NickServ",NetworkName,replyType,cid._nickname))
							
							nonIRCXsend = ":%s!%s@%s QUIT :Killed by %s (%s)\r\n" % (cid._nickname,cid._username,cid._hostmask,"NickServ","Ghosted nickname") #non IRCX clients don't understand KILL
							_send = ":%s!%s@%s KILL %s :Ghost nickname\r\n" % ("NickServ","NickServ",NetworkName,cid._nickname)
							if cid._IRCX: cid.send(_send)
							else: cid.send(nonIRCXsend)

							for each in cid._channels:
								chan = channels[each.lower()]
								for n in chan._users:
									if n in nicknames:
										nick = nicknames[n.lower()]
										if nick not in sendto:
											if cid._nickname.lower() not in chan._watch:
												if chan.MODE_auditorium == False or isOp(n,chan.channelname):
													sendto.append(nick)
													if nick._IRCX:
														nick.send(_send)
													else:
														nick.send(nonIRCXsend)

							sendto = []														

							cid.quittype = -1
							cid.quitmsg = " by NickServ"
							cid.die = True

							self.send(":%s!%s@%s %s %s :The ghosted nickname has been killed\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

						else:
							self.send(":%s!%s@%s %s %s :Error: Your nickname is free\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					else:
						self.send(":%s!%s@%s %s %s :Error: Invalid password\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
				else:
					self.send(":%s!%s@%s %s %s :Error: That nick isn't registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

			except:
				self.send(":%s!%s@%s %s %s :Syntax: \x02GHOST \x1Fnickname\x1F \x1Fpassword\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
		
		elif param[1] == "INFO":
			try:
				nickn = param[2]
				grouped_nick = None
				for groupnicks in Nickserv.values():
					if nickn.lower() in groupnicks._groupnick:
						grouped_nick = groupnicks
						break


				if nickn.lower() in Nickserv or grouped_nick != None:
					if grouped_nick != None:
						ns = grouped_nick
					else:
						ns = Nickserv[nickn.lower()]

					self.send(":%s!%s@%s %s %s :\x02Nickname Information\x02 for %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,ns._nickname))
					if len(ns._groupnick) != 0: self.send(":%s!%s@%s %s %s :Grouped nicknames: %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,", ".join(ns._groupnick)))
					self.send(":%s!%s@%s %s %s :Registered: %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,time.ctime(float(ns._registrationtime))))
					if ns._showemail == "True" or self._nickname.lower() in opers:
						emailaddress = ns._email
					else:
						emailaddress = "hidden"

					self.send(":%s!%s@%s %s %s :Email address: %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,emailaddress))
					onlineStatus = "Online but not identified (could be a clone)"
					if nickn.lower() in nicknames:
						nick_id = nicknames[nickn.lower()]
						if "r" in nick_id._MODE_:
							onlineStatus = "\x02Online and identified!\x02"
					else:
						onlineStatus = "Offline"

					self.send(":%s!%s@%s %s %s :User is: %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,onlineStatus))

					if self._nickname.lower() in opers:
						opid = opers[self._nickname.lower()]
						if opid.operlevel > ns._level:
							self.send(":%s!%s@%s %s %s :Address: %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,ns._details))
				else:
					self.send(":%s!%s@%s %s %s :Error: That nick isn't registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

			except:
				self.send(":%s!%s@%s %s %s :Syntax: \x02INFO \x1Fnickname\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
			

		elif param[1] == "SET":
			try:
				nickn = param[2]
				if nickn.upper() == "HELP":
					if self._nickname.lower() in opers:
						self.send(":%s!%s@%s %s %s :SET <nickname> \x02VHOST\x02 \x1Fmask\x1F\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

					self.send(":%s!%s@%s %s %s :SET <nickname> \x02PASSWORD\x02 \x1Fold password\x1F \x1Fnew password\x1F\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					self.send(":%s!%s@%s %s %s :SET <nickname> \x02SHOWEMAIL\x02 \x1Fon/off\x1F\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					

				elif nickn.lower() in Nickserv:
					option = param[3].upper()
					nid = Nickserv[nickn.lower()]

					try:
						value = param[4] 
					except:
						if option == "VHOST":
							if nid._vhost != "":
								self.send(":%s!%s@%s %s %s :Nickserv will no longer assign a vhost to %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,nid._nickname))
								nid._vhost = ""
								WriteUsers(MaxLocal,MaxGlobal,True,False)
							else:
								self.send(":%s!%s@%s %s %s :%s does not have a \x02vhost\x02 assigned\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,nid._nickname))

							option = ""
					
					if option == "": pass

					elif option == "VHOST":
						if self._nickname.lower() in opers:
							opid = opers[self._nickname.lower()]
							if opid.operlevel >= nid._level or self._nickname.lower() == nid._nickname.lower() and self._MODE_register:
								if self._validate(value.replace(".","a").replace("/","a")):
									nid._vhost = value
									WriteUsers(MaxLocal,MaxGlobal,True,False)
									self.send(":%s!%s@%s %s %s :A \x02vhost\x02 has been assigned to %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,nid._nickname))
									if nickn.lower() in nicknames:
										cid = nicknames[nickn.lower()]
										if cid._MODE_register and cid != self: # if they are registered 
											cid.send(":%s!%s@%s %s %s :A \x02vhost\x02 has been assigned to your registered nickname\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
											cid._hostmask = value
								else:
									self.send(":%s!%s@%s %s %s :Error: Invalid vhost\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
							else:
								self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
						else:
							self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					
					elif option == "SHOWEMAIL":
						if nickn.lower() == self._nickname.lower() and "r" in self._MODE_:
							if value == "on":
								nid._showemail = "True"
								self.send(":%s!%s@%s %s %s :Nickserv will now display your email on information requests\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
								WriteUsers(MaxLocal,MaxGlobal,True,False)
							elif value == "off":
								nid._showemail = "False"
								self.send(":%s!%s@%s %s %s :Nickserv will no longer display your email\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
								WriteUsers(MaxLocal,MaxGlobal,True,False)
							else:
								self.send(":%s!%s@%s %s %s :SET <nickname> \x02SHOWEMAIL\x02 \x1Fon/off\x1F\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
						else:
							self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

					elif option == "PASSWORD":
						value1 = param[5]
						if nickn.lower() in Nickserv:
							nid = Nickserv[nickn.lower()]

							writehash1 = sha.new()
							writehash1.update(value + NickservParam)

							writehash2 = sha.new()
							writehash2.update(value1 + NickservParam)

							if writehash1.hexdigest() == nid._password:
								nid._password = writehash2.hexdigest()
								WriteUsers(MaxLocal,MaxGlobal,True,False)
								self.send(":%s!%s@%s %s %s :Nickserv password has been changed successfully\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
								if nickn.lower() in nicknames:
									cid = nicknames[nickn.lower()]
									if cid._MODE_register:
										cid.send(":%s!%s@%s %s %s :Your nickname \x02password\x02 has been changed to \x02%s\x02\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,value1))
							else:
								self.send(":%s!%s@%s %s %s :Error: Invalid password\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
						else:
							self.send(":%s!%s@%s %s %s :Error: That nick isn't registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					else:
						self.send(":%s!%s@%s %s %s :Error: Unknown property\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
				else:
					self.send(":%s!%s@%s %s %s :Error: That nick isn't registered or you are not using your primary nickname\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
			except:
				self.send(":%s!%s@%s %s %s :Syntax Error: \x02SET \x1Fhelp\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

		elif param[1] == "UNGROUP": # NS GROUP nickname <password>
			try:
				if param[2].lower() in Nickserv:
					nid = Nickserv[param[2].lower()]
					writehash1 = sha.new()
					writehash1.update(param[3] + NickservParam)
					if writehash1.hexdigest() == nid._password:
						if self._nickname.lower() not in nid._groupnick:
							self.send(":%s!%s@%s %s %s :Error: No such nickname grouped to %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,nid._nickname))
						else:
							nid._groupnick.remove(self._nickname.lower())
							self.send(":%s!%s@%s %s %s :That nickname is now ungrouped\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
							WriteUsers(MaxLocal,MaxGlobal,True,False)
					else:
						self.send(":%s!%s@%s %s %s :Error: Invalid password\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

				else:
					self.send(":%s!%s@%s %s %s :Error: The nickname you're trying to group with does not exist!\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

			except IndexError:
				self.send(":%s!%s@%s %s %s :Syntax Error: \x02GROUP \x1Fprimary nickname\x1F \x1Fpassword\x1F\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
			


		elif param[1] == "GROUP": # NS GROUP nickname <password>
			try:
				if param[2].lower() in Nickserv:
					nid = Nickserv[param[2].lower()]
					writehash1 = sha.new()
					writehash1.update(param[3] + NickservParam)
					if writehash1.hexdigest() == nid._password:
						if len(nid._groupnick) == 2:
							self.send(":%s!%s@%s %s %s :Error: You can only \x02group\x02 two nicknames\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
						else:
							grouped_already = False
							for groupnicks in Nickserv.values():
								if self._nickname.lower() in groupnicks._groupnick:
									self.send(":%s!%s@%s %s %s :Error: This nickname is already grouped/registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
									grouped_already = True
									break

							if grouped_already == False:
								nid._groupnick.append(self._nickname.lower())
								self.send(":%s!%s@%s %s %s :\x02Grouping complete\x02\r\n:%s!%s@%s %s %s :%s has been \x02grouped\x02 with the registered nickname: %s\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname,self._nickname,nid._nickname))
								WriteUsers(MaxLocal,MaxGlobal,True,False)
								self._MODE_register = True
								for allservers in linkedServers: allservers.sendUserMode(self._nickname,"+r")
								if self._username[0] == PrefixChar: self._username = self._username[1:]
								if "r" not in self._MODE_: self._MODE_ += "r"
								self.send(":%s!%s@%s MODE %s +r\r\n" % ("NickServ","NickServ",NetworkName,self._nickname))
								sendNickservOpers("Notice -- \x02NickServ\x02 - (%s!%s@%s) [%s] has grouped their nickname with \x02%s\x02\r\n" % (self._nickname,self._username,self._hostmask,self.details[0],nid._nickname))

					else:
						self.send(":%s!%s@%s %s %s :Error: Invalid password\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

				else:
					self.send(":%s!%s@%s %s %s :Error: The nickname you're trying to group with does not exist!\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

			except IndexError:
				self.send(":%s!%s@%s %s %s :Syntax: \x02GROUP \x1Fprimary nickname\x1F \x1Fpassword\x1F\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
			

		elif param[1] == "DROP":
			try:
				nickn = param[2]
				try:
					passw = param[3]
				except:
					passw = ""

				grouped_nick = False
				for groupnicks in Nickserv.values():
					if nickn.lower() in groupnicks._groupnick:
						grouped_nick = True
						self.send(":%s!%s@%s %s %s :Error: You cannot \x02drop\x02 a grouped nickname, please use \x1FUNGROUP\x1F\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
						break

				if grouped_nick == False:
					if nickn.lower() in Nickserv:
						ns = Nickserv[nickn.lower()]

						writehash1 = sha.new()
						writehash1.update(passw + NickservParam)

						if ns._password == writehash1.hexdigest() or self._nickname.lower() in opers:

							if ns._password == writehash1.hexdigest(): dropn = True
							else:
								opid = opers[self._nickname.lower()]

								if opid.operlevel > ns._level: dropn = True
								else:
									dropn = False

							if dropn:
								if ns._nickname.lower() in nicknames:
									cid = nicknames[ns._nickname.lower()]
									if cid._MODE_register:
										cid._MODE_.replace("r","")
										for allservers in linkedServers: allservers.sendUserMode(self._nickname,"-r")
										cid._MODE_register = False
										if cid._username[0] != PrefixChar and cid._nickname.lower() not in opers: cid._username = PrefixChar + cid._username[1:]

										cid.send(":%s!%s@%s MODE %s -r\r\n" % ("NickServ","Nickserv",NetworkName,cid._nickname))
										if cid != self:
											cid.send(":%s!%s@%s %s %s :Your nickname has been dropped\r\n" % ("NickServ","NickServ",NetworkName,replyType,cid._nickname))
								
								del Nickserv[nickn.lower()]
								WriteUsers(MaxLocal,MaxGlobal,True,False)
								self.send(":%s!%s@%s %s %s :The nickname \x02%s\x02 has been dropped\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,ns._nickname))
							else:
								self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
						else:
							self.send(":%s!%s@%s %s %s :Error: Access denied\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
					else:
						self.send(":%s!%s@%s %s %s :Error: That nick isn't registered\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))

			except:
				self.send(":%s!%s@%s %s %s :Syntax: \x02DROP \x1Fnickname\x1F \x1F[password]\x1F\x02\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
		
		elif param[1] == "HELP":
			self.send(":%s!%s@%s %s %s :REGISTER register a nickname\r\n:%s!%s@%s %s %s :IDENTIFY identify yourself with a password\r\n:%s!%s@%s %s %s :GHOST Disconnect a user using your nickname \r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))
			self.send(":%s!%s@%s %s %s :INFO get information about a nickname\r\n:%s!%s@%s %s %s :DROP release nickname from services, this means other users can register this nick\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))
			self.send(":%s!%s@%s %s %s :GROUP/UNGROUP groups alternative nicknames with your primary nickname\r\n:%s!%s@%s %s %s :SET help\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))
			self.send(":%s!%s@%s %s %s :DEFCON view or modify the DEFCON settings\r\n:%s!%s@%s %s %s :IPLOCK view or modify the IP lock settings\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))
		
		else:
			self.send(":%s!%s@%s %s %s :Error: Unknown command\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname))
			
	except:
		self.send(":%s!%s@%s %s %s :REGISTER register a nickname\r\n:%s!%s@%s %s %s :IDENTIFY identify yourself with a password\r\n:%s!%s@%s %s %s :GHOST Disconnect a user using your nickname \r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))
		self.send(":%s!%s@%s %s %s :INFO get information about a nickname\r\n:%s!%s@%s %s %s :DROP release nickname from services, this means other users can register this nick\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))
		self.send(":%s!%s@%s %s %s :GROUP/UNGROUP groups alternative nicknames with your primary nickname\r\n:%s!%s@%s %s %s :SET help\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))
		self.send(":%s!%s@%s %s %s :DEFCON view or modify the DEFCON settings\r\n:%s!%s@%s %s %s :IPLOCK view or modify the IP lock settings\r\n" % ("NickServ","NickServ",NetworkName,replyType,self._nickname,"NickServ","NickServ",NetworkName,replyType,self._nickname))


def settings(): # this is information such as channels, max users etc
	myfile = open('database/channels.dat','rb')
	for lineStr in myfile.readlines():
		s_line = lineStr.split("\x01")
		if s_line[0].split("=")[0].upper() == "C":
			s_chan = s_line[0].split("=")[1]
			s_modes = s_line[1].split("=")[1]
			s_topic = s_line[2].split("=",1,)[1]
			s_founder = s_line[3].split("=",1,)[1]
			s_prop = s_line[4].split("=",1,)[1]
			s_ax = s_line[5].split("=",1,)[1]

			chanclass = Channel(s_chan,"",s_modes) #create
			if chanclass.channelname != "":
				_founder = ""
				channels[s_chan.lower()] = chanclass
				if "r" in s_modes: chanclass._prop.registered = ServerName
				if s_founder != "":
					_founder = _Access.CreateMaskString(s_founder,True)

				chanclass._founder = _founder
				chanclass._topic = s_topic
				
				chanclass._topic_nick = ServerName
				chanclass._topic_time = GetEpochTime()
				chanclass.ChannelAccess = loads(decompress(s_ax.strip().decode("hex")))
				chanclass._prop = loads(decompress(s_prop.decode("hex")))
				if s_founder != "":_addrec = _Access.AddRecord("",chanclass.channelname.lower(),"OWNER",_founder,0,"")
	
	myfile.close()

	global ServerAccess

	myfile = open('database/access.dat','rb')
	try:
		ServerAccess = loads(myfile.read())
	except EOFError:
		ServerAccess = []

	myfile.close()


class ServerListen(threading.Thread):

	def __init__ (self,port):
		self.port = port
		threading.Thread.__init__(self)

	def run(self):

		try:
			smain = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			smain.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			smain.bind((ipaddress,int(self.port)))
			smain.settimeout(5.0)
			smain.listen(100)

			print "* Listening on port " + str(self.port) + " on '"+ ipaddress+"'"

			while True:
				time.sleep(0.1)
				try:
					try:
						(clientsocket,address) = smain.accept()
						ClientConnecting(clientsocket,address,self.port).start()
					except:
						if self.port not in Ports:
							print "*** Terminating server on port " + self.port
							break

				except:
					print "There was an error whilst a user was connecting"
		except:
			print "*** ERROR: Socket error on port " + str(self.port)  + "(Bind Error)"

		if self.port in currentports:
			del currentports[self.port]


def GetUTC_NTP():

	return 0

	try:
		TIME1970 = 2208988800L
		client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		data = '\x1b' + 47 * '\0'
		client.sendto(data,(NTPServer, 123 ))
		data, address = client.recvfrom( 1024 )
		if data:
			t = unpack( '!12I', data )[10]
			t -= TIME1970
			return t

		return 0
	except:
		return 0


def GetEpochTime():
	#actual time from an NTP server is Time
	return int(time.time())
	# + timeDifference

def pyRCXsetup():
	if os.path.isfile("database/channels.dat") == False: 
		print "*** Could not find channels file, creating new channel file"
		createfile = open("database/channels.dat","w")
		createfile.close()
		return 0

	if os.path.isfile("database/access.dat") == False: 
		print "*** Could not find access file, setting up access file"
		createfile = open("database/access.dat","w")
		createfile.close()
		return 0

	if os.path.isfile("database/Nickserv.dat") == False: 
		print "*** Could not find Nickserv database, installing Nickserv"
		createfile = open("database/Nickserv.dat","w")
		createfile.close()
		return 0

	if os.path.isfile("database/users.dat") == False: 
		print "*** Could not find previous historic user counts, history being setup"
		createfile = open("database/access.dat","w")
		createfile.write("1\n1\n")
		createfile.close()
		return 0

	return 1
		

def SetupListeningSockets():
	global currentports

	for p in Ports:
		if p not in currentports: # If the port isn't already running, set it up, old ports will automatically timeout after five seconds
			currentports[p] = ServerListen(p).start()

def main():
	
	print " _____  __    __  _____    _____  __    __ "
	print "|  _  \ \ \  / / |  _  \  /  ___| \ \  / / "
	print "| |_| |  \ \/ /  | |_| |  | |      \ \/ /  "
	print "|  ___/   \  /   |  _  /  | |       }  {   "
	print "| |       / /    | | \ \  | |___   / /\ \  "
	print "|_|      /_/     |_|  \_\ \_____| /_/  \_\ v2.5.2"
	print "__________________________________________"
	print ""
	print "* Developed by chrisjw"
	print "* Bug fixes and recommendations, see /CREDITS"
	print "* Python: www.python.org"
	print "* IRC:    irc.freenode.org"
	print "__________________________________________"
	print ""

	global timeDifference

	print "*** Loading pyRCX 2.5, checking settings\r\n"

	if pyRCXsetup() == 0:
		print "*** please run pyRCXsetup.py first to configure pyRCX"
		return 0

	settings()

	rehash(0)

	print "*** Setting UTC through NTP, current server is: " + NTPServer + ":(123)\r\n"

	NTPtime = GetUTC_NTP()

	if NTPtime == 0:
		print "*** NTP is not set, possibly due to connection error.. your timing could be inaccurate, please do not link this server\r\n"
		NTPtime = int(time.time())
	else:
		print "*** UTC time has been synchronised..\r\n"
	
	timeDifference = NTPtime - int(time.time())

	print "*** Settings loaded, now trying to start your server on the ports you specified\r\n"

	rehash()
	#global NickservParam

	if NickservParam == "":
		raise Exception, "Cannot run server without Nickserv security, please add an n:line to your config"
	while True:
		time.sleep(50)

if __name__ == '__main__':
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