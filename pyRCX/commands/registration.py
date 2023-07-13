import re
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

    @staticmethod
    def _validate_full_name(text):
        check = re.compile("^[\x01-\xFF]{1,256}$")
        return check.match(text) is not None

    @staticmethod
    def _validate_user_name(text):
        check = re.compile("^[a-z0-9A-Z\_\-\^\|\`\'\[\]\\\~\{\}\x7F-\xFF]{1,32}$")
        return  check.match(text) is not None

    def execute(self, user: User, parameters: List[str]):
        if self._username != "":
            self._raw_messages.raw(user, "462", user.nickname)
        else:
            ustr = self._validate_user_name(parameters[1].replace(".", ""))
            if not ustr:
                parameters[1] = user.nickname

            if self._validate_user_name(parameters[1].replace(".", "")) and parameters[4]:
                full_name = " ".join(parameters[4:])
                full_name = full_name[1:] if full_name.startswith(":") else ""

                if self._validate_full_name(full_name.replace(" ", "")) or full_name == "":
                    self._fullname = full_name
                    if self._server_context.configuration.user_host_masking_style != 5:

                        user._username = self._server_context.configuration.unregistered_user_identity_prefix + \
                                         parameters[1].replace(
                                             self._server_context.configuration.unregistered_user_identity_prefix, "")

                    elif self._server_context.configuration.user_host_masking_style == 5:
                        user._username = self._server_context.configuration.unregistered_user_identity_prefix + sha256(
                            (user.details[
                                 0] + self._server_context.configuration.user_host_masking_style_parameter).encode(
                                'utf-8')).hexdigest().upper()[:16]

                    if self.has_registered(user):
                        user._sendwelcome()
                else:
                    self._raw_messages.raw(user, "434", user.nickname, parameters[1].replace(':', ''))
            else:
                self._raw_messages.raw(user, "434", user.nickname, parameters[1].replace(':', ''))
