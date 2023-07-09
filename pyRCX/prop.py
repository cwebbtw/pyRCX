import re
import time


class Prop:
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
        if "_nickname" in dir(account):
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

    def validate(self, property):
        p = re.compile("^[\x21-\xFF]{1,32}$")
        if p.match(property) == None:
            return False
        else:
            return True

    def _onmessage(self, chanid, _self, param3, sData, onmsg):
        if _self.nickname.lower() in chanid._users:
            if _self.nickname.lower() in chanid._op or _self.nickname.lower() in chanid._owner:
                if sData.__len__() > 256:
                    raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
                else:
                    stroj = sData
                    if stroj[0] != ":":
                        stroj = param3
                    else:
                        stroj = stroj[1:]

                    if onmsg.upper() == "ONJOIN":
                        chanid._prop.onjoin = stroj
                    elif onmsg.upper() == "ONPART":
                        chanid._prop.onpart = stroj

                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s PROP %s %s :%s\r\n" %
                            (_self.nickname, _self._username, _self._hostmask, chanid.channelname, onmsg, stroj))
            else:
                raw_messages.raw(_self, "482", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(_self, "442", _self.nickname, chanid.channelname)

    def _client(self, chanid, _self, sData):
        if _self.nickname.lower() in chanid._users:
            if _self.nickname.lower() in chanid._op or _self.nickname.lower() in chanid._owner:
                if sData.__len__() > 32:
                    raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]

                    chanid._prop.client = sData
                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s PROP %s CLIENT :%s\r\n" %
                            (_self.nickname, _self._username, _self._hostmask, chanid.channelname, sData))
            else:
                raw_messages.raw(_self, "482", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(_self, "442", _self.nickname, chanid.channelname)

    def _topic(self, chanid, _self, sData, strd):
        if strd.__len__() > 512:
            raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
        else:
            dotopic = False

            if chanid.MODE_optopic == False or _self.nickname.lower() in chanid._op or _self.nickname.lower() in chanid._owner:
                dotopic = True

            if dotopic:
                if chanid.MODE_ownertopic and _self.nickname.lower() not in chanid._owner:
                    raw_messages.raw(_self, "485", self._nickname, chanid.channelname)
                else:
                    chanid._topic = sData
                    if chanid._topic[0] == ":":
                        chanid._topic = strd
                    if chanid._topic == "":
                        chanid._topic = ""
                    else:
                        chanid._topic_nick = _self.nickname
                        chanid._topic_time = int(GetEpochTime())

                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s TOPIC %s :%s\r\n" %
                            (_self.nickname, _self._username, _self._hostmask, chanid.channelname, chanid._topic))
            else:
                raw_messages.raw(_self, "482", _self.nickname, chanid.channelname)

    def _subject(self, chanid, _self, sData):
        if _self.nickname.lower() in chanid._users:
            if _self.nickname.lower() in chanid._op or _self.nickname.lower() in chanid._owner:
                if sData.__len__() > 32:
                    raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]
                    chanid._prop.subject = sData
                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        cid.send(
                            ":%s!%s@%s PROP %s SUBJECT :%s\r\n" %
                            (_self.nickname, _self._username, _self._hostmask, chanid.channelname, sData))
            else:
                raw_messages.raw(_self, "482", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(_self, "442", _self.nickname, chanid.channelname)

    def _lag(self, chanid, _self, sData):
        if _self.nickname.lower() in chanid._users:
            if _self.nickname.lower() in chanid._op or _self.nickname.lower() in chanid._owner:
                if myint(sData) >= 5 or myint(sData) < -1 or myint(sData) == 0 and sData != "0":
                    raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
                else:
                    if myint(sData) == 0:
                        sData = 0
                    chanid._prop.lag = myint(sData)
                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        cid.send(":%s!%s@%s PROP %s LAG :%s\r\n" % (_self.nickname, _self._username,
                                                                    _self._hostmask, chanid.channelname,
                                                                    str(myint(sData))))
            else:
                raw_messages.raw(_self, "482", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(_self, "442", _self.nickname, chanid.channelname)

    def _language(self, chanid, _self, sData):
        if _self.nickname.lower() in chanid._users:
            if _self.nickname.lower() in chanid._op or _self.nickname.lower() in chanid._owner:
                if myint(sData) >= 65535 or myint(sData) < -1 or myint(sData) == 0 and sData != "0" and sData != ":":
                    raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
                else:
                    if sData == ":":
                        chanid._prop.language = ""
                    else:
                        chanid._prop.language = myint(sData)

                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        cid.send(":%s!%s@%s PROP %s LANGUAGE :%s\r\n" % (_self.nickname, _self._username,
                                                                         _self._hostmask, chanid.channelname,
                                                                         str(chanid._prop.language)))
            else:
                raw_messages.raw(_self, "482", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(_self, "442", _self.nickname, chanid.channelname)

    def _name(self, chanid, _self, sData):
        if _self.nickname.lower() in server_context.operator_entries:
            opid = server_context.operator_entries[_self.nickname.lower()]
            if opid.operator_level > 2:
                if sData.lower() == chanid.channelname.lower():
                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        cid._channels.remove(chanid.channelname)
                        cid._channels.append(sData)
                        cid.send(
                            ":%s!%s@%s PROP %s NAME :%s\r\n" %
                            (_self.nickname, _self._username, _self._hostmask, chanid.channelname, sData))

                    chanid.channelname = sData
                else:
                    raw_messages.raw(_self, "908", _self.nickname)
            else:
                raw_messages.raw(_self, "908", _self.nickname)
        else:
            raw_messages.raw(_self, "908", _self.nickname)

    def _hostkey(self, chanid, _self, sData):
        if _self.nickname.lower() in chanid._users:
            if _self.nickname.lower() in chanid._owner:
                if chanid._prop.validate(sData) == False:
                    raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]

                    chanid._prop.hostkey = sData
                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        if each.lower() in chanid._owner:
                            cid.send(
                                ":%s!%s@%s PROP %s HOSTKEY :%s\r\n" %
                                (_self.nickname, _self._username, _self._hostmask, chanid.channelname, sData))
            else:
                raw_messages.raw(_self, "485", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(_self, "442", _self.nickname, chanid.channelname)

    def _memberkey(self, chanid, _self, sData):
        if _self.nickname.lower() in chanid._op or _self.nickname.lower() in chanid._owner:
            if len(sData) <= 16:
                if sData == ":":
                    sData = ""
                if sData != "" and sData[0] == ":":
                    sData = sData[1:]

                chanid.MODE_key = str(sData)
                for each in chanid._users:
                    cclientid = server_context.nickname_to_client_mapping_entries[each]
                    if sData == "":
                        cclientid.send(
                            ":%s!%s@%s MODE %s -k\r\n" %
                            (_self.nickname, _self._username, _self._hostmask, chanid.channelname))
                    else:
                        cclientid.send(
                            ":%s!%s@%s MODE %s +k %s\r\n" %
                            (_self.nickname, _self._username, _self._hostmask, chanid.channelname, sData))
            else:
                raw_messages.raw(self, "905", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(self, "482", _self.nickname, chanid.channelname)

    def _ownerkey(self, chanid, _self, sData):

        if _self.nickname.lower() in chanid._users:
            if _self.nickname.lower() in chanid._owner:
                if chanid._prop.validate(sData) == False:
                    raw_messages.raw(_self, "905", _self.nickname, chanid.channelname)
                else:
                    if sData == ":":
                        sData = ""
                    if sData != "" and sData[0] == ":":
                        sData = sData[1:]

                    chanid._prop.ownerkey = sData

                    time.sleep(0.2)

                    for each in chanid._users:
                        cid = server_context.nickname_to_client_mapping_entries[each]
                        if each.lower() in chanid._owner:
                            cid.send(":%s!%s@%s PROP %s OWNERKEY :%s\r\n" %
                                     (_self.nickname, _self._username, _self._hostmask, chanid.channelname, sData))

                    time.sleep(0.2)  # let people have fun!

            else:
                raw_messages.raw(_self, "485", _self.nickname, chanid.channelname)
        else:
            raw_messages.raw(_self, "442", _self.nickname, chanid.channelname)

    def _reset(self, chanid, _self, sData):

        if _self.nickname.lower() in server_context.operator_entries or _self.nickname.lower() in chanid._owner:
            b = True
            r = myint(sData)
            if r == 0 and sData == "0":
                chanid._prop.reset = 0
            elif r <= 120 and r > -1:
                chanid._prop.reset = r
            else:
                raw_messages.raw(_self, "906", _self.nickname, sData)
                b = False

            if b:
                for each in chanid._users:
                    cid = server_context.nickname_to_client_mapping_entries[each]
                    cid.send(":%s!%s@%s PROP %s RESET :%d\r\n" % (_self.nickname, _self._username,
                                                                  _self._hostmask, chanid.channelname,
                                                                  chanid._prop.reset))
        else:
            raw_messages.raw(_self, "485", _self.nickname, chanid.channelname)