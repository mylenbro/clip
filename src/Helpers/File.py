from pathlib import Path
from typing import List
from difflib import SequenceMatcher
from subprocess import run
from platform import system


class File:
    @classmethod
    def __getAllFiles(cls, directory: str) -> List[str]:
        files = []
        for path in Path(directory).iterdir():
            if path.is_file():
                files.append(path.name)
        return files

    @classmethod
    def attemptToGetFile(cls, directory: str, filename: str) -> str:
        if not filename:
            return ""

        files = File.__getAllFiles(directory)
        if not files:
            return ""

        data = [(file, SequenceMatcher(None, filename, file).ratio()) for file in files]
        data.sort(key=lambda tup: tup[1], reverse=True)

        mostSimilar = data[0][0]
        return mostSimilar

    @classmethod
    def currentDirectory(cls) -> str:
        return str(Path().resolve())

    @classmethod
    def getPath(cls, directory: str, filename: str) -> str:
        sanitized = File.__sanitizeFilename(filename)
        filepath = f"{directory}\\{sanitized}"
        path = Path(filepath)
        return str(path)

    @classmethod
    def __sanitizeFilename(cls, filename: str) -> str:
        return filename.translate({ord(i): None for i in '\\/:*?"<>|'})

    @classmethod
    def open(cls, path: str) -> None:
        systemPlatform = system().lower()
        if systemPlatform == "darwin":  # macOS
            run(["open", path])
        elif systemPlatform == "linux":
            run(["xdg-open", path])
        elif systemPlatform == "windows":
            run(["start", path], shell=True)
        else:
            raise ("Unsupported operating system")
