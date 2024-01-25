from abc import abstractmethod


class DialogView:
    @abstractmethod
    def setTextEditText(self, text: str):
        raise NotImplementedError

    @abstractmethod
    def setCancelButtonText(self, text: str):
        raise NotImplementedError

    @abstractmethod
    def setProgressBarValue(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def setOpenButtonEnabled(self):
        raise NotImplementedError

    @abstractmethod
    def closeDialog(self):
        raise NotImplementedError

    @abstractmethod
    def setDialogTitle(self, text: str):
        raise NotImplementedError

    @abstractmethod
    def showErrorMessage(self, text: str, informativeText: str):
        raise NotImplementedError
