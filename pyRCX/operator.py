class OperatorEntry:
    """
    Represents an operator entry parsed from configuration
    """

    operlevel: int = 0
    
    guide = False
    hidden = False
    watchserver = False
    watchbans = False
    watchnickserv = False
    usage = False

    def __init__(self, username, password, flags, filename):
        self.username = username
        self.password = password
        self.flags = flags
        self.filename = filename


class LinkOpers:
    """
    Represents an operator entry from another server

    Not used
    """

    operlevel = 0
    guide = False
    hidden = False
    watchserver = False
    watchbans = False
    watchnickserv = False
    usage = False

    def __init__(self, username, password, flags, filename):
        self.username = username
        self.password = password
        self.flags = flags
        self.filename = filename
