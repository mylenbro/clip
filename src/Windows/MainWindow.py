from PySide6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QFileDialog,
    QCheckBox,
    QLabel,
)
from PySide6.QtCore import Qt
from Windows.Dialog import Dialog
from Presenters.MainWindowPresenter import MainWindowPresenter
from Views.MainWindowView import MainWindowView
from Models.UserOptions import UserOptions


class MainWindow(QMainWindow, MainWindowView):
    def __init__(self):
        super().__init__()
        self.buildUI()
        self.presenter = MainWindowPresenter(self)
        self.presenter.viewDidLoad()

    def buildUI(self):
        self.setWindowTitle("Clip")
        self.setFixedHeight(330)
        self.setFixedWidth(544)

        widget = QWidget()
        layout = QVBoxLayout()
        mainGroupBox = QGroupBox("Main")
        mainGroupBox.setFixedHeight(90)
        mainLayout = QFormLayout()
        mainLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        ffmpegGroupBox = QGroupBox("Settings")
        # ffmpegGroupBox.setFixedHeight(100)
        ffmpegLayout = QFormLayout()
        ffmpegLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.linkLineEdit = QLineEdit()
        self.linkLineEdit.textEdited.connect(self.onLinkEdited)
        self.linkLineEdit.returnPressed.connect(self.onReturnPressed)
        destinationLayout = QHBoxLayout()
        self.destinationLineEdit = QLineEdit()
        self.destinationLineEdit.textChanged.connect(self.onDestinationChanged)
        self.destinationLineEdit.returnPressed.connect(self.onReturnPressed)
        browseButton = QPushButton("Browse")
        browseButton.clicked.connect(self.onBrowseButtonClicked)
        timeWidget = QWidget()
        timeLayout = QHBoxLayout()
        timeLabelLeft = QLabel("Trim:")
        self.trimFromLineEdit = QLineEdit("00:00:00")
        self.trimFromLineEdit.setInputMask("99:99:99;0")
        self.trimFromLineEdit.setFixedWidth(60)
        self.trimFromLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.trimFromLineEdit.textChanged.connect(self.onTrimFromEdited)
        self.trimFromLineEdit.returnPressed.connect(self.onReturnPressed)
        xLabel = QLabel("x")
        self.trimToLineEdit = QLineEdit("00:00:00")
        self.trimToLineEdit.setInputMask("99:99:99;0")
        self.trimToLineEdit.setFixedWidth(60)
        self.trimToLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.trimToLineEdit.textEdited.connect(self.onTrimToEdited)
        self.trimToLineEdit.returnPressed.connect(self.onReturnPressed)
        timeLabelRight = QLabel(
            "HH:MM:SS format. If left untouched, download will" + "\nbe faster."
        )
        keyFramesLayout = QHBoxLayout()
        keyFramesWidget = QWidget()
        self.forceKeyFramesCheckBox = QCheckBox()
        self.forceKeyFramesCheckBox.stateChanged.connect(
            self.onForceKeyframesStateChanged
        )
        forceKeyFramesLabelLeft = QLabel("Force key-frames at cut:")
        forceKeyFramesLabelRight = QLabel(
            "Use this if the output file was not trimmed correctly.\n"
            + "Re-encodes. Slower download and higher CPU usage."
        )
        formatWidget = QWidget()
        formatLayout = QHBoxLayout()
        formatLabelLeft = QLabel("Format:")
        self.formatLineEdit = QLineEdit()
        self.formatLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formatLineEdit.setFixedWidth(138)
        self.formatLineEdit.textEdited.connect(self.onFormatEdited)
        self.formatLineEdit.returnPressed.connect(self.onReturnPressed)
        formatLabelRight = QLabel(
            "How your file will be named. "
            + 'See <a href="https://github.com/yt-dlp/yt-dlp#output-template">'
            + "formats template</a>."
        )
        formatLabelRight.setTextFormat(Qt.TextFormat.RichText)
        formatLabelRight.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )
        formatLabelRight.setOpenExternalLinks(True)
        supportedLinksLabel = QLabel(
            '<a href="'
            + 'https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md">'
            + "Supported sites</a> by yt-dlp"
        )
        supportedLinksLabel.setTextFormat(Qt.TextFormat.RichText)
        supportedLinksLabel.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )
        supportedLinksLabel.setOpenExternalLinks(True)
        supportedLinksLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        downloadButton = QPushButton("Download")
        downloadButton.clicked.connect(self.onDownloadPushButtonClicked)

        self.setCentralWidget(widget)
        widget.setLayout(layout)
        layout.addWidget(mainGroupBox)
        mainGroupBox.setLayout(mainLayout)
        mainLayout.addRow("Link:", self.linkLineEdit)
        mainLayout.addRow("Destination:", destinationLayout)
        destinationLayout.addWidget(self.destinationLineEdit)
        destinationLayout.addWidget(browseButton)
        layout.addWidget(ffmpegGroupBox)
        ffmpegGroupBox.setLayout(ffmpegLayout)
        timeWidget.setLayout(timeLayout)
        timeLayout.addWidget(timeLabelLeft)
        timeLayout.addWidget(self.trimFromLineEdit)
        timeLayout.addWidget(xLabel)
        timeLayout.addWidget(self.trimToLineEdit)
        timeLayout.addStretch(0)
        keyFramesWidget.setLayout(keyFramesLayout)
        keyFramesLayout.addWidget(forceKeyFramesLabelLeft)
        keyFramesLayout.addWidget(self.forceKeyFramesCheckBox)
        formatWidget.setLayout(formatLayout)
        formatLayout.addWidget(formatLabelLeft)
        formatLayout.addWidget(self.formatLineEdit)
        ffmpegLayout.addRow(timeWidget, timeLabelRight)
        ffmpegLayout.addRow(formatWidget, formatLabelRight)
        ffmpegLayout.addRow(keyFramesWidget, forceKeyFramesLabelRight)

        layout.addWidget(downloadButton)
        layout.addWidget(supportedLinksLabel)
        layout.addStretch(0)

    # region Events

    def onDownloadPushButtonClicked(self):
        self.presenter.onDownloadPushButtonClicked()

    def showDialog(self, userOptions: UserOptions):
        dialog = Dialog(userOptions)
        dialog.exec()

    def onBrowseButtonClicked(self):
        dialog = QFileDialog()
        dialog.setDirectory(self.destinationLineEdit.text())
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        if dialog.exec():
            destination = dialog.directory().absolutePath()
            self.destinationLineEdit.setText(destination)

    def onLinkEdited(self, text: str):
        self.presenter.onLinkEdited(text)

    def onDestinationChanged(self, text: str):
        self.presenter.onDestinationChanged(text)

    def onTrimFromEdited(self, _: str):
        self.presenter.onTrimFromEdited(self.trimFromLineEdit.displayText())

    def onTrimToEdited(self, _: str):
        self.presenter.onTrimToEdited(self.trimToLineEdit.displayText())

    def onFormatEdited(self, text: str):
        self.presenter.onFormatEdited(text)

    def onForceKeyframesStateChanged(self, state: int):
        self.presenter.onForceKeyframesStateChanged(state)

    def onReturnPressed(self):
        self.presenter.onDownloadPushButtonClicked()

    # endregion

    # region View

    def setDestination(self, destination: str):
        self.destinationLineEdit.setText(destination)

    def setOutputFormat(self, outputFormat: str):
        self.formatLineEdit.setText(outputFormat)

    # endregion
