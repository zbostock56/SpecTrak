from PyQt6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem, QTabWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QSplitter, QListWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

class View(QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        loadUi('placeholder.ui', self)
        self.init_ui()

    def init_ui(self):
        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.searchBar = self.findChild(QLineEdit, 'searchBar')
        self.addButton = self.findChild(QPushButton, 'addButton')
        self.syncButton = self.findChild(QPushButton, 'syncButton')
        self.loadButton = self.findChild(QPushButton, 'loadButton')
        self.currentRequirementLabel = self.findChild(QLabel, 'currentRequirementLabel')
        self.descriptionLabel = self.findChild(QLabel, 'descriptionLabel')
        self.codeCommentsLabel = self.findChild(QLabel, 'codeCommentsLabel')
        self.traceLabel = self.findChild(QLabel, 'traceLabel')
        self.generalCommentsLabel = self.findChild(QLabel, 'generalCommentsLabel')

        self.projectListWidget = self.findChild(QListWidget, 'projectListWidget')

        self.addButton.setText("➕")
        self.syncButton.setText("🔄")
        self.loadButton.setText("📂")

        self.addButton.setToolTip("Click to add a new requirement.")
        self.syncButton.setToolTip("Click to sync with the remote server.")
        self.loadButton.setToolTip("Click to load data from local storage.")

        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        self.currentRequirementLabel.setFont(header_font)
        self.currentRequirementLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        description_font = QFont()
        description_font.setPointSize(12)
        self.descriptionLabel.setFont(description_font)
        self.descriptionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.descriptionLabel.setWordWrap(True)

        self.codeCommentsLabel.setFont(description_font)
        self.codeCommentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.codeCommentsLabel.setWordWrap(True)

        self.traceLabel.setFont(description_font)
        self.traceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.traceLabel.setWordWrap(True)

        self.generalCommentsLabel.setFont(description_font)
        self.generalCommentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generalCommentsLabel.setWordWrap(True)

        card_layout = self.currentRequirementLabel.parentWidget().layout()
        card_layout.addWidget(self.currentRequirementLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.descriptionLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.codeCommentsLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.traceLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.generalCommentsLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addStretch()

        central_layout = self.centralWidget().layout()
        if central_layout is None:
            central_layout = QVBoxLayout(self.centralWidget())
            self.centralWidget().setLayout(central_layout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.projectListWidget)
        splitter.addWidget(self.tabWidget)
        central_layout.addWidget(splitter)

    def populate_tree(self, items):
        self.treeWidget.clear()
        for item in items:
            system_item = QTreeWidgetItem([item])
            self.treeWidget.addTopLevelItem(system_item)
        self.add_special_item()

    def add_special_item(self):
        self.special_item = QTreeWidgetItem(["Add System Requirement"])
        font = self.special_item.font(0)
        font.setBold(True)
        self.special_item.setFont(0, font)
        self.treeWidget.addTopLevelItem(self.special_item)

    def update_card(self, name, description, code_comments, trace, general_comments):
        self.currentRequirementLabel.setText(name)
        self.descriptionLabel.setText(description)
        self.codeCommentsLabel.setText(code_comments)
        self.traceLabel.setText(trace)
        self.generalCommentsLabel.setText(general_comments)

    def populate_project_list(self, projects):
        self.projectListWidget.clear()
        for project in projects:
            self.projectListWidget.addItem(project)
        self.add_special_project_item()

    def add_special_project_item(self):
        item = QListWidgetItem("Create New Project")
        font = item.font()
        font.setBold(True)
        item.setFont(font)
        self.projectListWidget.addItem(item)
