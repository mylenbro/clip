from re import search
from typing import List
from pathlib import Path
from PySide6.QtCore import Signal
from Models.UserOptions import UserOptions
from Helpers.Converter import Time
from Process.Process import Process


class YtdlpProcess(Process):
    onProgressUpdate = Signal(int)
    onFilenameUpdate = Signal(str)

    def __init__(self, options: UserOptions):
        args = self.__getArguments(options)
        super().__init__("yt-dlp", args)
        if options.trimTo() != 0 and options.trimFrom() != 0:
            self.trimTo = options.trimTo() - options.trimFrom()
        else:
            self.trimTo = options.trimTo()
        self.doubleDownload = False
        self.hasDownloadedVideo = False
        self.onOutput.connect(self.__onStandardOutput)
        self.onError.connect(self.__onStandardError)

    # region Events

    def __onStandardOutput(self, text: str):
        if text.find("[download]") != -1:
            self.__parseFilename(text)
            self.__parseProgressYtdlp(text)
        if text.find("[info]") != -1:
            self.__parseFormats(text)

    def __onStandardError(self, text: str):
        if text.find("time=") != -1:
            self.__parseProgressFFmpeg(text)
        if text.find("Duration: ") != -1:
            self.__parseDuration(text)

    # endregion

    # region Parsing

    def __parseDuration(self, text: str):
        duration = search(r"(?!(Duration:\s))(\d\d:\d\d:\d\d.\d\d)(?=,)", text)
        if not duration:
            return
        durationMs = Time.toMs(duration[0])
        if self.trimTo > durationMs:
            self.trimTo = durationMs

    def __parseFormats(self, text: str):
        lines = text.split("\n")
        if not lines:
            return
        words = lines[0].split(" ")
        if not words:
            return
        formats = words[-1]
        if formats.find("+") != -1:
            self.doubleDownload = True

    def __parseProgressYtdlp(self, text: str):
        time = search(r"\S+(?=%\s+of)", text)
        if not time:
            return
        progress = float(time[0])
        self.__updateProgress(progress, text)

    def __parseProgressFFmpeg(self, text: str):
        if search(r"(speed=N/A)", text) is not None:
            return
        time = search(r"(\d{2}:\d{2}:\d{2}\.\d{2})", text)
        if time:
            currentMs = Time.toMs(time[0])
            totalMs = self.trimTo
            progress = int((currentMs / totalMs) * 100)
            self.__updateProgress(progress, text)

    def __updateProgress(self, progress: float, text: str) -> None:
        if self.doubleDownload:
            progress = progress * 0.5
        if self.hasDownloadedVideo:
            progress = progress + 50
        if self.doubleDownload and progress == 50 and text.find("ETA") == -1:
            self.hasDownloadedVideo = True
        progress = int(progress)
        self.onProgressUpdate.emit(progress)

    def __parseOnDowloading(self, text: str) -> str:
        filepath = text.split("[download] Destination: ")[1]
        if filepath.find("\n\r") != -1:
            filepath = text.split("\n")[0]
        else:
            filepath = filepath.replace("\n", "")
        return filepath

    def __parseAlreadyDownloaded(self, text: str) -> str:
        return (
            text.replace("[download] ", "")
            .split("\n")[0]
            .replace(" has already been downloaded", "")
        )

    def __parseFilename(self, text: str):
        filepath = None
        if text.find("[download] Destination: ") != -1:
            filepath = self.__parseOnDowloading(text)
        elif text.find("has already been downloaded") != -1:
            filepath = self.__parseAlreadyDownloaded(text)
        if not filepath:
            return
        filename = Path(filepath).name
        self.onFilenameUpdate.emit(filename)

    # endregion

    # region Private

    def __getArguments(self, options: UserOptions) -> List[str]:
        trimFrom = options.trimFrom() // 1000
        trimTo = options.trimTo() // 1000
        settings = options.settings()
        args: List[str] = []
        # args.append("--verbose")
        args.append("--compat-options")
        args.append("no-direct-merge")
        if options.forceKeyframes():
            args.append("--force-keyframes-at-cuts")
        if settings.outputFormat():
            args.append("-o")
            args.append(settings.outputFormat())
        if settings.destination():
            args.append("--paths")
            args.append(settings.destination())
        if not (trimFrom == 0 and trimTo == 0):
            args.append("--download-sections")
            args.append(f"*{trimFrom}-{trimTo}")
        args.append(options.link())
        return args

    # endregion
