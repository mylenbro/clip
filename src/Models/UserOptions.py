from Helpers.Converter import Time
from Models.Settings import Settings


class UserOptions:
    def __init__(self, settings: Settings):
        self.__link = ""
        self.__settings = settings
        self.__trimFrom = 0
        self.__trimTo = 0
        self.__forceKeyframes = False

    def link(self) -> str:
        return self.__link

    def setLink(self, link: str):
        self.__link = link

    def settings(self) -> Settings:
        return self.__settings

    def setSettings(self, settings: str):
        self.__settings = settings

    def trimFrom(self) -> int:
        return self.__trimFrom

    def setTrimFrom(self, trimFrom: str):
        self.__trimFrom = Time.toMs(trimFrom)

    def trimTo(self) -> int:
        return self.__trimTo

    def setTrimTo(self, trimTo: str):
        self.__trimTo = Time.toMs(trimTo)

    def forceKeyframes(self) -> bool:
        return self.__forceKeyframes

    def setForceKeyframes(self, forceKeyframes: bool):
        self.__forceKeyframes = forceKeyframes
