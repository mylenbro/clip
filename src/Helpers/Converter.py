class Time:
    @classmethod
    def toMs(cls, timeString: str) -> int:
        hours, minutes, seconds = timeString.split(":")
        seconds, milliseconds = seconds.split(".")
        hours, minutes, seconds, milliseconds = map(
            int, (hours, minutes, seconds, milliseconds)
        )
        totalMs = (
            (hours * 60 * 60 * 1000)
            + (minutes * 60 * 1000)
            + (seconds * 1000)
            + milliseconds * 10  # ffmpeg uses .xx instead of .xxxx
        )
        return totalMs
