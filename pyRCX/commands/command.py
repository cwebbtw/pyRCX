from abc import abstractmethod
from typing import List

from pyRCX.user import User


class Command:
    @abstractmethod
    def execute(self, user: User, parameters: List[str]):
        pass
