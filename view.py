from PyQt6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem, QTabWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QHBoxLayout, QSplitter, QVBoxLayout, QListWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

class View(QMainWindow):
    """
    The View class represents the GUI of the application.
    It extends QMainWindow and uses a .ui file for its layout.
    """

    def __init__(self):
        """
        Initializes the View class.
        Loads the UI and initializes the UI components.
        """
        super(View, self).__init__()
        loadUi('placeholder.ui', self)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI components.
        Finds and assigns the QTabWidget, QTreeWidget, QLineEdit, QPushButton, and QLabel from the loaded UI.
        """
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

        # Initialize project list widget
        self.projectListWidget = self.findChild(QListWidget, 'projectListWidget')

        # Set emojis only
        self.addButton.setText("➕")
        self.syncButton.setText("🔄")
        self.loadButton.setText("📂")

        # Set tooltips
        self.addButton.setToolTip("Click to add a new requirement.")
        self.syncButton.setToolTip("Click to sync with the remote server.")
        self.loadButton.setToolTip("Click to load data from local storage.")

        # Style currentRequirementLabel as a smaller header
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        self.currentRequirementLabel.setFont(header_font)
        self.currentRequirementLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Style descriptionLabel and other labels to be larger
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

        # Retrieve the existing layout and add spacing
        card_layout = self.currentRequirementLabel.parentWidget().layout()
        card_layout.addWidget(self.currentRequirementLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)  # Add spacing between the labels
        card_layout.addWidget(self.descriptionLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)  # Add spacing between the labels
        card_layout.addWidget(self.codeCommentsLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)  # Add spacing between the labels
        card_layout.addWidget(self.traceLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)  # Add spacing between the labels
        card_layout.addWidget(self.generalCommentsLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addStretch()

        # Ensure the central widget has a layout
        central_layout = self.centralWidget().layout()
        if central_layout is None:
            central_layout = QVBoxLayout(self.centralWidget())
            self.centralWidget().setLayout(central_layout)

        # Add the QListWidget to the existing layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.projectListWidget)
        splitter.addWidget(self.tabWidget)
        central_layout.addWidget(splitter)

    def populate_tree(self, items):
        """
        Populates the QTreeWidget with system-level items.

        Args:
            items (list of str): List of item names to be added as system-level items in the QTreeWidget.
        """
        self.treeWidget.clear()
        for item in items:
            system_item = QTreeWidgetItem([item])
            self.treeWidget.addTopLevelItem(system_item)
        # Add the special "Add System Requirement" item
        self.add_special_item()

    def add_special_item(self):
        """
        Adds a special item to the tree that allows adding a new system requirement.
        """
        self.special_item = QTreeWidgetItem(["Add System Requirement"])
        font = self.special_item.font(0)
        font.setBold(True)
        self.special_item.setFont(0, font)
        self.treeWidget.addTopLevelItem(self.special_item)

    def update_card(self, name, description, code_comments, trace, general_comments):
        """
        Updates the card with the current requirement details.
        
        Args:
            name (str): The name of the current requirement.
            description (str): The description of the current requirement.
            code_comments (str): The code comments of the current requirement.
            trace (str): The trace of the current requirement.
            general_comments (str): The general comments of the current requirement.
        """
        self.currentRequirementLabel.setText(name)
        self.descriptionLabel.setText(description)
        self.codeCommentsLabel.setText(code_comments)
        self.traceLabel.setText(trace)
        self.generalCommentsLabel.setText(general_comments)

    def populate_project_list(self, projects):
        """
        Populates the project list with the given project names.

        Args:
            projects (list of str): List of project names.
        """
        self.projectListWidget.clear()
        for project in projects:
            self.projectListWidget.addItem(project)
        # Add the special "Create New Project" item
        self.add_special_project_item()

    def add_special_project_item(self):
        """
        Adds a special item to the project list for creating a new project.
        """
        item = QListWidgetItem("Create New Project")
        font = item.font()
        font.setBold(True)
        item.setFont(font)
        self.projectListWidget.addItem(item)
