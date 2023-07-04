import time


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
