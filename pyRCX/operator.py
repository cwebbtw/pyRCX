class OperatorEntry:
    """
    Represents an operator entry parsed from configuration
    """
    
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

        self.operator_level: int = 0
