from shutil import which


class DependencyStatus:
    def __init__(self):
        self.hasDependencies = True
        self.text = None


class DependencyHelper:
    @classmethod
    def __hasDependency(cls, dep: str) -> bool:
        return which(dep) is not None

    @classmethod
    def __missingDependenciesText(cls) -> str:
        return (
            "Missing dependency."
            + "\nDrop it into the same folder as "
            + "this program for it to work.\n"
        )

    @classmethod
    def __getYtdlpText(cls) -> str:
        return (
            "\nyt-dlp"
            + "\n-> Link: https://github.com/yt-dlp/yt-dlp/releases/"
            + "\n-> Download the yt-dlp.exe in the Assets section."
        )

    @classmethod
    def __getFFmpegText(cls) -> str:
        return (
            "\nFFmpeg"
            + "\n-> Link: https://github.com/BtbN/FFmpeg-Builds/releases"
            + "\n-> Download the ffmpeg-master-lastest-win64. GPL or LGPL."
        )

    @classmethod
    def getStatus(cls) -> DependencyStatus:
        status = DependencyStatus()
        hasFFmpeg = cls.__hasDependency("ffmpeg")
        hasYtdlp = cls.__hasDependency("yt-dlp")
        if hasFFmpeg and hasYtdlp:
            return status
        status.hasDependencies = False
        status.text = cls.__missingDependenciesText()
        if not hasFFmpeg:
            status.text += cls.__getFFmpegText() + "\n"
        if not hasYtdlp:
            status.text += cls.__getYtdlpText()
        return status
