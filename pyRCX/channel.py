import re
import time

from .prop import Prop
from .raw import Raw
from .server_context import ServerContext


class Channel:
    def __init__(self, server_context: ServerContext, raw_messages: Raw, channelname, joinuser, creationmodes=""):
        self._configuration = server_context.configuration
        self._operator_entries = server_context.operator_entries
        self._nickname_to_client_mapping_entries = server_context.nickname_to_client_mapping_entries
        self._raw_messages = raw_messages

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

        self.channelname = channelname
        if joinuser != "" and self.__validate(channelname, joinuser) == False:
            if joinuser != "":
                cclientid = self._nickname_to_client_mapping_entries[joinuser.lower()]
                cclientid.send(
                    ":%s 706 %s :Channel name is not valid\r\n" % (self._configuration.server_name, cclientid._nickname))

            delGlobalChannel(self.channelname.lower())

            self.channelname = ""
        else:
            cclientid = None
            if creationmodes == "":
                creationmodes = self._configuration.default_modes

            if "Z" in creationmodes:
                self.MODE_noircx = True

            if joinuser != "":
                self._users[joinuser.lower()] = self._nickname_to_client_mapping_entries[joinuser.lower()]
                cclientid = self._nickname_to_client_mapping_entries[joinuser.lower()]

            if joinuser != "":
                if self.MODE_noircx == False:
                    self._owner = [cclientid._nickname.lower()]
                else:
                    self._op = [cclientid._nickname.lower()]

            if joinuser != "":
                self._prop = Prop(channelname, cclientid)  # create instance of prop class
            else:
                self._prop = Prop(channelname, self._configuration.server_name)

            if self.channelname[0] == "&":
                self.localChannel = True
            if len(self.channelname) >= 2:
                if self.channelname[0] + self.channelname[1] == "%&":
                    self.localChannel = True

            setupModes(self, creationmodes)

            if joinuser != "":
                cclientid._channels.append(self.channelname)
                cclientid.send(
                    ":%s!%s@%s JOIN :%s\r\n" %
                    (cclientid._nickname, cclientid._username, cclientid._hostmask, channelname))
                self.sendnames(cclientid._nickname, True)

    def __validate(self, channelname, joinuser):
        channel_prefix = "(" + "|".join(self._configuration.channel_prefix.split(",")) + ")"
        p = re.compile(f"^{channel_prefix}[\u0021-\u002B\u002E-\u00FF\-]{{0,128}}$")

        operator_level = 0
        if joinuser.lower() in self._operator_entries:
            operator_level = self._operator_entries[joinuser.lower()].operator_level

        return p.match(channelname) is not None and not self._configuration.filtering.filter(channelname, "chan", operator_level)

    def GetChannelModes(self, objid, nokey=False):
        modestr = ""
        if self.MODE_moderated:
            modestr += "m"
        if self.MODE_noclones:
            modestr += "K"
        if self.MODE_cloneroom:
            modestr += "e"
        if self.MODE_createclone:
            modestr += "d"
        if self.MODE_ownersetmode:
            modestr += "M"
        if self.MODE_Adminonly:
            modestr += "A"
        if self.MODE_ownerkick == True:
            modestr += "Q"
        if self.MODE_profanity:
            modestr += "f"
        if self.MODE_whisper:
            modestr += "w"
        if self.MODE_gagonban:
            modestr += "G"
        if self.MODE_secret:
            modestr += "s"
        if self.MODE_nomodechanges:
            modestr += "S"
        if self.MODE_inviteonly:
            modestr += "i"
        if self.MODE_hidden:
            modestr += "h"
        if self.MODE_private:
            modestr += "p"
        if self.MODE_externalmessages:
            modestr += "n"
        if self.MODE_ownersetprop:
            modestr += "P"
        if self.MODE_optopic:
            modestr += "t"
        if self.MODE_ownertopic:
            modestr += "T"
        if self.MODE_registered:
            modestr += "r"
        if self.MODE_auditorium:
            modestr += "x"
        if self.MODE_registeredonly:
            modestr += "R"
        if self.MODE_ownersetaccess:
            modestr += "X"
        if self.MODE_noircx:
            modestr += "Z"
        if self.MODE_authenticatedclients:
            modestr += "a"
        if self.MODE_servicechan:
            modestr += "N"
        if self.MODE_nocolour:
            modestr += "c"
        if self.MODE_stripcolour:
            modestr += "C"
        if self.MODE_knock:
            modestr += "u"
        if self.MODE_limit:
            mstr = modestr.split(" ")
            if self.MODE_key == "":
                modestr = mstr[0] + "l " + self.MODE_limitamount
            else:
                if objid == 0 or objid in self._users:
                    modestr = mstr[0].replace("k", "") + "lk " + self.MODE_limitamount + " " + self.MODE_key
                else:
                    modestr = mstr[0].replace("k", "") + "lk " + self.MODE_limitamount

        if self.MODE_key != "" and nokey == False:
            mstr = modestr.split(" ")
            if self.MODE_limit:
                if objid == 0 or objid in self._users:
                    modestr = mstr[0].replace("k", "") + "k " + self.MODE_limitamount + " " + self.MODE_key
                else:
                    modestr = mstr[0].replace("k", "") + "k " + self.MODE_limitamount
            else:
                modestr = mstr[0] + "k " + self.MODE_key

        return modestr

    def isBanned(self, cid):
        _Access.CheckChannelExpiry(self)
        if cid._nickname.lower() in self._operator_entries or isOp(cid._nickname, self.channelname):
            return False
        for each in self.ChannelAccess:
            if each._level.upper() == "DENY":
                ret = _Access.MatchAccess(each._mask, cid)
                if ret == 1:
                    _override = False
                    for eachgrant in self.ChannelAccess:
                        if eachgrant._level.upper() != "DENY":
                            gret = _Access.MatchAccess(eachgrant._mask, cid)
                            if gret == 1:
                                _override = True
                                break

                    if _override:
                        return False
                    return True
        return False

    def ClearUsersModes(self, nick):
        if nick.lower() in self._owner:
            self._owner.remove(nick.lower())
        if nick.lower() in self._op:
            self._op.remove(nick.lower())
        if nick.lower() in self._voice:
            self._voice.remove(nick.lower())

    def kick(self, nick, knick, kickmsg):
        clientid = self._nickname_to_client_mapping_entries[knick.lower()]
        ChanCopyNames = list(self._users)
        for each in ChanCopyNames:
            cclientid = self._nickname_to_client_mapping_entries[each.lower()]
            if self.MODE_auditorium == False or isOp(
                    cclientid._nickname, self.channelname) or isOp(
                nick._nickname, self.channelname) or isOp(
                knick._nickname, self.channelname) or cclientid._nickname.lower() == knick.lower():
                cclientid.send(
                    ":%s!%s@%s KICK %s %s :%s\r\n" %
                    (nick._nickname, nick._username, nick._hostmask, self.channelname, knick, kickmsg))

        if self.channelname in clientid._channels:
            clientid._channels.remove(self.channelname)
        self.__remuser(knick, False)

        if self._prop.onpart != "":
            iloop = 0
            numstr = len(self._prop.onpart.split("\\n"))
            while iloop < numstr:
                clientid.send(
                    ":%s NOTICE %s :%s\r\n" %
                    (self.channelname, clientid._nickname, self._prop.onpart.split("\\n")[iloop]))
                iloop += 1

        if len(self._users) == 0:
            self.resetchannel()

    def sendnames(self, nick, owner=False, sendwatch=False):
        cclientid = getUserOBJ(nick.lower())
        str_chanlist = ""
        iloop = 0
        if isSecret(self, "private",
                    "hidden") == False or nick.lower() in self._users or nick.lower() in self._operator_entries:
            for each in list(self._users):
                cid = getUserOBJ(each)
                iloop += 1
                if iloop == 20:
                    self._raw_messages.raw(cclientid, "353", cclientid._nickname, self.channelname, str_chanlist[1:])
                    str_chanlist = ""
                    iloop = 0

                if self.channelname in cid._watch:
                    if cclientid == cid:
                        if cclientid._IRCX and self.MODE_noircx == False:
                            str_chanlist += " ."
                        else:
                            str_chanlist += " @"

                        if cid._nickname.lower() in self._voice:
                            str_chanlist += "+"

                        str_chanlist += cid._nickname

                elif cid._nickname.lower() in self._owner or cid._nickname.lower() in self._op or cid._nickname.lower() in self._voice:

                    if nick.lower() not in self._users and cid._MODE_invisible and nick.lower() not in self._operator_entries:
                        pass
                    else:
                        isVoice = False
                        if cid._nickname.lower() in self._voice:
                            isVoice = True

                        if cid._nickname.lower() in self._op:
                            str_chanlist += " @"
                            if isVoice:
                                str_chanlist += "+"

                            str_chanlist += cid._nickname

                        elif cid._nickname.lower() in self._owner:
                            if cclientid._IRCX:
                                if self.MODE_noircx:
                                    str_chanlist += " @"
                                else:
                                    str_chanlist += " ."
                            else:
                                str_chanlist += " @"

                            if isVoice:
                                str_chanlist += "+"

                            str_chanlist += cid._nickname

                        else:
                            str_chanlist += " +" + cid._nickname

                else:
                    if nick.lower() not in self._users and cid._MODE_invisible and nick.lower() not in self._operator_entries:
                        pass
                    else:
                        if self.MODE_auditorium:
                            if isOp(nick, self.channelname) or cid._nickname.lower() == nick.lower():
                                str_chanlist = str_chanlist + " " + cid._nickname
                        else:
                            str_chanlist = str_chanlist + " " + cid._nickname

            if str_chanlist != "":
                self._raw_messages.raw(cclientid, "353", cclientid._nickname, self.channelname, str_chanlist[1:])

        self._raw_messages.raw(cclientid, "366", cclientid._nickname, self.channelname)

    def __remuser(self, nick, sendmsg):  # remove users from the user record for this channel
        if nick.lower() in self._users:
            # cclientid = nicknames[nick.lower()]
            cclientid = getUserOBJ(nick.lower())
            if self.channelname in cclientid._watch:
                cclientid._watch.remove(self.channelname)
            if sendmsg:

                if nick.lower() in self._watch:
                    cclientid.send(
                        ":%s!%s@%s PART %s\r\n" %
                        (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname))
                else:
                    for each in list(self._users):
                        # clientid = nicknames[each.lower()]
                        clientid = getUserOBJ(each.lower())
                        if self.MODE_auditorium == False or isOp(
                                clientid._nickname, self.channelname) or isOp(
                            cclientid._nickname, self.channelname) or cclientid == clientid:
                            clientid.send(
                                ":%s!%s@%s PART %s\r\n" %
                                (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname))

            # once a user leaves the channel, they lose their modes, it's now up to access to give them the modes back if enabled
            self.ClearUsersModes(nick.lower())
            if nick.lower() in self._watch:
                self._watch.remove(nick.lower())
            del self._users[nick.lower()]
            return True
        else:
            return False  # return false if user wasn't on the channel to begin with

    def __adduser(self, nick, key=""):
        if nick.lower() in self._users:
            return -1  # return False if user is already in channel
        else:
            cclientid = self._nickname_to_client_mapping_entries[nick.lower()]
            haskey = False
            if self.MODE_authenticatedclients and nick.lower() not in self._operator_entries:
                return 0

            if self.MODE_Adminonly:
                if nick.lower() in self._operator_entries:
                    opid = self._operator_entries[nick.lower()]
                    if opid.operator_level >= 3:
                        cclientid._channels.append(self.channelname)
                        self._users[nick.lower()] = cclientid
                    else:
                        return -4
                else:
                    return -4

            if self.MODE_registeredonly:
                if nick.lower() in self._operator_entries:
                    pass
                else:
                    if cclientid._MODE_register == False:
                        return -6

            if key != "":
                if key == self._prop.ownerkey:
                    haskey = True
                if key == self._prop.hostkey:
                    haskey = True

            if self.MODE_limit:
                if len(self._users) >= myint(
                        self.MODE_limitamount) and nick.lower() not in self._operator_entries and haskey == False:
                    return -3

            if self.MODE_noclones and nick.lower() not in self._operator_entries:
                susers = copy(self._users)
                for each in susers:
                    uid = self._nickname_to_client_mapping_entries[each.lower()]
                    if uid.details[0] == cclientid.details[0]:
                        return -7

            if self.MODE_inviteonly and nick.lower() not in self._operator_entries:
                cid = self._nickname_to_client_mapping_entries[nick.lower()]
                if self.channelname.lower() not in cid._invites and haskey == False:
                    return -2

            if nick.lower() not in self._operator_entries and nick.lower() not in self._op and nick.lower() not in self._owner:
                for each in self.ChannelAccess:
                    if each._level.upper() == "DENY":
                        ret = _Access.MatchAccess(each._mask, cclientid)
                        if ret == 1:
                            _override = False
                            for eachgrant in self.ChannelAccess:
                                if eachgrant._level.upper() != "DENY":
                                    gret = _Access.MatchAccess(eachgrant._mask, cclientid)
                                    if gret == 1:
                                        _override = True
                                        break

                            if _override:
                                break

                            return -5  # no access!!!

            if self.channelname.lower() in cclientid._invites:
                cclientid._invites.remove(self.channelname.lower())
            cclientid._channels.append(self.channelname)
            self._users[nick.lower()] = cclientid
            return 1

    def resetchannel(self, killchan=False):
        if self.MODE_registered or self.MODE_servicechan:
            pass
        elif self._prop.reset != 0 and killchan == False:
            PropResetChannel(self).start()
        else:
            # self._users = {}
            # self._watch = []
            # self._prop = None
            # self._topic = ""
            # self.ChannelAccess = []
            delGlobalChannel(self.channelname.lower())
            # self.channelname = ""
            del self

    def updateuser(self, oldnick, newnick):  # This function will update the user record for this channel
        if oldnick.lower() in self._users:
            if oldnick.lower() in self._op:
                self._op.append(newnick.lower())
            if oldnick.lower() in self._owner:
                self._owner.append(newnick.lower())
            if oldnick.lower() in self._voice:
                self._voice.append(newnick.lower())
            self.ClearUsersModes(oldnick)

            del self._users[oldnick.lower()]
            self._users[newnick.lower()] = getUserOBJ(oldnick.lower())
            return True
        else:
            return False

    def part(self, partuser):
        cclientid = getUserOBJ(partuser.lower())
        if cclientid:
            if self.__remuser(partuser, True) == False:
                self._raw_messages.raw(cclientid, "442", cclientid._nickname, self.channelname)
                return False
            else:
                cclientid._channels.remove(self.channelname)

                if self._prop.onpart != "":
                    iloop = 0
                    numstr = len(self._prop.onpart.split("\\n"))
                    while iloop < numstr:
                        cclientid.send(
                            ":%s NOTICE %s :%s\r\n" %
                            (self.channelname, cclientid._nickname, self._prop.onpart.split("\\n")[iloop]))
                        iloop += 1

                if len(self._users) == 0:
                    self.resetchannel()

                return True

    def quit(self, quituser):
        self.__remuser(quituser, False)

        if len(self._users) == 0:
            self.resetchannel()

    def join(self, joinuser, key=""):
        _Access.CheckChannelExpiry(self)
        _r = self.__adduser(joinuser, key)
        cclientid = getUserOBJ(joinuser.lower())

        if joinuser.lower() not in self._operator_entries and _r != -1 and _r != -4 and _r != 0 and _r != -6:  # opers not affected
            for each in self.ChannelAccess:
                if each._level.upper() != "DENY" and each._level.upper() != "GRANT":
                    ret = _Access.MatchAccess(each._mask, cclientid)
                    if ret == 1:
                        if each._level.upper() == "OWNER":
                            if joinuser.lower() in self._op:
                                self._op.remove(joinuser.lower())
                            if joinuser.lower() not in self._owner:
                                self._owner.append(joinuser.lower())
                            _r = 1
                            break

                        if each._level.upper() == "HOST":

                            if joinuser.lower() in self._owner:
                                break
                            else:
                                if joinuser.lower() not in self._op:
                                    self._op.append(joinuser.lower())
                                _r = 1

                        if each._level.upper() == "VOICE":
                            if joinuser.lower() not in self._voice:
                                self._voice.append(joinuser.lower())
                            _r = 1

        if _r == 1:

            if self.MODE_noircx:
                if joinuser.lower() in self._owner:
                    self._owner.remove(joinuser.lower())
                    if joinuser.lower() not in self._op:
                        self._op.append(joinuser.lower())

            if self.channelname.lower() in cclientid._invites:
                cclientid._invites.remove(self.channelname.lower())
            if self.channelname not in cclientid._channels:
                cclientid._channels.append(self.channelname)
            if joinuser.lower() not in self._users:
                self._users[joinuser.lower()] = cclientid

            keyjoin = 0

            isoper = False
            if joinuser.lower() in self._operator_entries:
                if self.MODE_noircx:
                    if joinuser.lower() not in self._op:
                        self._op.append(joinuser.lower())  # make opers owner of channel automatically
                else:
                    if joinuser.lower() not in self._owner:
                        self._owner.append(joinuser.lower())  # make opers owner of channel automatically

                isoper = True

            if self.channelname in cclientid._watch:
                self._watch.append(joinuser.lower())
                cclientid.send(
                    ":%s!%s@%s JOIN :%s\r\n" %
                    (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname))
            else:
                ChanCopyNames = list(self._users)
                for each in ChanCopyNames:
                    clientid = getUserOBJ(each.lower())
                    if self.MODE_auditorium == False or isOp(
                            clientid._nickname, self.channelname) or isOp(
                        cclientid._nickname, self.channelname) or clientid == cclientid:
                        if isoper or key == self._prop.ownerkey and key != "" or joinuser.lower() in self._owner:
                            keyjoin = 2
                            if clientid._IRCX and self.MODE_noircx == False:
                                clientid.send(
                                    ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +q %s\r\n" %
                                    (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                     server_name, self.channelname, cclientid._nickname))
                            else:
                                clientid.send(
                                    ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +o %s\r\n" %
                                    (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                     server_name, self.channelname, cclientid._nickname))

                        elif key == self._prop.hostkey and key != "" or joinuser.lower() in self._op:
                            clientid.send(
                                ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +o %s\r\n" %
                                (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                 server_name, self.channelname, cclientid._nickname))
                            keyjoin = 1

                        elif joinuser.lower() in self._voice and joinuser.lower() not in self._op and joinuser.lower() not in self._owner:
                            clientid.send(
                                ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +v %s\r\n" %
                                (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                 server_name, self.channelname, cclientid._nickname))
                        else:
                            clientid.send(
                                ":%s!%s@%s JOIN :%s\r\n" %
                                (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname))

                del ChanCopyNames

            if keyjoin == 1:
                if joinuser.lower() not in self._op:
                    self._op.append(joinuser.lower())
            elif keyjoin == 2:
                if self.MODE_noircx:
                    if joinuser.lower() not in self._owner:
                        self._op.append(joinuser.lower())
                else:
                    if joinuser.lower() not in self._owner:
                        self._owner.append(joinuser.lower())

            elif keyjoin == 3:
                if joinuser.lower() not in self._voice:
                    self._voice.append(joinuser.lower())

            if self._topic != "":
                self._raw_messages.raw(cclientid, "332", cclientid._nickname, self.channelname, self._topic)
                self._raw_messages.raw(cclientid, "333", cclientid._nickname, self.channelname, self._topic_nick,
                                 self._topic_time)

            self.sendnames(cclientid._nickname, False, True)

            if self._prop.onjoin != "":
                iloop = 0
                numstr = len(self._prop.onjoin.split("\\n"))
                while iloop < numstr:
                    cclientid.send(
                        ":%s PRIVMSG %s :%s\r\n" %
                        (self.channelname, self.channelname, self._prop.onjoin.split("\\n")[iloop]))
                    iloop += 1
        else:
            k_numeric = ""
            if _r == -1:
                self._raw_messages.raw(cclientid, "927", cclientid._nickname, self.channelname)

            elif _r == -2:
                self._raw_messages.raw(cclientid, "473", cclientid._nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "473"

            elif _r == -3:
                if self.MODE_createclone:

                    newc = self.cloneid.channelname + str(self.cloneindex + 1)

                    if newc.lower() in server_context.channel_entries:  # get rid of any channels that were made before clone rooms were created
                        chanid = server_context.channel_entries[newc.lower()]
                        if chanid.MODE_cloneroom == False:
                            for each in chanid._users:
                                cid = getUserOBJ(each.lower())
                                self._raw_messages.raw(cid, "934", cid._nickname)  # LINK NOTE: sendRawDataHere

                            chanid.resetchannel()
                        else:
                            chanid.join(joinuser)
                            return

                    server_context.channel_entries[newc.lower()] = copy(self)
                    newchan = server_context.channel_entries[newc.lower()]
                    newchan.cloneid = self.cloneid
                    newchan.cloneindex = self.cloneindex + 1
                    newchan.channelname = newc
                    newchan.MODE_cloneroom = True
                    newchan._users = {}
                    newchan.join(joinuser)

                else:
                    self._raw_messages.raw(cclientid, "471", cclientid._nickname, self.channelname)
                    if self.MODE_knock:
                        k_numeric = "471"

            elif _r == -4:
                self._raw_messages.raw(cclientid, "483", cclientid._nickname, self.channelname,
                                 "You are not an Administrator")
                if self.MODE_knock:
                    k_numeric = "483"

            elif _r == -5:
                self._raw_messages.raw(cclientid, "913", cclientid._nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "913"

            elif _r == -6:
                self._raw_messages.raw(cclientid, "477", cclientid._nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "477"

            elif _r == -7:
                self._raw_messages.raw(cclientid, "483", cclientid._nickname, self.channelname,
                                 "User with same address already in channel")
                if self.MODE_knock:
                    k_numeric = "483"

            elif _r == 0:
                self._raw_messages.raw(cclientid, "520", cclientid._nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "520"

            if k_numeric:
                for each in copy(self._users):
                    clientid = getUserOBJ(each)
                    clientid.send(
                        ":%s!%s@%s KNOCK %s %s\r\n" %
                        (cclientid._nickname, cclientid._username, cclientid._hostmask, self.channelname, k_numeric))

    def communicate(self, msguser, nop, msg):
        cclientid = self._nickname_to_client_mapping_entries[msguser.lower()]
        if msguser.lower() in self._users or self.MODE_externalmessages == False:
            sendto = True

            if self.channelname in cclientid._watch:
                self._raw_messages.raw(cclientid, "404", cclientid._nickname, self.channelname, "Cannot send to channel")
                cclientid.send(":" + server_name +
                               " NOTICE SERVER :*** You are watching this channel, you can't participate\r\n")
                sendto = False

            elif self.MODE_moderated:
                if msguser.lower() in self._voice or msguser.lower() in self._op or msguser.lower() in self._owner or msguser.lower() in self._operator_entries:
                    pass
                else:
                    sendto = False
                    self._raw_messages.raw(cclientid, "404", cclientid._nickname, self.channelname, "Cannot send to channel")

            elif self.MODE_nocolour:
                if chr(3) in msg or chr(2) in msg or "\x1F" in msg:
                    self._raw_messages.raw(cclientid, "404", cclientid._nickname, self.channelname, "Cannot send to channel")
                    sendto = False

            if self.MODE_gagonban:
                if self.isBanned(cclientid):
                    self._raw_messages.raw(cclientid, "404", cclientid._nickname, self.channelname,
                                     "Cannot send to channel whilst banned")
                    sendto = False

            if self.MODE_profanity:
                foundprofanity = False
                for all in profanity:
                    tmsg = re.compile(all.lower().replace(".", r"\.").replace("*", "(.+|)"))
                    if tmsg.match(msg.lower()):
                        foundprofanity = True
                        break

                if foundprofanity:
                    sendto = False
                    self._raw_messages.raw(cclientid, "404", cclientid._nickname, self.channelname,
                                     "Cannot send to channel (filter in use)")
                    cclientid.send(":" + server_name +
                                   " NOTICE SERVER :*** A filter is in use, your last message was blocked\r\n")

            if sendto:
                for each in copy(self._users):
                    clientid = self._nickname_to_client_mapping_entries[each.lower()]
                    if clientid != cclientid:
                        if self.MODE_auditorium == False or isOp(
                                clientid._nickname, self.channelname) or isOp(
                            cclientid._nickname, self.channelname):
                            if self.MODE_stripcolour:
                                msg = re.sub("\x03[0-9]{1,2}(\,[0-9]{1,2}|)|\x1F|\x02", "", msg)

                            clientid.send(
                                ":%s!%s@%s %s %s :%s\r\n" %
                                (cclientid._nickname, cclientid._username, cclientid._hostmask, nop.upper(),
                                 self.channelname, msg))

            if "PRIVMSG" not in FloodingExempt:
                if cclientid._nickname.lower() not in self._op and cclientid._nickname.lower() not in self._owner and cclientid._nickname.lower() not in self._operator_entries:
                    time.sleep(0.8)
                else:
                    time.sleep(0.18)

        else:
            self._raw_messages.raw(cclientid, "442", cclientid._nickname, self.channelname)
