import re
import time

from pyRCX.server_context import ServerContext

__server_context: ServerContext | None = None
__raw_messages: ServerContext | None = None


class AccessInformation:
    """
    Represents access information but poorly named and needs refactoring
    """

    def __init__(self, object, level, mask, setby, expires, reason, oplevel):
        self._object = object  # objects: *, #, $
        self._level = level.upper()
        self._reason = reason
        self._mask = mask
        self._setby = setby
        self._setat = int(time.time())
        if expires == 0:
            self._expires = 0
            self._deleteafterexpire = False
        else:
            self._expires = int(time.time()) + (expires * 60)
            self._deleteafterexpire = True

        self._oplevel = oplevel


# channels only - this only needs to be done on events where access may apply, commands are JOIN and ACCESS
def CheckChannelExpiry(chanid):
    for each in list(chanid.ChannelAccess):
        if int(time.time()) >= each._expires:
            if each._deleteafterexpire:
                chanid.ChannelAccess.remove(each)
                # _Access.records.remove(each)


# channels only - this only needs to be done on events where access may apply, commands are JOIN and ACCESS
def CheckSelfExpiry(nickid):
    for each in list(nickid._access):
        if int(time.time()) >= each._expires:
            if each._deleteafterexpire:
                nickid._access.remove(each)
                # _Access.records.remove(each)


def CFS(_mask):
    "Create format string"
    _mask = _mask.replace("\\", "\\\\").replace("[", "\[").replace("]", "\]").replace("{", "\{")
    _mask = _mask.replace(
        "}", "\}").replace(
        ".", "\.").replace(
        "+", "\+").replace(
        "^", "\^").replace(
        "$", "\$").replace(
        "?", ".").replace(
        "*", ".*")

    return _mask


def MatchAccess(_mask, cid, NoMatchIP=False):
    if _mask[0] == "&":
        if "&" == _mask[0]:
            if cid._MODE_register:
                for groupnicks in list(__server_context.nickserv_entries.values()):
                    if _mask[1:].lower() in groupnicks.grouped_nicknames or _mask[
                                                                            1:].lower() == groupnicks.nickname.lower():
                        if cid.nickname.lower() in groupnicks.grouped_nicknames or cid.nickname.lower() == groupnicks.nickname.lower():
                            return 1

    p = re.compile("^(.+)\!(.+)\@(.+)\$(.+)$")
    g = p.match(_mask)
    if g == None:
        return -1
    else:
        _nick = g.group(1)
        _nick_re = "^" + CFS(_nick.lower()) + "\!"

        _user = g.group(2)
        _user_re = CFS(_user.lower()) + "\@"

        _host = g.group(3)
        _host_re = CFS(_host.lower())

        _server = g.group(4)
        _server_re = "^" + CFS(_server.lower()) + "$"

        x = re.compile(_nick_re + _user_re + _host_re + "$")

        s = re.compile(_server_re)

        if s.match(cid._server):
            if x.match(cid.nickname.lower() + "!" + cid._username.lower() + "@" + cid._hostmask.lower()) != None:
                return 1
            if x.match(
                    cid.nickname.lower() + "!" + cid._username.lower() + "@" + cid._hostname.lower()) != None and NoMatchIP == False:
                return 1
            if x.match(cid.nickname.lower() + "!" + cid._username.lower() + "@" + cid.details[
                0]) != None and NoMatchIP == False:
                return 1
        else:
            return -1


def getgroup(d, id):
    try:
        if d.group(id) == "":
            return "*"
        else:
            return d.group(id)
    except:
        return "*"


def CreateMaskString(strin, server=False):
    if strin[0] == "&":
        if "!" in strin or "@" in strin:
            return -1
        else:
            if strin.lower()[1:] in __server_context.nickserv_entries or server == True:
                return strin
            else:
                for groupnicks in list(__server_context.nickserv_entries.values()):
                    if strin.lower()[1:] in groupnicks.grouped_nicknames:
                        return strin

                return -2

    if strin.count("!") > 1 or strin.count("$") > 1 or strin.count("@") > 1:
        return -1
    prefix, suffix, term, chars = "", "", 0, "[a-z0-9A-Z\_\@\$\!-\^\|\`\'\[\]\>\~\{\}\x7F-\xFF]{0,32}"

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

        svr = re.compile("(" + chars + "|)\$(" + chars + "|)")  # lol$lol
        m = svr.match(strin)
        if m == None:
            return -1
        if len(m.groups()) == 2:
            return "*!*@" + getgroup(m, 1) + "$" + getgroup(m, 2)
    else:
        term = 4
        smatch = "^(" + chars + ")$"
        suffix = "!*@*$*"

    p = re.compile(smatch)
    if p == None:
        return -1
    else:
        g = p.match(strin)
        if g == None:
            return -1
        try:
            if term == 0:
                return -1
            if term == 1:
                return (getgroup(g, 1) + "!" + getgroup(g, 2) + "@" + getgroup(g,
                                                                               3) + suffix).replace(
                    ":", "")
            if term == 2:
                return (getgroup(g, 1) + "!" + getgroup(g, 2) + suffix).replace(":", "")
            if term == 3:
                return (prefix + getgroup(g, 1) + "@" + getgroup(g, 2) + suffix).replace(":", "")
            if term == 4:
                return (getgroup(g, 1) + suffix).replace(":", "")
            if term == 5:
                return (getgroup(g, 1) + "!" + getgroup(g, 2) + "@" + getgroup(g,
                                                                               3) + "$" + getgroup(
                    g, 4)).replace(":", "")
            if term == 6:
                return (getgroup(g, 1) + "!" + getgroup(g, 2) + suffix + getgroup(g, 3)).replace(":",
                                                                                                 "")
            if term == 7:
                return (prefix + getgroup(g, 1) + "@" + getgroup(g, 2) + "$" + getgroup(g,
                                                                                        3)).replace(
                    ":", "")
            if term == 8:
                return (prefix + getgroup(g, 1)).replace(":", "")
        except:
            return "*!*@*$*"


def ClearRecords(object, cid, level=""):
    _securitymsg = False
    if object == "*":
        opid = __server_context.operator_entries[cid.nickname.lower()]
        for each in list(__server_context.server_access_entries):

            if level == "" or level.upper() == each._level.upper():
                if (opid.operator_level + 2) < each._oplevel:
                    _securitymsg = True
                else:
                    __server_context.server_access_entries.remove(each)

        if _securitymsg:
            __raw_messages.raw(cid, "922", cid.nickname, "*")
        else:
            if level == "":
                level = "*"
            __raw_messages.raw(cid, "820", cid.nickname, "*", level)

    elif object[0] == "#" or object[0] == "%" or object[0] == "&":
        chanid = __server_context.channel_entries[object.lower()]
        _operlevel = 0
        if cid.nickname.lower() in chanid._op:
            _operlevel = 1
        if cid.nickname.lower() in chanid._owner:
            _operlevel = 2
        if cid.nickname.lower() in __server_context.operator_entries:
            opid = __server_context.operator_entries[cid.nickname.lower()]
            _operlevel = opid.operator_level + 2

        if _operlevel < 1:
            __raw_messages.raw(cid, "913", cid.nickname, chanid.channelname)
            return -1

        for each in list(chanid.ChannelAccess):
            if level == "" or level.upper() == each._level.upper():
                if _operlevel < each._oplevel:
                    _securitymsg = True
                else:
                    chanid.ChannelAccess.remove(each)

        if _securitymsg:
            __raw_messages.raw(cid, "922", cid.nickname, chanid.channelname)
        else:
            if level == "":
                level = "*"
            __raw_messages.raw(cid, "820", cid.nickname, chanid.channelname, level)

    else:
        for each in list(cid._access):
            if level == "" or level.upper() == each._level.upper():
                cid._access.remove(each)

        if level == "":
            level = "*"
        __raw_messages.raw(cid, "820", cid.nickname, cid.nickname, level)


def DelRecord(cid, object, level, mask):
    if object[0] == "*":
        opid = __server_context.operator_entries[cid.nickname.lower()]
        for each in list(__server_context.server_access_entries):
            if each._mask.lower() == mask.lower() and each._level.lower() == level.lower():
                if (opid.operator_level + 2) < each._oplevel:
                    return -2
                __server_context.server_access_entries.remove(each)

                return 1

    elif object[0] == "#" or object[0] == "%" or object[0] == "&":
        chanid = __server_context.channel_entries[object.lower()]
        _operlevel = 0
        if cid.nickname.lower() in chanid._op:
            _operlevel = 1
        if cid.nickname.lower() in chanid._owner:
            _operlevel = 2
        if cid.nickname.lower() in __server_context.operator_entries:
            opid = __server_context.operator_entries[cid.nickname.lower()]
            _operlevel = opid.operator_level + 2

        if cid.nickname.lower() not in chanid._op and cid.nickname.lower() not in chanid._owner and cid.nickname.lower() not in __server_context.operator_entries:
            return -2  # not op - return no access
        if level.upper() == "OWNER" and cid.nickname.lower() not in chanid._owner and cid.nickname.lower() not in __server_context.operator_entries:
            return -2  # not owner - return no access

        CopyChannelAccess = list(chanid.ChannelAccess)
        for each in CopyChannelAccess:
            if each._mask.lower() == mask.lower() and each._level.lower() == level.lower():
                if _operlevel < each._oplevel:
                    return -2
                chanid.ChannelAccess.remove(each)

                return 1

    else:
        CopyAccess = list(cid._access)
        for each in CopyAccess:
            if each._mask.lower() == mask.lower() and each._level.lower() == level.lower():
                cid._access.remove(each)

                return 1

    return -1


def AddRecord(cid, object, level, mask, expires, tag):
    _list = None
    objid = None
    if object == "*":
        if cid == "":
            _operlevel = 6
        else:
            opid = __server_context.operator_entries[cid.nickname.lower()]
            _operlevel = opid.operator_level + 2

        _list = __server_context.server_access_entries

    elif object[0] == "#" or object[0] == "%" or object[0] == "&":
        objid = __server_context.channel_entries[object.lower()]
        _operlevel = 0
        if cid == "":
            _operlevel = 5
        else:
            if cid.nickname.lower() in objid._op:
                _operlevel = 1
            if cid.nickname.lower() in objid._owner:
                _operlevel = 2
            if cid.nickname.lower() in __server_context.operator_entries:
                opid = __server_context.operator_entries[cid.nickname.lower()]
                _operlevel = opid.operator_level + 2

            if cid.nickname.lower() not in objid._op and cid.nickname.lower() not in objid._owner and cid.nickname.lower() not in __server_context.operator_entries:
                return -2  # not op - return no access
            if level.upper() == "OWNER" and cid.nickname.lower() not in objid._owner and cid.nickname.lower() not in __server_context.operator_entries:
                return -2  # not owner - return no access

        _list = objid.ChannelAccess

    else:
        objid = __server_context.nickname_to_client_mapping_entries[object.lower()]
        _list = objid._access
        _operlevel = 0

    for each in _list:
        if each._mask.lower() == mask.lower():
            return -1  # Duplicate access entry

    entry = None
    if cid == "":
        setby = __server_context.configuration.server_name
    else:
        setby = cid._username + "@" + cid._hostmask

    if object == "*":
        entry = AccessInformation("*", level, mask, setby, expires, tag, _operlevel)
        __server_context.server_access_entries.append(entry)

    # TODO this should support prefixchar rather than hard coded values
    elif object[0] == "#" or object[0] == "%" or object[0] == "&":
        entry = AccessInformation(objid.channelname, level, mask, setby, expires, tag, _operlevel)
        objid.ChannelAccess.append(entry)
    else:
        entry = AccessInformation(objid._nickname, level, mask, setby, expires, tag, _operlevel)
        objid._access.append(entry)

    return 1


def initialise(server_context, raw_messages):
    global __server_context, __raw_messages
    __server_context = server_context
    __raw_messages = raw_messages
