from abc import abstractmethod
from Models.UserOptions import UserOptions


class MainWindowView:
    @abstractmethod
    def setDestination(self, destination: str):
        raise NotImplementedError

    @abstractmethod
    def setOutputFormat(self, outputFormat: str):
        raise NotImplementedError

    @abstractmethod
    def showDialog(self, userOptions: UserOptions):
        raise NotImplementedError
