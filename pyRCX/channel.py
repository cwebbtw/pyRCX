import re
import threading
import time

from copy import copy

from .helpers import int_or_zero
from .raw import Raw
from .server_context import ServerContext

import pyRCX.access as access_helper


class ChannelProperties:
    """
    Represents the properties of a given channel

    This data must be serializable
    """

    def __init__(self, name, account):
        self.name = name
        self.profanity = []
        self.ownerkey = ""
        self.hostkey = ""
        self.memberkey = ""
        self.reset = 0
        self.client = ""
        self.subject = ""
        self.creation = str(int(time.time()))
        if "nickname" in dir(account):
            self.account = True
            self.account_name = account.nickname
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


class _PropResetChannel(threading.Thread):
    """
    This needs to be removed
    """

    def __init__(self, server_context, channel):
        self.server_context = server_context
        self.channel = channel
        threading.Thread.__init__(self)

    def run(self):
        try:
            exptime = int(time.time()) + self.channel._prop.reset

            while int(time.time()) <= exptime and self.channel.channelname != "":
                if len(self.channel._users) != 0:
                    return

                time.sleep(0.1)

            if len(self.channel._users) == 0:
                self.channel._users = {}
                self.channel._watch = []
                self.channel._prop = None
                self.channel._topic = ""
                self.channel.ChannelAccess = []

                self.server_context.remove_channel(self.channel.channelname)
                self.channel.channelname = ""
        except:
            pass


class Channel:
    def __init__(self, server_context: ServerContext, raw_messages: Raw, channelname, joinuser, creationmodes=""):
        self._server_context = server_context
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
                    ":%s 706 %s :Channel name is not valid\r\n" % (
                        self._configuration.server_name, cclientid.nickname))

            server_context.remove_channel(self.channelname)

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
                    self._owner = [cclientid.nickname.lower()]
                else:
                    self._op = [cclientid.nickname.lower()]

            if joinuser != "":
                self._prop = ChannelProperties(channelname, cclientid)  # create instance of prop class
            else:
                self._prop = ChannelProperties(channelname, self._configuration.server_name)

            if self.channelname[0] == "&":
                self.localChannel = True
            if len(self.channelname) >= 2:
                if self.channelname[0] + self.channelname[1] == "%&":
                    self.localChannel = True

            self._setupModes(creationmodes)

            if joinuser != "":
                cclientid._channels.append(self.channelname)
                cclientid.send(
                    ":%s!%s@%s JOIN :%s\r\n" %
                    (cclientid.nickname, cclientid._username, cclientid._hostmask, channelname))
                self.sendnames(cclientid.nickname, True)

    def has_channel_permissions(self, nickname):  # return true or false depending upon whether nick is oper
        if nickname.lower() in self._op or nickname.lower() in self._owner or self._server_context.get_operator(
                nickname):
            return True
        else:
            return False

    def _setupModes(self, creationmodes_full):
        creationmodes = creationmodes_full.split(" ")[0]
        if "Z" in creationmodes:
            self.MODE_noircx = True
        if "m" in creationmodes:
            self.MODE_moderated = True
        if "d" in creationmodes:
            self.MODE_createclone = True
        if "K" in creationmodes:
            self.MODE_noclones = True
        if "e" in creationmodes:
            self.MODE_cloneroom = True
        if "M" in creationmodes and self.MODE_noircx == False:
            self.MODE_ownersetmode = True
        if "G" in creationmodes:
            self.MODE_gagonban = True
        if "Q" in creationmodes and self.MODE_noircx == False:
            self.MODE_ownerkick = True
        if "A" in creationmodes:
            self.MODE_Adminonly = True
        if "f" in creationmodes:
            self.MODE_profanity = True
        if "N" in creationmodes:
            self.MODE_servicechan = True
        if "P" in creationmodes and self.MODE_noircx == False:
            self.MODE_ownersetprop = True
        if "X" in creationmodes:
            self.MODE_ownersetaccess = True
        if "R" in creationmodes:
            self.MODE_registeredonly = True
        if "w" in creationmodes:
            self.MODE_whisper = True
        if "s" in creationmodes:
            self.MODE_secret = True
        if "S" in creationmodes:
            self.MODE_nomodechanges = True
        if "h" in creationmodes and "s" not in creationmodes and "p" not in creationmodes:
            self.MODE_hidden = True
        if "T" in creationmodes and self.MODE_noircx == False:
            self.MODE_ownertopic = True
        if "t" in creationmodes and "T" not in creationmodes:
            self.MODE_optopic = True
        if "n" in creationmodes:
            self.MODE_externalmessages = True
        if "r" in creationmodes:
            self.MODE_registered = True
        if "x" in creationmodes:
            self.MODE_auditorium = True
        if "a" in creationmodes:
            self.MODE_authenticatedclients = True
        if "p" in creationmodes and "s" not in creationmodes and "h" not in creationmodes:
            self.MODE_private = True
        if "c" in creationmodes:
            self.MODE_nocolour = True
        if "C" in creationmodes and "c" not in creationmodes:
            self.MODE_stripcolour = True
        if "u" in creationmodes:
            self.MODE_knock = True
        if "l" in creationmodes or "k" in creationmodes:
            data_limit = str(int_or_zero(creationmodes_full.split(" ")[1]))
            data_key = creationmodes_full.split(" ")[1]
            if "l" in creationmodes and "k" in creationmodes:
                if creationmodes.find("l") > creationmodes.find("k"):
                    data_key = creationmodes_full.split(" ")[1]
                    data_limit = str(int_or_zero(creationmodes_full.split(" ")[2]))
                else:
                    data_key = creationmodes_full.split(" ")[2]
                    data_limit = str(int_or_zero(creationmodes_full.split(" ")[1]))

            if "l" in creationmodes:
                self.MODE_limit = True
                self.MODE_limitamount = data_limit

            if "k" in creationmodes:
                self.MODE_key = data_key

    def __validate(self, channelname, joinuser):
        channel_prefix = "(" + "|".join(self._configuration.channel_prefix.split(",")) + ")"
        p = re.compile(f"^{channel_prefix}[\u0021-\u002B\u002E-\u00FF\-]{{0,128}}$")

        operator_level = 0
        if joinuser.lower() in self._operator_entries:
            operator_level = self._operator_entries[joinuser.lower()].operator_level

        return p.match(channelname) is not None and not self._configuration.filtering.filter(channelname, "chan",
                                                                                             operator_level)

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

        access_helper.CheckChannelExpiry(self)
        if cid.nickname.lower() in self._operator_entries or self.has_channel_permissions(cid.nickname):
            return False
        for each in self.ChannelAccess:
            if each._level.upper() == "DENY":
                ret = access_helper.MatchAccess(self._server_context, each._mask, cid)
                if ret == 1:
                    _override = False
                    for eachgrant in self.ChannelAccess:
                        if eachgrant._level.upper() != "DENY":
                            gret = access_helper.MatchAccess(self._server_context, eachgrant._mask, cid)
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
        users_in_channel = self._users.keys()
        for each in users_in_channel:
            each_channel_user = self._server_context.get_user(each)
            if self.MODE_auditorium == False or self.has_channel_permissions(
                    each_channel_user.nickname) or self.has_channel_permissions(
                nick.nickname) or self.has_channel_permissions(
                knick.nickname) or each_channel_user.nickname.lower() == knick.lower():
                # This is showing other people that are allowed to see the kick that the user is kicked
                each_channel_user.send(
                    ":%s!%s@%s KICK %s %s :%s\r\n" %
                    (nick.nickname, nick._username, nick._hostmask, self.channelname, knick, kickmsg))

        if self.channelname in clientid._channels:
            clientid._channels.remove(self.channelname)
        self.__remuser(knick, False)

        if self._prop.onpart != "":
            iloop = 0
            numstr = len(self._prop.onpart.split("\\n"))
            while iloop < numstr:
                clientid.send(
                    ":%s NOTICE %s :%s\r\n" %
                    (self.channelname, clientid.nickname, self._prop.onpart.split("\\n")[iloop]))
                iloop += 1

        if len(self._users) == 0:
            self.resetchannel()

    def should_send_names(self):
        return self.MODE_secret or self.MODE_servicechan or self.MODE_hidden or self.MODE_private

    def visible_in_list(self):
        return not self.MODE_secret and not self.MODE_private

    def sendnames(self, nick, owner=False, sendwatch=False):
        cclientid = self._server_context.get_user(nick)
        str_chanlist = ""
        iloop = 0
        if self.should_send_names() or nick.lower() in self._users or nick.lower() in self._operator_entries:
            for each in self._users.keys():
                cid = self._server_context.get_user(each)
                if cid:
                    iloop += 1
                    if iloop == 20:
                        self._raw_messages.raw(cclientid, "353", cclientid.nickname, self.channelname,
                                               str_chanlist[1:])
                        str_chanlist = ""
                        iloop = 0

                    if self.channelname in cid._watch:
                        if cclientid == cid:
                            if cclientid._IRCX and self.MODE_noircx == False:
                                str_chanlist += " ."
                            else:
                                str_chanlist += " @"

                            if cid.nickname.lower() in self._voice:
                                str_chanlist += "+"

                            str_chanlist += cid.nickname

                    elif cid.nickname.lower() in self._owner or cid.nickname.lower() in self._op or cid.nickname.lower() in self._voice:

                        if nick.lower() not in self._users and cid._MODE_invisible and nick.lower() not in self._operator_entries:
                            pass
                        else:
                            isVoice = False
                            if cid.nickname.lower() in self._voice:
                                isVoice = True

                            if cid.nickname.lower() in self._op:
                                str_chanlist += " @"
                                if isVoice:
                                    str_chanlist += "+"

                                str_chanlist += cid.nickname

                            elif cid.nickname.lower() in self._owner:
                                if cclientid._IRCX:
                                    if self.MODE_noircx:
                                        str_chanlist += " @"
                                    else:
                                        str_chanlist += " ."
                                else:
                                    str_chanlist += " @"

                                if isVoice:
                                    str_chanlist += "+"

                                str_chanlist += cid.nickname

                            else:
                                str_chanlist += " +" + cid.nickname

                    else:
                        if nick.lower() not in self._users and cid._MODE_invisible and nick.lower() not in self._operator_entries:
                            pass
                        else:
                            if self.MODE_auditorium:
                                if self.has_channel_permissions(nick) or cid.nickname.lower() == nick.lower():
                                    str_chanlist = str_chanlist + " " + cid.nickname
                            else:
                                str_chanlist = str_chanlist + " " + cid.nickname

            if str_chanlist != "":
                self._raw_messages.raw(cclientid, "353", cclientid.nickname, self.channelname, str_chanlist[1:])

        self._raw_messages.raw(cclientid, "366", cclientid.nickname, self.channelname)

    def __remuser(self, nick, sendmsg):  # remove users from the user record for this channel
        cclientid = self._server_context.get_user(nick)
        if cclientid is not None:
            if self.channelname in cclientid._watch:
                cclientid._watch.remove(self.channelname)
            if sendmsg:

                if nick.lower() in self._watch:
                    cclientid.send(
                        ":%s!%s@%s PART %s\r\n" %
                        (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname))
                else:
                    for each in list(self._users):
                        clientid = self._server_context.get_user(each)
                        if clientid is not None:
                            if self.MODE_auditorium == False or self.has_channel_permissions(
                                    clientid.nickname) or self.has_channel_permissions(
                                cclientid.nickname) or cclientid == clientid:
                                clientid.send(
                                    ":%s!%s@%s PART %s\r\n" %
                                    (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname))

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
                if len(self._users) >= int_or_zero(
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
                        ret = access_helper.MatchAccess(self._server_context, each._mask, cclientid)
                        if ret == 1:
                            _override = False
                            for eachgrant in self.ChannelAccess:
                                if eachgrant._level.upper() != "DENY":
                                    gret = access_helper.MatchAccess(self._server_context, eachgrant._mask, cclientid)
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
            _PropResetChannel(self._server_context, self).start()
        else:
            self._server_context.remove_channel(self.channelname)

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
            self._users[newnick.lower()] = self._server_context.get_user(oldnick)
            return True
        else:
            return False

    def part(self, parting_nickname):
        parting_user = self._server_context.get_user(parting_nickname)
        if parting_user:
            if self.__remuser(parting_nickname, True) == False:
                self._raw_messages.raw(parting_user, "442", parting_user.nickname, self.channelname)
                return False
            else:
                parting_user._channels.remove(self.channelname)

                if self._prop.onpart != "":
                    iloop = 0
                    numstr = len(self._prop.onpart.split("\\n"))
                    while iloop < numstr:
                        parting_user.send(
                            ":%s NOTICE %s :%s\r\n" %
                            (self.channelname, parting_user.nickname, self._prop.onpart.split("\\n")[iloop]))
                        iloop += 1

                if len(self._users) == 0:
                    self.resetchannel()

                return True

    def quit(self, quituser):
        self.__remuser(quituser, False)

        if len(self._users) == 0:
            self.resetchannel()

    def join(self, joinuser, key=""):
        access_helper.CheckChannelExpiry(self)
        _r = self.__adduser(joinuser, key)

        cclientid = self._server_context.get_user(joinuser)

        if joinuser.lower() not in self._operator_entries and _r != -1 and _r != -4 and _r != 0 and _r != -6:  # opers not affected
            for each in self.ChannelAccess:
                if each._level.upper() != "DENY" and each._level.upper() != "GRANT":
                    ret = access_helper.MatchAccess(self._server_context, each._mask, cclientid)
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
                    (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname))
            else:
                ChanCopyNames = list(self._users)
                for each in ChanCopyNames:
                    clientid = self._server_context.get_user(each)
                    if self.MODE_auditorium == False or self.has_channel_permissions(
                            clientid.nickname) or self.has_channel_permissions(
                        cclientid.nickname) or clientid == cclientid:
                        if isoper or key == self._prop.ownerkey and key != "" or joinuser.lower() in self._owner:
                            keyjoin = 2
                            if clientid._IRCX and self.MODE_noircx == False:
                                clientid.send(
                                    ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +q %s\r\n" %
                                    (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                     self._configuration.server_name, self.channelname, cclientid.nickname))
                            else:
                                clientid.send(
                                    ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +o %s\r\n" %
                                    (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                     self._configuration.server_name, self.channelname, cclientid.nickname))

                        elif key == self._prop.hostkey and key != "" or joinuser.lower() in self._op:
                            clientid.send(
                                ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +o %s\r\n" %
                                (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                 self._configuration.server_name, self.channelname, cclientid.nickname))
                            keyjoin = 1

                        elif joinuser.lower() in self._voice and joinuser.lower() not in self._op and joinuser.lower() not in self._owner:
                            clientid.send(
                                ":%s!%s@%s JOIN :%s\r\n:%s MODE %s +v %s\r\n" %
                                (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                 self._configuration.server_name, self.channelname, cclientid.nickname))
                        else:
                            clientid.send(
                                ":%s!%s@%s JOIN :%s\r\n" %
                                (cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname))

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
                self._raw_messages.raw(cclientid, "332", cclientid.nickname, self.channelname, self._topic)
                self._raw_messages.raw(cclientid, "333", cclientid.nickname, self.channelname, self._topic_nick,
                                       self._topic_time)

            self.sendnames(cclientid.nickname, False, True)

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
                self._raw_messages.raw(cclientid, "927", cclientid.nickname, self.channelname)

            elif _r == -2:
                self._raw_messages.raw(cclientid, "473", cclientid.nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "473"

            elif _r == -3:
                if self.MODE_createclone:

                    newc = self.cloneid.channelname + str(self.cloneindex + 1)

                    chanid = self._server_context.get_channel(newc)
                    if chanid:  # get rid of any channels that were made before clone rooms were created
                        if chanid.MODE_cloneroom == False:
                            for each in chanid._users:
                                cid = self._server_context.get_user(each)
                                if cid is not None:
                                    self._raw_messages.raw(cid, "934", cid.nickname)  # LINK NOTE: sendRawDataHere

                            chanid.resetchannel()
                        else:
                            chanid.join(joinuser)
                            return

                    newchan = copy(self)
                    self._server_context.add_channel(newc, newchan)
                    newchan.cloneid = self.cloneid
                    newchan.cloneindex = self.cloneindex + 1
                    newchan.channelname = newc
                    newchan.MODE_cloneroom = True
                    newchan._users = {}
                    newchan.join(joinuser)

                else:
                    self._raw_messages.raw(cclientid, "471", cclientid.nickname, self.channelname)
                    if self.MODE_knock:
                        k_numeric = "471"

            elif _r == -4:
                self._raw_messages.raw(cclientid, "483", cclientid.nickname, self.channelname,
                                       "You are not an Administrator")
                if self.MODE_knock:
                    k_numeric = "483"

            elif _r == -5:
                self._raw_messages.raw(cclientid, "913", cclientid.nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "913"

            elif _r == -6:
                self._raw_messages.raw(cclientid, "477", cclientid.nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "477"

            elif _r == -7:
                self._raw_messages.raw(cclientid, "483", cclientid.nickname, self.channelname,
                                       "User with same address already in channel")
                if self.MODE_knock:
                    k_numeric = "483"

            elif _r == 0:
                self._raw_messages.raw(cclientid, "520", cclientid.nickname, self.channelname)
                if self.MODE_knock:
                    k_numeric = "520"

            if k_numeric:
                for each in self._users:
                    each_user = self._server_context.get_user(each)
                    if each_user is not None:
                        each_user.send(
                            ":%s!%s@%s KNOCK %s %s\r\n" %
                            (
                                cclientid.nickname, cclientid._username, cclientid._hostmask, self.channelname,
                                k_numeric))

    def communicate(self, msguser, nop, msg):
        cclientid = self._nickname_to_client_mapping_entries[msguser.lower()]
        if msguser.lower() in self._users or self.MODE_externalmessages == False:
            sendto = True

            if self.channelname in cclientid._watch:
                self._raw_messages.raw(cclientid, "404", cclientid.nickname, self.channelname,
                                       "Cannot send to channel")
                cclientid.send(":" + self._configuration.server_name +
                               " NOTICE SERVER :*** You are watching this channel, you can't participate\r\n")
                sendto = False

            elif self.MODE_moderated:
                if msguser.lower() in self._voice or msguser.lower() in self._op or msguser.lower() in self._owner or msguser.lower() in self._operator_entries:
                    pass
                else:
                    sendto = False
                    self._raw_messages.raw(cclientid, "404", cclientid.nickname, self.channelname,
                                           "Cannot send to channel")

            elif self.MODE_nocolour:
                if chr(3) in msg or chr(2) in msg or "\x1F" in msg:
                    self._raw_messages.raw(cclientid, "404", cclientid.nickname, self.channelname,
                                           "Cannot send to channel")
                    sendto = False

            if self.MODE_gagonban:
                if self.isBanned(cclientid):
                    self._raw_messages.raw(cclientid, "404", cclientid.nickname, self.channelname,
                                           "Cannot send to channel whilst banned")
                    sendto = False

            if self.MODE_profanity:
                foundprofanity = False
                for all in self._configuration.profanity_entries:
                    tmsg = re.compile(all.lower().replace(".", r"\.").replace("*", "(.+|)"))
                    if tmsg.match(msg.lower()):
                        foundprofanity = True
                        break

                if foundprofanity:
                    sendto = False
                    self._raw_messages.raw(cclientid, "404", cclientid.nickname, self.channelname,
                                           "Cannot send to channel (filter in use)")
                    cclientid.send(":" + self._configuration.server_name +
                                   " NOTICE SERVER :*** A filter is in use, your last message was blocked\r\n")

            if sendto:
                for each in copy(self._users):
                    clientid = self._nickname_to_client_mapping_entries[each.lower()]
                    if clientid != cclientid:
                        if self.MODE_auditorium == False or self.has_channel_permissions(
                                clientid.nickname) or self.has_channel_permissions(
                            cclientid.nickname):
                            if self.MODE_stripcolour:
                                msg = re.sub("\x03[0-9]{1,2}(\,[0-9]{1,2}|)|\x1F|\x02", "", msg)

                            clientid.send(
                                ":%s!%s@%s %s %s :%s\r\n" %
                                (cclientid.nickname, cclientid._username, cclientid._hostmask, nop.upper(),
                                 self.channelname, msg))

            if "PRIVMSG" not in self._configuration.flooding_exempt_commands:
                if cclientid.nickname.lower() not in self._op and cclientid.nickname.lower() not in self._owner and cclientid.nickname.lower() not in self._operator_entries:
                    time.sleep(0.8)
                else:
                    time.sleep(0.18)

        else:
            self._raw_messages.raw(cclientid, "442", cclientid.nickname, self.channelname)

    def _validate(self, property):
        p = re.compile("^[\x21-\xFF]{1,32}$")
        if p.match(property) is None:
            return False
        else:
            return True

    def change_event_message(self, user, param3, sData, onmsg):
        if user.nickname.lower() in self._users:
            if user.nickname.lower() in self._op or user.nickname.lower() in self._owner:
                if sData.__len__() > 256:
                    self._raw_messages.raw(user, "905", user.nickname, self.channelname)
                else:
                    stroj = sData
                    if stroj[0] != ":":
                        stroj = param3
                    else:
                        stroj = stroj[1:]

                    if onmsg.upper() == "ONJOIN":
                        self._prop.onjoin = stroj
                    elif onmsg.upper() == "ONPART":
                        self._prop.onpart = stroj

                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s PROP %s %s :%s\r\n" %
                            (user.nickname, user._username, user._hostmask, self.channelname, onmsg, stroj))
            else:
                self._raw_messages.raw(user, "482", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "442", user.nickname, self.channelname)

    def change_client(self, user, sData):
        if user.nickname.lower() in self._users:
            if user.nickname.lower() in self._op or user.nickname.lower() in self._owner:
                if sData.__len__() > 32:
                    self._raw_messages.raw(user, "905", user.nickname, self.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]

                    self._prop.client = sData
                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s PROP %s CLIENT :%s\r\n" %
                            (user.nickname, user._username, user._hostmask, self.channelname, sData))
            else:
                self._raw_messages.raw(user, "482", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "442", user.nickname, self.channelname)

    def change_topic(self, user, content):
        if content.__len__() > 512:
            self._raw_messages.raw(user, "905", user.nickname, self.channelname)
        else:
            if self.MODE_optopic == False or user.nickname.lower() in self._op or user.nickname.lower() in self._owner:
                if self.MODE_ownertopic and user.nickname.lower() not in self._owner:
                    self._raw_messages.raw(user, "485", user.nickname, self.channelname)
                else:
                    self._topic = content[1:] if content.startswith(":") else content.split(" ")[0]
                    if self._topic == "":
                        self._topic = ""
                    else:
                        self._topic_nick = user.nickname
                        self._topic_time = int(time.time())

                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s TOPIC %s :%s\r\n" %
                            (user.nickname, user._username, user._hostmask, self.channelname, self._topic))
            else:
                self._raw_messages.raw(user, "482", user.nickname, self.channelname)

    def change_subject(self, user, sData):
        if user.nickname.lower() in self._users:
            if user.nickname.lower() in self._op or user.nickname.lower() in self._owner:
                if sData.__len__() > 32:
                    self._raw_messages.raw(user, "905", user.nickname, self.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]
                    self._prop.subject = sData
                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s PROP %s SUBJECT :%s\r\n" %
                            (user.nickname, user._username, user._hostmask, self.channelname, sData))
            else:
                self._raw_messages.raw(user, "482", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "442", user.nickname, self.channelname)

    def change_lag(self, user, sData):
        if user.nickname.lower() in self._users:
            if user.nickname.lower() in self._op or user.nickname.lower() in self._owner:
                if int_or_zero(sData) >= 5 or int_or_zero(sData) < -1 or int_or_zero(sData) == 0 and sData != "0":
                    self._raw_messages.raw(user, "905", user.nickname, self.channelname)
                else:
                    if int_or_zero(sData) == 0:
                        sData = 0
                    self._prop.lag = int_or_zero(sData)
                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        cid.send(":%s!%s@%s PROP %s LAG :%s\r\n" % (user.nickname, user._username,
                                                                    user._hostmask, self.channelname,
                                                                    str(int_or_zero(sData))))
            else:
                self._raw_messages.raw(user, "482", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "442", user.nickname, self.channelname)

    def change_language(self, user, sData):
        if user.nickname.lower() in self._users:
            if user.nickname.lower() in self._op or user.nickname.lower() in self._owner:
                if int_or_zero(sData) >= 65535 or int_or_zero(sData) < -1 or int_or_zero(
                        sData) == 0 and sData != "0" and sData != ":":
                    self._raw_messages.raw(user, "905", user.nickname, self.channelname)
                else:
                    if sData == ":":
                        self._prop.language = ""
                    else:
                        self._prop.language = int_or_zero(sData)

                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        cid.send(":%s!%s@%s PROP %s LANGUAGE :%s\r\n" % (user.nickname, user._username,
                                                                         user._hostmask, self.channelname,
                                                                         str(self._prop.language)))
            else:
                self._raw_messages.raw(user, "482", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "442", user.nickname, self.channelname)

    def change_name(self, user, sData):
        if user.nickname.lower() in self._server_context.operator_entries:
            opid = self._server_context.operator_entries[user.nickname.lower()]
            if opid.operator_level > 2:
                if sData.lower() == self.channelname.lower():
                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        cid._channels.remove(self.channelname)
                        cid._channels.append(sData)
                        cid.send(
                            ":%s!%s@%s PROP %s NAME :%s\r\n" %
                            (user.nickname, user._username, user._hostmask, self.channelname, sData))

                    self.channelname = sData
                else:
                    self._raw_messages.raw(user, "908", user.nickname)
            else:
                self._raw_messages.raw(user, "908", user.nickname)
        else:
            self._raw_messages.raw(user, "908", user.nickname)

    def change_hostkey(self, user, sData):
        if user.nickname.lower() in self._users:
            if user.nickname.lower() in self._owner:
                if not self._validate(sData):
                    self._raw_messages.raw(user, "905", user.nickname, self.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]

                    self._prop.hostkey = sData
                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        if each.lower() in self._owner:
                            cid.send(
                                ":%s!%s@%s PROP %s HOSTKEY :%s\r\n" %
                                (user.nickname, user._username, user._hostmask, self.channelname, sData))
            else:
                self._raw_messages.raw(user, "485", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "442", user.nickname, self.channelname)

    def change_memberkey(self, user, sData):
        if user.nickname.lower() in self._op or user.nickname.lower() in self._owner:
            if len(sData) <= 16:
                if sData == ":":
                    sData = ""
                if sData != "" and sData[0] == ":":
                    sData = sData[1:]

                self.MODE_key = str(sData)
                for each in self._users:
                    cclientid = self._server_context.nickname_to_client_mapping_entries[each]
                    if sData == "":
                        cclientid.send(
                            ":%s!%s@%s MODE %s -k\r\n" %
                            (user.nickname, user._username, user._hostmask, self.channelname))
                    else:
                        cclientid.send(
                            ":%s!%s@%s MODE %s +k %s\r\n" %
                            (user.nickname, user._username, user._hostmask, self.channelname, sData))
            else:
                self._raw_messages.raw(user, "905", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "482", user.nickname, self.channelname)

    def change_ownerkey(self, user, sData):
        if user.nickname.lower() in self._users:
            if user.nickname.lower() in self._owner:
                if not self._validate(sData):
                    self._raw_messages.raw(user, "905", user.nickname, self.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]

                    self._prop.ownerkey = sData

                    time.sleep(0.2)

                    for each in self._users:
                        cid = self._server_context.nickname_to_client_mapping_entries[each]
                        if each.lower() in self._owner:
                            cid.send(":%s!%s@%s PROP %s OWNERKEY :%s\r\n" %
                                     (user.nickname, user._username, user._hostmask, self.channelname, sData))

                    time.sleep(0.2)  # let people have fun!

            else:
                self._raw_messages.raw(user, "485", user.nickname, self.channelname)
        else:
            self._raw_messages.raw(user, "442", user.nickname, self.channelname)

    def change_reset(self, user, sData):
        if user.nickname.lower() in self._server_context.operator_entries or user.nickname.lower() in self._owner:
            b = True
            r = int_or_zero(sData)
            if r == 0 and sData == "0":
                self._prop.reset = 0
            elif 120 >= r > -1:
                self._prop.reset = r
            else:
                self._raw_messages.raw(user, "906", user.nickname, sData)
                b = False

            if b:
                for each in self._users:
                    cid = self._server_context.nickname_to_client_mapping_entries[each]
                    cid.send(":%s!%s@%s PROP %s RESET :%d\r\n" % (user.nickname, user._username,
                                                                  user._hostmask, self.channelname,
                                                                  self._prop.reset))
        else:
            self._raw_messages.raw(user, "485", user.nickname, self.channelname)
