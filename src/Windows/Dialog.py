from PySide6.QtWidgets import (
    QDialog,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QProgressBar,
    QMessageBox,
)
from PySide6.QtGui import QCloseEvent
from Presenters.DialogPresenter import DialogPresenter
from Views.DialogView import DialogView
from Models.UserOptions import UserOptions


class Dialog(QDialog, DialogView):
    def __init__(self, userOptions: UserOptions):
        super().__init__()
        self.buildUI()
        self.presenter = DialogPresenter(self, userOptions)
        self.presenter.viewDidLoad()

    def buildUI(self):
        self.setWindowTitle("Progress")
        self.setModal(True)
        self.resize(800, 500)

        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        buttonsLayout = QHBoxLayout()
        self.openButton = QPushButton("Open")
        self.openButton.setDefault(True)
        self.openButton.setDisabled(True)
        self.openButton.clicked.connect(self.onOpenButtonClicked)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.onCancelButtonClicked)

        self.setLayout(layout)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.progressBar)
        layout.addLayout(buttonsLayout)
        buttonsLayout.addWidget(self.openButton)
        buttonsLayout.addWidget(self.cancelButton)

    # region Events

    def closeEvent(self, _: QCloseEvent):
        self.presenter.onDialogClose()

    def onOpenButtonClicked(self):
        self.presenter.onOpenButtonClicked()

    def onCancelButtonClicked(self):
        self.presenter.onCancelButtonClicked()

    # endregion

    # region View

    def setTextEditText(self, text: str):
        self.textEdit.append(text)

    def setCancelButtonText(self, text: str):
        self.cancelButton.setText(text)

    def setProgressBarValue(self, value: int):
        self.progressBar.setValue(value)

    def setOpenButtonEnabled(self):
        self.openButton.setEnabled(True)

    def closeDialog(self):
        self.reject()

    def setDialogTitle(self, text: str):
        self.setWindowTitle(text)

    def showErrorMessage(self, text: str, informativeText: str):
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Critical)
        messageBox.setText(text)
        messageBox.setInformativeText(informativeText)
        messageBox.setWindowTitle("Error")
        messageBox.exec()

    # endregion
