import logging
import time
from typing import Dict

from pyRCX.configuration import Configuration
from pyRCX.user import User
from pyRCX.statistics import Statistics

class Raw:

    def __init__(self, configuration: Configuration, statistics: Statistics,
                 disabled_functionality: Dict[str, int]):
        self.logger = logging.getLogger('RAW')

        self.configuration: Configuration = configuration
        self.statistics: Statistics = statistics
        self.disabled_functionality: Dict[str, int] = disabled_functionality

    def raw(self, param1: User, param2="", param3="", param4="", param5="", param6="", param7=""):
        if param3 == "":
            param3 = "*"

        if param2 == "001":
            param1.send(
                ":" + self.configuration.server_name + " 001 " + param3 + " :Welcome to the " + self.configuration.network_name + " chat service " + param3 + "\r\n")

        if param2 == "002":
            param1.send(
                ":" + self.configuration.server_name + " 002 " + param3 + " :Your host is " + self.configuration.server_name + ", running version " + self.configuration.VERSION + "\r\n")

        if param2 == "003":
            param1.send(":" + self.configuration.server_name + " 003 " + param3 + " :This server was created on %s\r\n" %
                        (time.strftime("%A %B %d %H:%M:%S %Y GMT", time.localtime())))

        if param2 == "004":
            param1.send(":" + self.configuration.server_name + " 004 " + param3 + " " + self.configuration.network_name +
                        " pyRCX " + self.configuration.VERSION + " abAfghiInoOpPrwzX aAbcCdefGhikKlmMnNopPqQrRsStTuvwxXZ\r\n")

        if param2 == "005":
            if "IRCX" in self.disabled_functionality:
                param1.send(
                    ":" + self.configuration.server_name + " 005 " + param3 + " IRC PREFIX=(ov)@+ NETWORK=" + self.configuration.network_name +
                    " are supported by this server\r\n")
            else:
                param1.send(
                    ":" + self.configuration.server_name + " 005 " + param3 + " IRCX PREFIX=(qov).@+ NETWORK=" + self.configuration.network_name +
                    " are supported by this server\r\n")

        if param2 == "221":
            param1.send(":" + self.configuration.server_name + " 221 " + param3 + " " + param4 + "\r\n")

        if param2 == "251":
            param1.send(
                ":" + self.configuration.server_name + " 251 " + param3 + " :There are " + str(
                    self.statistics.current_online_users()) +
                " users and " + str(self.statistics.current_invisible_users()) + " invisible on 1 server\r\n")

        if param2 == "252":
            total_operators_online = self.statistics.current_online_operators()

            if total_operators_online > 0:
                param1.send(
                    ":" + self.configuration.server_name + " 252 " + param3 + " " + str(
                        total_operators_online) + " :operator(s) online\r\n")

        if param2 == "253":
            if self.statistics.current_unknown_connections() > 0:
                param1.send(":" + self.configuration.server_name + " 253 " + param3 + " " + str(
                    self.statistics.current_unknown_connections()) +
                            " :unknown connection(s)\r\n")

        if param2 == "254":
            total_channels = self.statistics.current_channels()
            if total_channels > 0:
                param1.send(
                    ":" + self.configuration.server_name + " 254 " + param3 + " " + str(total_channels) + " :channels formed\r\n")

        if param2 == "255":
            param1.send(":" + self.configuration.server_name + " 255 " + param3 + " :I have " + str(
                self.statistics.current_local_users()) + " client(s) and 1 server\r\n")

        if param2 == "256":
            # display if operators available
            param1.send(
                ":" + self.configuration.server_name + " 256 " + param3 + " :" + self.configuration.network_name + " communications service\r\n")

        if param2 == "257":
            # display if operators available
            param1.send(":" + self.configuration.server_name + " 257 " + param3 + " :pyRCX version " + self.configuration.VERSION + ", see /CREDITS\r\n")

        if param2 == "258":
            param1.send(":" + self.configuration.server_name + " 258 " + param3 + " :" + self.configuration.server_admin_name + "\r\n")

        if param2 == "259":
            param1.send(":" + self.configuration.server_name + " 259 " + param3 + " :" + self.configuration.server_admin_organisation + "\r\n")

        if param2 == "263":
            param1.send(":" + self.configuration.server_name + " 263 " + param3 + " :Message too long, restrict your output\r\n")

        if param2 == "265":
            param1.send(":" + self.configuration.server_name + " 265 " + param3 + " :Current Local Users: " + str(
                self.statistics.current_local_users()) + "  Max: " + str(self.statistics.max_local_users()) + "\r\n")

        if param2 == "266":
            param1.send(
                ":" + self.configuration.server_name + " 266 " + param3 + " :Current Global Users: " + str(
                    self.statistics.current_global_users()) + "  Max: " + str(
                    self.statistics.max_local_users()) + "\r\n")

        if param2 == "301":
            param1.send(
                ":" + self.configuration.server_name + " 301 " + param3 + " " + param4._nickname + " " + param4._away + "\r\n")

        if param2 == "302":
            param1.send(
                ":" + self.configuration.server_name + " 302 " + param3 + " :" + param4._nickname + "=+" + param4._username + "@" +
                (param4.details[0] if param5 else param4._hostmask) + "\r\n")

        if param2 == "303":
            param1.send(":" + self.configuration.server_name + " 303 " + param3 + " :" + param4 + "\r\n")

        if param2 == "305":
            param1.send(":" + self.configuration.server_name + " 305 " + param3 + " :You are no longer marked as being away\r\n")

        if param2 == "306":
            param1.send(":" + self.configuration.server_name + " 306 " + param3 + " :You have been marked as being away\r\n")

        if param2 == "307":
            param1.send(
                ":" + self.configuration.server_name + " 307 " + param3 + " " + param4._nickname + " :is registered to services\r\n")

        if param2 == "311":
            param1.send(
                ":" + self.configuration.server_name + " 311 " + param3 + " " + param4._nickname + " " + param4._username + " " + param4._hostmask +
                " * :" + param4._fullname + "\r\n")

        if param2 == "312":
            param1.send(
                ":" + self.configuration.server_name + " 312 " + param3 + " " + param4._nickname + " " + param4._server + " :" + self.configuration.network_name + "\r\n")

        if param2 == "313":
            if "A" in param5:
                param1.send(":" + self.configuration.server_name + " 313 " + param3 + " " + param4._nickname +
                            " :is the Network Administrator\r\n")

            elif "O" in param5:
                param1.send(":" + self.configuration.server_name + " 313 " + param3 + " " + param4._nickname +
                            " :is a Server Administrator\r\n")

            elif "a" in param5:
                param1.send(":" + self.configuration.server_name + " 313 " + param3 + " " + param4._nickname +
                            " :is a System Chat Manager\r\n")

            elif "o" in param5:
                param1.send(":" + self.configuration.server_name + " 313 " + param3 + " " + param4._nickname +
                            " :is a System Operator\r\n")

            if "g" in param5:
                param1.send(
                    ":" + self.configuration.server_name + " 313 " + param3 + " " + param4._nickname + " :is a Guide\r\n")

        if param2 == "315":
            param1.send(":" + self.configuration.server_name + " 315 " + param3 + " " + param4 + " :End of /WHO list.\r\n")

        if param2 == "316":
            param1.send(":" + self.configuration.server_name + " 316 " + param3 + " " + param4 +
                        " :is unable to participate because they are on the gag list\r\n")

        if param2 == "317":
            param1.send(
                ":" + self.configuration.server_name + " 317 " + param3 + " " + param4._nickname + " " +
                str(max(int(time.time()) - param4._idletime, 0)) + " " + str(param4._signontime) +
                " :seconds idle, signon time\r\n")

        if param2 == "318":
            param1.send(":" + self.configuration.server_name + " 318 " + param3 + " " + param4 + " :End of /WHOIS list\r\n")

        if param2 == "319":
            param1.send(
                ":" + self.configuration.server_name + " 319 " + param3 + " " + param4._nickname + " :" + param5 + "\r\n")

        if param2 == "320":
            if param4._friendlyname:
                param1.send(
                    ":" + self.configuration.server_name + " 320 " + param3 + " " + param4._nickname + " :" + param4._friendlyname + "\r\n")

        if param2 == "321":
            param1.send(":" + self.configuration.server_name + " 321 " + param3 + " Channel :Users  Name\r\n")

        if param2 == "322":
            param1.send(
                ":" + self.configuration.server_name + " 322 " + param3 + " " + param4 + " " + param5 + " :" + param6 + "\r\n")

        if param2 == "323":
            param1.send(":" + self.configuration.server_name + " 323 " + param3 + " :End of /LIST\r\n")

        if param2 == "324":
            param1.send(":" + self.configuration.server_name + " 324 " + param3 + " " + param4 + " +" + param5 + "\r\n")

        if param2 == "331":
            param1.send(":" + self.configuration.server_name + " 331 " + param3 + " " + param4 + " :No topic is set\r\n")

        if param2 == "332":
            param1.send(":" + self.configuration.server_name + " 332 " + param3 + " " + param4 + " :" + param5 + "\r\n")

        if param2 == "333":
            if param5 == "":
                param5 = self.configuration.server_name
            param1.send(
                ":" + self.configuration.server_name + " 333 " + param3 + " " + param4 + " " + param5 + " " + str(param6) + "\r\n")

        if param2 == "341":
            param1.send(":" + self.configuration.server_name + " 341 " + param3 + " " + param4 + " " + param5 + "\r\n")

        if param2 == "352":
            param1.send(":" + self.configuration.server_name + " 352 " + param3 + " " + param4 + "\r\n")

        if param2 == "353":
            param1.send(":" + self.configuration.server_name + " 353 " + param3 + " = " + param4 + " :" + param5 + "\r\n")

        if param2 == "364":
            param1.send(
                ":" + self.configuration.server_name + " 364 " + param3 + " " + param4 + " " + self.configuration.network_name + " :0 " + param5 + "\r\n")

        if param2 == "365":
            param1.send(":" + self.configuration.server_name + " 365 " + param3 + " * :End of /LINKS list.\r\n")

        if param2 == "366":
            param1.send(":" + self.configuration.server_name + " 366 " + param3 + " " + param4 + " :End of /NAMES list.\r\n")

        if param2 == "367":
            param1.send(
                ":" + self.configuration.server_name + " 367 " + param3 + " " + param4 + " " + param5 + " " + param6 + " " + param7 + "\r\n")

        if param2 == "368":
            param1.send(":" + self.configuration.server_name + " 368 " + param3 + " " + param4 + " :End of Channel Ban List\r\n")

        if param2 == "371":
            param1.send(
                ":" + self.configuration.server_name + " 371 " + param3 + " :" + self.configuration.network_name + "communication service "
                                                                            + self.configuration.VERSION + "\r\n:" +
                self.configuration.server_name + " 371 " + param3 + self.statistics.server_launch + "\r\n")

        if param2 == "372":
            param1.send(":" + self.configuration.server_name + " 372 " + param3 + " :- " + param4.replace("\r", "").replace("\n",
                                                                                                              "") + "\r\n")

        if param2 == "374":
            param1.send(":" + self.configuration.server_name + " 374 " + param3 + " :End of /INFO list.\r\n")

        if param2 == "375":
            param1.send(
                ":" + self.configuration.server_name + " 375 " + param3 + " :- " + self.configuration.server_name + " Message of the Day\r\n")

        if param2 == "376":
            param1.send(":" + self.configuration.server_name + " 376 " + param3 + " :End of /MOTD command.\r\n")

        if param2 == "378":
            if param5:
                param1.send(
                    ":" + self.configuration.server_name + " 378 " + param3 + " " + param4._nickname + " :is connecting from " +
                    param4.details
                    [0] + "\r\n")

        if param2 == "381":
            param1.send(":" + self.configuration.server_name + " 381 " + param3 + " :" + param4 + "\r\n")

        if param2 == "391":
            param1.send(":" + self.configuration.server_name + " 381 " + param3 + " :%s\r\n" %
                        (time.strftime("%A %B %d %H:%M:%S %Y GMT", time.localtime())))

        if param2 == "401":
            param1.send(":" + self.configuration.server_name + " 401 " + param3 + " " + param4 + " :No such nick/channel\r\n")

        if param2 == "403":
            param1.send(":" + self.configuration.server_name + " 403 " + param3 + " " + param4 + " :No such channel\r\n")

        if param2 == "404":
            param1.send(":" + self.configuration.server_name + " 404 " + param3 + " " + param4 + " :" + param5 + "\r\n")

        if param2 == "405":
            param1.send(
                ":" + self.configuration.server_name + " 405 " + param3 + " " + param4 + " :You have joined too many channels\r\n")

        if param2 == "409":
            param1.send(":" + self.configuration.server_name + " 409 " + param3 + " :No origin specified\r\n")

        if param2 == "411":
            param1.send(":" + self.configuration.server_name + " 411 " + param3 + " :No recipient given (" + param4 + ")\r\n")

        if param2 == "412":
            param1.send(":" + self.configuration.server_name + " 412 " + param3 + " :No text to send (" + param4 + ")\r\n")

        if param2 == "416":
            param1.send(":" + self.configuration.server_name + " 416 " + param3 + " " + param4 +
                        " :Too many lines in the output, restrict your request\r\n")

        if param2 == "421":
            param1.send(":" + self.configuration.server_name + " 421 " + param3 + " " + param4 + " :Unknown Command\r\n")

        if param2 == "422":
            param1.send(":" + self.configuration.server_name + " 422 " + param3 + " :MOTD File is missing\r\n")

        if param2 == "432":
            if param3 == "" or param3 == "*":
                param3 = "*"
                param1._nosendnickserv = True

            param1.send(":" + self.configuration.server_name + " 432 " + param3 + " " + param4 + " :Erroneous Nickname\r\n")

        if param2 == "433":
            if param3 == "" or param3 == "*":
                param3 = "*"
                param1._nosendnickserv = True

            param1.send(":" + self.configuration.server_name + " 433 " + param3 + " " + param4 + " :Nickname is already in use\r\n")

        if param2 == "434":
            if param3 == "":
                param3 = "*"

            param1.send(":" + self.configuration.server_name + " 434 " + param3 + " " + param4 + " :Erroneous Username\r\n")

        if param2 == "437":
            param1.send(":" + self.configuration.server_name + " 437 " + param3 + " " + param4 +
                        " :Cannot change nickname while banned on channel\r\n")

        if param2 == "438":
            param1.send(
                ":" + self.configuration.server_name + " 438 " + param3 + " :Nick change too fast. Please try again in a few minutes.\r\n")

        if param2 == "441":
            param1.send(":" + self.configuration.server_name + " 441 " + param3 + " " + param4 + " :They aren't on that channel\r\n")

        if param2 == "442":
            param1.send(":" + self.configuration.server_name + " 442 " + param3 + " " + param4 + " :You're not in that channel\r\n")

        if param2 == "443":
            param1.send(
                ":" + self.configuration.server_name + " 443 " + param3 + " " + param4 + " " + param5 + " :is already on channel\r\n")

        if param2 == "446":
            param1.send(":" + self.configuration.server_name + " 446 " + param3 + " :" + param4 + " has been disabled\r\n")

        if param2 == "451":
            param1.send(":" + self.configuration.server_name + " 451 " + param3 + " :You have not registered\r\n")

        if param2 == "461":
            if param3 == "":
                param3 = "*"
            param1.send(":" + self.configuration.server_name + " 461 " + param3 + " " + param4 + " :Not enough parameters\r\n")

        if param2 == "462":
            if param3 == "":
                param3 = "*"
            param1.send(":" + self.configuration.server_name + " 462 " + param3 + " " + ":You may not reregister\r\n")

        if param2 == "465":
            param1.send(":" + self.configuration.server_name + " 465 " + param3 + " " + ":You are banned from this server\r\n")
            if param4 != "":
                param1.send("ERROR :Closing Link: " + param1.details[0] + " (" + param4.strip() + ")\r\n")

        if param2 == "468":
            param1.send(
                ":" + self.configuration.server_name + " 468 " + param3 + " " + param4 + " :Only servers can change that mode\r\n")

        if param2 == "471":
            param1.send(":" + self.configuration.server_name + " 471 " + param3 + " " + param4 + " :Cannot join channel (+l)\r\n")

        if param2 == "472":
            param1.send(":" + self.configuration.server_name + " 472 " + param3 + " " + param4 + " :is unknown mode char to me\r\n")

        if param2 == "473":
            param1.send(":" + self.configuration.server_name + " 473 " + param3 + " " + param4 + " :Cannot join channel (+i)\r\n")

        if param2 == "475":
            param1.send(":" + self.configuration.server_name + " 475 " + param3 + " " + param4 + " :Cannot join channel (+k)\r\n")

        if param2 == "477":
            param1.send(":" + self.configuration.server_name + " 477 " + param3 + " " + param4 +
                        " :You need a registered nickname to join that channel\r\n")

        if param2 == "481":
            param1.send(":" + self.configuration.server_name + " 481 " + param3 + " :" + param4 + "\r\n")

        if param2 == "482":
            param1.send(":" + self.configuration.server_name + " 482 " + param3 + " " + param4 + " :You're not channel operator\r\n")

        if param2 == "483":
            param1.send(
                ":" + self.configuration.server_name + " 483 " + param3 + " " + param4 + " :Cannot join channel (" + param5 + ")\r\n")

        if param2 == "485":
            param1.send(":" + self.configuration.server_name + " 485 " + param3 + " " + param4 + " :You're not channel owner\r\n")

        if param2 == "491":
            param1.send(":" + self.configuration.server_name + " 491 " + param3 + " :" + param4 + "\r\n")

        if param2 == "501":
            param1.send(":" + self.configuration.server_name + " 501 " + param3 + " :Unknown MODE flag\r\n")

        if param2 == "502":
            param1.send(":" + self.configuration.server_name + " 502 " + param3 + " :Can't change mode for other users\r\n")

        if param2 == "520":
            param1.send(":" + self.configuration.server_name + " 520 " + param3 + " " + param4 + " :Authenticated clients only\r\n")

        if param2 == "613":  # :TK2CHATWBC05 613 null :207.68.167.157 6667
            param1.send(":" + self.configuration.server_name + " 613 " + param3 + " :" + param4 + " +" + param5 + "\r\n")

        if param2 == "702":
            param1.send(":" + self.configuration.server_name + " 702 " + param3 + " " + param4 + " :Channel not found\r\n")

        if param2 == "705":
            param1.send(
                ":" + self.configuration.server_name + " 705 " + param3 + " " + param4 + " :Channel with same name exists\r\n")

        if param2 == "710":
            param1.send(
                ":" + self.configuration.server_name + " 710 " + param3 + " :The server Administrator has limited this server to " + param4 +
                " channels\r\n")

        if param2 == "800":
            param1.send(":" + self.configuration.server_name + " 800 " + param3 + " " + param4 + " 0 ANON 512 *\r\n")

        if param2 == "801":
            param1.send(":%s 801 %s %s\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "802":
            param1.send(":%s 802 %s %s\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "803":
            param1.send(":%s 803 %s %s :Start of access entries\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "804":
            param1.send(":%s 804 %s %s\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "805":
            param1.send(":%s 805 %s %s :End of access entries\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "818":
            param1.send(":" + self.configuration.server_name + " 818 " + param3 + " " + param4 + "\r\n")

        if param2 == "819":
            param1.send(":" + self.configuration.server_name + " 819 " + param3 + " " + param4 + " :End of properties\r\n")

        if param2 == "820":
            param1.send(":%s 820 %s %s %s :Clear\r\n" % (self.configuration.server_name, param3, param4, param5))

        # if param2 == "821":
        # param1.send(":%s 821 :User unaway\r\n" % (param3._nickname))

        # if param2 == "822":
        # param1.send(":%s 822 :%s\r\n" % (param3._nickname,param3._away))

        if param2 == "900":
            param1.send(":%s 900 %s %s :Bad command\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "903":
            param1.send(":%s 903 %s %s :Bad level\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "905":
            param1.send(":%s 905 %s %s :Bad property specified\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "906":
            param1.send(":%s 906 %s %s :Bad value specified\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "908":
            param1.send(":%s 908 %s :No permissions to perform command\r\n" % (self.configuration.server_name, param3))

        if param2 == "909":
            param1.send(":%s 909 %s :No such nickname registered to services\r\n" % (self.configuration.server_name, param3))

        if param2 == "912":
            param1.send(":%s 912 %s %s :Unsupported authentication package\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "913":
            param1.send(":%s 913 %s %s :No access\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "914":
            param1.send(":%s 914 %s %s :Duplicate access entry\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "915":
            param1.send(":%s 915 %s %s :Unknown access entry\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "916":
            param1.send(":%s 916 %s %s :Too many access entries\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "922":
            param1.send(
                ":%s 922 %s %s :Some entries not cleared due to security\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "923":
            param1.send(":%s 923 %s %s :Does not permit whispers\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "924":
            param1.send(":%s 924 %s %s :No such object found\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "925":
            param1.send(":%s 925 %s %s :Command not supported.\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "927":
            param1.send(":%s 927 %s %s :Already in the channel.\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "934":
            param1.send(
                ":%s 934 %s %s :The channel you were on has been closed\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "935":
            param1.send(":%s 935 %s %s :Too many wildcards\r\n" % (self.configuration.server_name, param3, param4))

        if param2 == "997":
            param1.send(":%s 997 %s %s %s :Not supported by object\r\n" % (self.configuration.server_name, param3, param4, param5))

        if param2 == "998":
            param1.send(":%s 998 %s %s %s :Cannot invite to channel\r\n" % (self.configuration.server_name, param3, param4, param5))

        if param2 == "955":
            param1.send(
                ":%s 955 %s :\x02Credits - pyRCX networking chat service %s\x02\r\n:%s 955 %s :Christopher Webb\r\n" %
                (self.configuration.server_name, param3, self.configuration.VERSION, self.configuration.server_name, param3))
            param1.send(":%s 955 %s :-\r\n" % (self.configuration.server_name, param3))
            param1.send(
                ":%s 955 %s :\x02With thanks to:\x02\r\n:%s 955 %s :Darren Davies, Rob Lancaster, Kevin Deveau, "
                "Aaron Caffrey, Shane Britt\r\n" % (
                    self.configuration.server_name, param3, self.configuration.server_name, param3))
            param1.send(":%s 955 %s :-\r\n" % (self.configuration.server_name, param3))
            param1.send(
                ":%s 955 %s :\x02In loving memory of:\x02\r\n:%s 955 %s :Danny Moon, Ricky Laurn\r\n" %
                (self.configuration.server_name, param3, self.configuration.server_name, param3))
            param1.send(":%s 955 %s :-\r\n" % (self.configuration.server_name, param3))
            param1.send(
                ":%s 955 %s :\x02Be kind to one another, love like it's your last day on this amazing planet.\r\n" %
                (self.configuration.server_name, param3))
