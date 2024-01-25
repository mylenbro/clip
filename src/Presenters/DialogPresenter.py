from weakref import ref
from Views.DialogView import DialogView
from Process.YtdlpProcess import YtdlpProcess
from Helpers.Dependency import DependencyHelper
from Helpers.File import File
from Models.UserOptions import UserOptions


class DialogPresenter:
    def __init__(self, view: DialogView, options: UserOptions):
        self.view = ref(view)
        self.ytdlp = None
        self.filename = None
        self.userOptions = options
        self.dialogFinished = False

    # region Public

    def viewDidLoad(self):
        self.__checkDependencies()

    # endregion

    # region View's events

    def onOpenButtonClicked(self):
        destination = self.userOptions.settings().destination()
        filename = self.filename
        path = File.getPath(destination, filename)
        try:
            File.open(path)
        except Exception as e:
            self.__showErrorMessage(e.strerror, f"{e.filename}\nCode: {e.errno}")

    def onCancelButtonClicked(self):
        if self.ytdlp:
            self.ytdlp.stop()
        if self.dialogFinished:
            self.view().closeDialog()

    def onDialogClose(self):
        if self.ytdlp:
            self.ytdlp.stop()
        self.view().closeDialog()

    # endregion

    # region Private

    def __checkDependencies(self):
        status = DependencyHelper.getStatus()
        if status.hasDependencies:
            self.__startYtdlp(self.userOptions)
        else:
            self.view().setTextEditText(status.text)
            self.__dialogCanBeClosed()

    def __getFixedFilename(self, filename: str):
        destination = self.userOptions.settings().destination()
        newFilename = File.attemptToGetFile(destination, filename)
        return newFilename

    def __showErrorMessage(self, text: str, informativeText: str):
        self.view().showErrorMessage(text, informativeText)

    def __dialogCanBeClosed(self):
        self.view().setCancelButtonText("Close")
        self.dialogFinished = True

    # endregion

    # region yt-dlp related

    def __startYtdlp(self, options: UserOptions):
        self.ytdlp = YtdlpProcess(options)
        self.ytdlp.onProgressUpdate.connect(self.__onProgressUpdate)
        self.ytdlp.onFilenameUpdate.connect(self.__onFilenameUpdate)
        self.ytdlp.onUpdate.connect(self.__onUpdate)
        self.ytdlp.onCompletion.connect(self.__onCompletion)
        self.ytdlp.start()

    def __onProgressUpdate(self, progress: int):
        self.view().setProgressBarValue(progress)
        self.view().setWindowTitle(f"Progress {progress}%")

    def __onFilenameUpdate(self, filename: str):
        self.filename = filename

    def __onUpdate(self, text: str):
        self.view().setTextEditText(text)

    def __onCompletion(self, processStatus: dict):
        if processStatus["code"] == 0:
            self.filename = self.__getFixedFilename(self.filename)
            self.__onProgressUpdate(100)
            self.view().setOpenButtonEnabled()
        else:
            self.onCancelButtonClicked()
        self.__dialogCanBeClosed()

    # endregion
