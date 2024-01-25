class Settings:
    def __init__(self, __outputFormat: str, __destination: str):
        self.__outputFormat = __outputFormat
        self.__destination = __destination

    def outputFormat(self) -> str:
        return self.__outputFormat

    def setOutputFormat(self, outputFormat: str):
        self.__outputFormat = outputFormat

    def destination(self) -> str:
        return self.__destination

    def setDestination(self, destination: str):
        self.__destination = destination
