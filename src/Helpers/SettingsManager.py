from json import dump, load
from Models.Settings import Settings
from Helpers.File import File


class SettingsManager:
    @classmethod
    def save(cls, settings: Settings):
        with open("settings.json", "w", encoding="utf-8") as f:
            dump(settings.__dict__, f, ensure_ascii=False)

    @classmethod
    def load(cls) -> Settings:
        settings = None
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                data = load(f)
                settings = Settings(**data)
                if not settings.outputFormat():
                    settings.setOutputFormat(cls.__defaultOutputFormat())
        except FileNotFoundError:
            settings = cls.__createDefaultSettings()
            cls.save(settings)
        return settings

    @classmethod
    def __createDefaultSettings(cls) -> Settings:
        outputFormat = cls.__defaultOutputFormat()
        directory = File.currentDirectory()
        settings = Settings(outputFormat, directory)
        return settings

    @classmethod
    def __defaultOutputFormat(cls) -> str:
        return "%(title)s [%(id)s].%(ext)s"
