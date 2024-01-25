# from exitstatus import ExitStatus
from psutil import Process as PSUProcess
from PySide6.QtCore import QProcess, Signal, QObject, QByteArray


class Process(QObject):
    onCompletion = Signal(dict)
    onOutput = Signal(str)
    onError = Signal(str)
    onUpdate = Signal(str)

    def __init__(self, program: str, args: str):
        super().__init__()
        process = QProcess()
        self.process = process
        process.readyReadStandardOutput.connect(self.__onOutput)
        process.readyReadStandardError.connect(self.__onError)
        process.finished.connect(self.__onCompletion)
        self.process.setProgram(program)
        self.process.setArguments(args)

    def start(self):
        self.process.start()

    def stop(self):
        pid = self.process.processId()
        if pid > 0:
            parent = PSUProcess(pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        self.process.kill()

    # def __onCompletion(self, code: int, status: ExitStatus):
    def __onCompletion(self, code: int, status):
        dic = {"code": code, "status": status}
        self.onCompletion.emit(dic)

    def __onOutput(self):
        text = self.__getText(self.process.readAllStandardOutput())
        self.onOutput.emit(text)
        self.onUpdate.emit(text)

    def __onError(self):
        text = self.__getText(self.process.readAllStandardError())
        self.onError.emit(text)
        self.onUpdate.emit(text)

    def __getText(self, byteArray: QByteArray) -> str:
        return byteArray.data().decode("mbcs", errors="ignore")
