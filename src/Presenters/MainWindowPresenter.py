from weakref import ref
from Views.MainWindowView import MainWindowView
from Helpers.SettingsManager import SettingsManager
from Models.UserOptions import UserOptions


class MainWindowPresenter:
    def __init__(self, view: MainWindowView):
        self.view = ref(view)
        settings = SettingsManager().load()
        self.userOptions = UserOptions(settings)

    def viewDidLoad(self):
        self.__setSettingsToView()

    def onLinkEdited(self, text: str):
        self.userOptions.setLink(text)

    def onDestinationChanged(self, text: str):
        settings = self.userOptions.settings()
        if text != settings.destination():
            settings.setDestination(text)
            SettingsManager().save(settings)
            self.userOptions.settings().setDestination(text)

    def __setSettingsToView(self):
        settings = self.userOptions.settings()
        self.view().setDestination(settings.destination())
        self.view().setOutputFormat(settings.outputFormat())

    def onTrimFromEdited(self, text: str):
        self.userOptions.setTrimFrom(f"{text}.00")

    def onTrimToEdited(self, text: str):
        self.userOptions.setTrimTo(f"{text}.00")

    def onFormatEdited(self, text: str):
        settings = self.userOptions.settings()
        if text != settings.outputFormat():
            settings.setOutputFormat(text)
            SettingsManager().save(settings)
            self.userOptions.settings().setOutputFormat(text)

    def onForceKeyframesStateChanged(self, state: int):
        forceKeyframes = False if state == 0 else True
        # forceKeyframes = state in [1, 2]
        self.userOptions.setForceKeyframes(forceKeyframes)

    def onDownloadPushButtonClicked(self):
        options = self.userOptions
        self.view().showDialog(options)
