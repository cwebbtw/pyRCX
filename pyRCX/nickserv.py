class NickServEntry:
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
