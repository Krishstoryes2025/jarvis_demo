# ============================================================
# JARVIS AI GUI
# ============================================================


import os
import sys

from dotenv import dotenv_values

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import (
    QColor,
    QFont,
    QIcon,
    QMovie,
    QPainter,
    QPixmap,
    QTextBlockFormat,
    QTextCharFormat,
)
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# ============================================================
# LOAD ENV VARIABLES
# ============================================================

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "Jarvis")

# ============================================================
# PATHS
# ============================================================

current_dir = os.getcwd()

TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")

# Create folders if not exist
os.makedirs(TempDirPath, exist_ok=True)
os.makedirs(GraphicsDirPath, exist_ok=True)

# ============================================================
# GLOBAL VARIABLES
# ============================================================

old_chat_message = ""

# ============================================================
# HELPER FUNCTIONS
# ============================================================


def GraphicsDirectoryPath(filename):
    """Return graphics file path"""
    return os.path.join(GraphicsDirPath, filename)


def TempDirectoryPath(filename):
    """Return temp file path"""
    return os.path.join(TempDirPath, filename)


def ensure_file_exists(filepath, default_text=""):
    """Create file if missing"""
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(default_text)


# Create required files
ensure_file_exists(TempDirectoryPath("Mic.data"), "False")
ensure_file_exists(TempDirectoryPath("Status.data"), "Ready...")
ensure_file_exists(TempDirectoryPath("Responses.data"), "")


# ============================================================
# TEXT MODIFIERS
# ============================================================

def AnswerModifier(answer):
    """
    Remove empty lines from answer
    """
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)

    return modified_answer


def QueryModifier(query):
    """
    Format query properly
    """

    query = query.lower().strip()

    if not query:
        return ""

    question_words = [
        "how",
        "what",
        "who",
        "where",
        "when",
        "why",
        "which",
        "whose",
        "whom",
        "can you",
        "what's",
        "where's",
        "how's",
    ]

    is_question = any(query.startswith(word) for word in question_words)

    # Remove punctuation
    if query[-1] in [".", "?", "!"]:
        query = query[:-1]

    # Add proper punctuation
    if is_question:
        query += "?"
    else:
        query += "."

    return query.capitalize()


# ============================================================
# FILE STATUS FUNCTIONS
# ============================================================

def SetMicrophoneStatus(command):
    with open(TempDirectoryPath("Mic.data"), "w", encoding="utf-8") as file:
        file.write(command)


def GetMicrophoneStatus():
    with open(TempDirectoryPath("Mic.data"), "r", encoding="utf-8") as file:
        return file.read()


def SetAssistantStatus(status):
    with open(TempDirectoryPath("Status.data"), "w", encoding="utf-8") as file:
        file.write(status)


def GetAssistantStatus():
    with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
        return file.read()


def MicButtonInitialized():
    SetMicrophoneStatus("False")


def MicButtonClosed():
    SetMicrophoneStatus("True")


def ShowTextToScreen(text):
    with open(TempDirectoryPath("Responses.data"), "w", encoding="utf-8") as file:
        file.write(text)


# ============================================================
# CHAT SECTION
# ============================================================

class ChatSection(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(10, 40, 10, 20)

        # ====================================================
        # CHAT BOX
        # ====================================================

        self.chat_text_edit = QTextEdit()

        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)

        font = QFont()
        font.setPointSize(13)

        self.chat_text_edit.setFont(font)

        layout.addWidget(self.chat_text_edit)

        # ====================================================
        # GIF LABEL
        # ====================================================

        self.gif_label = QLabel()

        self.gif_label.setStyleSheet("border:none;")

        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))

        movie.setScaledSize(QSize(480, 270))

        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.gif_label.setMovie(movie)

        movie.start()

        layout.addWidget(self.gif_label)

        # ====================================================
        # STATUS LABEL
        # ====================================================

        self.label = QLabel("Ready...")

        self.label.setStyleSheet("""
            color:white;
            font-size:16px;
            border:none;
        """)

        self.label.setAlignment(Qt.AlignRight)

        layout.addWidget(self.label)

        self.setStyleSheet("background-color:black;")

        # ====================================================
        # TIMER
        # ====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)

        # 100ms refresh (better CPU performance)
        self.timer.start(100)

    # ========================================================
    # LOAD CHAT MESSAGES
    # ========================================================

    def loadMessages(self):

        global old_chat_message

        try:
            with open(
                TempDirectoryPath("Responses.data"),
                "r",
                encoding="utf-8"
            ) as file:

                messages = file.read().strip()

                if not messages:
                    return

                if old_chat_message == messages:
                    return

                self.addMessage(messages, "white")

                old_chat_message = messages

        except Exception as e:
            print("Message Load Error:", e)

    # ========================================================
    # UPDATE STATUS TEXT
    # ========================================================

    def SpeechRecogText(self):

        try:
            with open(
                TempDirectoryPath("Status.data"),
                "r",
                encoding="utf-8"
            ) as file:

                messages = file.read()

                self.label.setText(messages)

        except Exception as e:
            print("Status Read Error:", e)

    # ========================================================
    # ADD MESSAGE TO CHAT
    # ========================================================

    def addMessage(self, message, color):

        cursor = self.chat_text_edit.textCursor()

        text_format = QTextCharFormat()
        text_format.setForeground(QColor(color))

        block_format = QTextBlockFormat()
        block_format.setTopMargin(10)
        block_format.setLeftMargin(10)

        cursor.setCharFormat(text_format)
        cursor.setBlockFormat(block_format)

        cursor.insertText(message + "\n")

        self.chat_text_edit.setTextCursor(cursor)


# ============================================================
# INITIAL SCREEN
# ============================================================

class InitialScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()

        screen_width = geometry.width()
        screen_height = geometry.height()

        layout = QVBoxLayout()

        # ====================================================
        # GIF
        # ====================================================

        gif_label = QLabel()

        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))

        movie.setScaledSize(QSize(screen_width, int(screen_width / 16 * 9)))

        gif_label.setMovie(movie)

        gif_label.setAlignment(Qt.AlignCenter)

        movie.start()

        layout.addWidget(gif_label)

        # ====================================================
        # STATUS LABEL
        # ====================================================

        self.label = QLabel("Ready...")

        self.label.setStyleSheet("""
            color:white;
            font-size:16px;
        """)

        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)

        # ====================================================
        # MIC ICON
        # ====================================================

        self.icon_label = QLabel()

        self.toggled = True

        self.load_icon("Mic_on.png")

        self.icon_label.mousePressEvent = self.toggle_icon

        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        # ====================================================
        # WINDOW SETTINGS
        # ====================================================

        self.setLayout(layout)

        self.setFixedWidth(screen_width)
        self.setFixedHeight(screen_height)

        self.setStyleSheet("background-color:black;")

        # ====================================================
        # TIMER
        # ====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.SpeechRecogText)

        self.timer.start(100)

    # ========================================================
    # LOAD ICON
    # ========================================================

    def load_icon(self, filename, width=60, height=60):

        pixmap = QPixmap(GraphicsDirectoryPath(filename))

        new_pixmap = pixmap.scaled(width, height)

        self.icon_label.setPixmap(new_pixmap)

    # ========================================================
    # TOGGLE MIC ICON
    # ========================================================

    def toggle_icon(self, event=None):

        if self.toggled:

            self.load_icon("Mic_off.png")

            MicButtonClosed()

        else:

            self.load_icon("Mic_on.png")

            MicButtonInitialized()

        self.toggled = not self.toggled

    # ========================================================
    # UPDATE STATUS LABEL
    # ========================================================

    def SpeechRecogText(self):

        try:
            with open(
                TempDirectoryPath("Status.data"),
                "r",
                encoding="utf-8"
            ) as file:

                messages = file.read()

                self.label.setText(messages)

        except Exception as e:
            print("Status Error:", e)


# ============================================================
# MESSAGE SCREEN
# ============================================================

class MessageScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()

        screen_width = geometry.width()
        screen_height = geometry.height()

        layout = QVBoxLayout()

        chat_section = ChatSection()

        layout.addWidget(chat_section)

        self.setLayout(layout)

        self.setFixedWidth(screen_width)
        self.setFixedHeight(screen_height)

        self.setStyleSheet("background-color:black;")


# ============================================================
# CUSTOM TOP BAR
# ============================================================

class CustomTopBar(QWidget):

    def __init__(self, parent, stacked_widget):
        super().__init__(parent)

        self.stacked_widget = stacked_widget

        self.initUI()

    def initUI(self):

        self.setFixedHeight(50)

        layout = QHBoxLayout(self)

        # ====================================================
        # TITLE
        # ====================================================

        title_label = QLabel(f"{Assistantname} AI")

        title_label.setStyleSheet("""
            color:black;
            font-size:18px;
            background-color:white;
        """)

        # ====================================================
        # HOME BUTTON
        # ====================================================

        home_button = QPushButton("Home")

        home_button.setIcon(QIcon(GraphicsDirectoryPath("Home.png")))

        home_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )

        # ====================================================
        # CHAT BUTTON
        # ====================================================

        chat_button = QPushButton("Chat")

        chat_button.setIcon(QIcon(GraphicsDirectoryPath("Chats.png")))

        chat_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(1)
        )

        # ====================================================
        # MINIMIZE BUTTON
        # ====================================================

        minimize_button = QPushButton()

        minimize_button.setIcon(
            QIcon(GraphicsDirectoryPath("Minimize2.png"))
        )

        minimize_button.clicked.connect(self.minimizeWindow)

        # ====================================================
        # MAXIMIZE BUTTON
        # ====================================================

        self.maximize_button = QPushButton()

        self.maximize_icon = QIcon(
            GraphicsDirectoryPath("Maximize.png")
        )

        self.restore_icon = QIcon(
            GraphicsDirectoryPath("Minimize.png")
        )

        self.maximize_button.setIcon(self.maximize_icon)

        self.maximize_button.clicked.connect(self.maximizeWindow)

        # ====================================================
        # CLOSE BUTTON
        # ====================================================

        close_button = QPushButton()

        close_button.setIcon(QIcon(GraphicsDirectoryPath("Close.png")))

        close_button.clicked.connect(self.closeWindow)

        # ====================================================
        # STYLE
        # ====================================================

        button_style = """
            QPushButton{
                height:40px;
                background-color:white;
                color:black;
                border:none;
                padding:5px;
            }

            QPushButton:hover{
                background-color:#dddddd;
            }
        """

        home_button.setStyleSheet(button_style)
        chat_button.setStyleSheet(button_style)
        minimize_button.setStyleSheet(button_style)
        self.maximize_button.setStyleSheet(button_style)
        close_button.setStyleSheet(button_style)

        # ====================================================
        # ADD WIDGETS
        # ====================================================

        layout.addWidget(title_label)

        layout.addStretch(1)

        layout.addWidget(home_button)
        layout.addWidget(chat_button)

        layout.addStretch(1)

        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

        self.setStyleSheet("background-color:white;")

        # ====================================================
        # WINDOW DRAGGING
        # ====================================================

        self.offset = None

    # ========================================================
    # PAINT EVENT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(self.rect(), Qt.white)

        super().paintEvent(event)

    # ========================================================
    # MINIMIZE
    # ========================================================

    def minimizeWindow(self):
        self.parent().showMinimized()

    # ========================================================
    # MAXIMIZE / RESTORE
    # ========================================================

    def maximizeWindow(self):

        if self.parent().isMaximized():

            self.parent().showNormal()

            self.maximize_button.setIcon(self.maximize_icon)

        else:

            self.parent().showMaximized()

            self.maximize_button.setIcon(self.restore_icon)

    # ========================================================
    # CLOSE
    # ========================================================

    def closeWindow(self):
        self.parent().close()

    # ========================================================
    # WINDOW DRAGGING
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.parent().pos()

    def mouseMoveEvent(self, event):

        if self.offset and event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos() - self.offset)


# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.initUI()

    def initUI(self):

        screen = QApplication.primaryScreen()

        geometry = screen.availableGeometry()

        screen_width = geometry.width()
        screen_height = geometry.height()

        # ====================================================
        # STACKED WIDGET
        # ====================================================

        self.stacked_widget = QStackedWidget()

        self.initial_screen = InitialScreen()
        self.message_screen = MessageScreen()

        self.stacked_widget.addWidget(self.initial_screen)
        self.stacked_widget.addWidget(self.message_screen)

        self.setCentralWidget(self.stacked_widget)

        # ====================================================
        # TOP BAR
        # ====================================================

        top_bar = CustomTopBar(self, self.stacked_widget)

        self.setMenuWidget(top_bar)

        # ====================================================
        # WINDOW SETTINGS
        # ====================================================

        self.setGeometry(0, 0, screen_width, screen_height)

        self.setStyleSheet("background-color:black;")


# ============================================================
# RUN APPLICATION
# ============================================================

def GraphicalUserInterface():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec_())


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    GraphicalUserInterface()