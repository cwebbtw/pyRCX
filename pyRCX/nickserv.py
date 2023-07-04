class NickServEntry:
    """
    Represents an entry in the NickServ database
    """

    def __init__(self,
                 nickname: str,
                 password: str,
                 email: str,
                 registration_time: int,
                 ip: str,
                 virtual_host: str,
                 level: int,
                 show_email: str = False):
        self.grouped_nicknames = []
        self.registration_time = registration_time
        self.show_email = show_email
        self.virtual_host = virtual_host

        # TODO readable variables
        self._nickname = nickname
        self._password = password
        self._email = email
        self._details = ip
        self._level = int(level)
