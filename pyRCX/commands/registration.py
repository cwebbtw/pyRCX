from abc import ABC
from hashlib import sha256
from typing import List

from pyRCX.commands.command import Command
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class RegistrationCommand(ABC, Command):
    def __init__(self, server_context: ServerContext,
                 raw_messages: Raw):
        self._server_context = server_context
        self._raw_messages = raw_messages

    def has_registered(self, user: User):
        if user._username != "" and user.nickname != "":
            return self._server_context.configuration.server_password is not None and not user.presented_password

        return False


class UserCommand(RegistrationCommand):
    def __init__(self, server_context: ServerContext, raw_messages: Raw):
        RegistrationCommand.__init__(self, server_context, raw_messages)

    def execute(self, user: User, parameters: List[str]):

        if self._username != "":
            self._raw_messages.raw(user, "462", user.nickname)
        else:
            ustr = self._validate(parameters[1].replace(".", ""))
            if ustr == False:
                parameters[1] = user.nickname

            if self._validate(parameters[1].replace(".", "")) and parameters[4]:

                if len(strdata.split(":", 1)) == 2:
                    _fn = strdata.split(":", 1)[1][:256]
                else:
                    _fn = ""
                if self._validatefullname(_fn.replace(" ", "")) or _fn == "":
                    self._fullname = _fn
                    if self._server_context.configuration.user_host_masking_style != 5:

                        user._username = self._server_context.configuration.unregistered_user_identity_prefix + \
                                         parameters[1].replace(
                                             self._server_context.configuration.unregistered_user_identity_prefix, "")

                    elif self._server_context.configuration.user_host_masking_style == 5:
                        user._username = self._server_context.configuration.unregistered_user_identity_prefix + sha256(
                            (user.details[0] + self._server_context.configuration.user_host_masking_style_parameter).encode(
                                'utf-8')).hexdigest().upper()[:16]

                    if self.has_registered(user):
                        self._sendwelcome()
                else:
                    self._raw_messages.raw(user, "434", user.nickname, parameters[1].replace(':', ''))
            else:
                self._raw_messages.raw(user, "434", user.nickname, parameters[1].replace(':', ''))
