import sys
from PyQt6.QtWidgets import QApplication, QTreeWidgetItem, QMessageBox, QListWidgetItem, QInputDialog
from model import Model
from view import View

class Controller:
    """
    The Controller class connects the Model and the View.
    It handles user interaction and updates the view and model accordingly.
    """

    def __init__(self):
        """
        Initializes the Controller class.
        Sets up the application, model, and view.
        Connects signals and slots.
        """
        self.app = QApplication(sys.argv)
        self.model = Model()
        self.view = View()
        self.tree_data = self.generate_tree_data()
        self.project_data = self.generate_project_data()
        self.current_project = None
        self.populate_project_list()

        # Event handlers
        self.view.treeWidget.itemClicked.connect(self.handle_item_click)
        self.view.searchBar.textChanged.connect(self.handle_search)
        self.view.addButton.clicked.connect(self.add_requirement)
        self.view.syncButton.clicked.connect(self.sync_with_remote)
        self.view.loadButton.clicked.connect(self.load_from_local)
        self.view.projectListWidget.itemClicked.connect(self.handle_project_selection)

    def generate_tree_data(self):
        """
        Generates the hierarchical tree data.
        
        Returns:
            list: A list of dictionaries representing the tree structure.
        """
        tree_data = []

        for i in range(1, 10):
            system_level = f"System Requirement R{str(i).zfill(6)}"
            high_level_reqs = []

            for j in range(1, 6):
                high_level_req = f"High Level Requirement R{str(i).zfill(6)}.{j}"
                low_level_reqs = [f"Low Level Requirement R{str(i).zfill(6)}.{j}.{k}" for k in range(1, 6)]
                high_level_reqs.append({"name": high_level_req, "children": low_level_reqs})

            tree_data.append({"name": system_level, "children": high_level_reqs})

        return tree_data

    def generate_project_data(self):
        """
        Generates dummy project data. Each project has its own tree structure.

        Returns:
            dict: A dictionary with project names as keys and tree data as values.
        """
        project_data = {
            "Project A": self.generate_tree_data(),
            "Project B": self.generate_tree_data(),
            "Project C": self.generate_tree_data(),
        }
        return project_data

    def populate_tree(self, tree_data=None):
        """
        Populates the QTreeWidget with items from the hierarchical tree data.
        """
        if tree_data is None:
            tree_data = self.tree_data
        # Hide the header
        self.view.treeWidget.setHeaderHidden(True)
        self.view.treeWidget.clear()
        self.system_level_items = []

        for item in tree_data:
            system_item = QTreeWidgetItem([item["name"]])
            self.view.treeWidget.addTopLevelItem(system_item)
            self.system_level_items.append(system_item)
            self.add_child_items(system_item, item["children"])

        self.view.add_special_item()

    def add_child_items(self, parent_item, children):
        """
        Adds child items to a given parent item in the QTreeWidget.

        Args:
            parent_item (QTreeWidgetItem): The parent item to which child items will be added.
            children (list of dict): List of child items to be added under the parent item.
        """
        for child in children:
            if isinstance(child, dict):
                child_item = QTreeWidgetItem([child["name"]])
                parent_item.addChild(child_item)
                self.add_child_items(child_item, child["children"])
            else:
                child_item = QTreeWidgetItem([child])
                parent_item.addChild(child_item)

    def handle_item_click(self, item, column):
        """
        Handles the click event on a tree item.
        Updates the card with the selected item details.

        Args:
            item (QTreeWidgetItem): The clicked item in the QTreeWidget.
            column (int): The column index of the clicked item.
        """
        self.selected_item = item

        if item == self.view.special_item:
            self.add_system_requirement()
        else:
            # Update the card with the current requirement details
            name = item.text(0)
            description = f"Description for {name}. This is a detailed description that should wrap around to test the word wrapping functionality in the label."
            code_comments = f"Code comments for {name}. This is a sample code comment that is also quite long to test word wrapping."
            trace = f"Trace for {name}. This trace is long enough to require word wrapping to test the functionality."
            general_comments = f"General comments for {name}. This general comment is intended to be long to ensure that word wrapping is tested thoroughly in the label."
            self.view.update_card(name, description, code_comments, trace, general_comments)

    def handle_search(self, query):
        """
        Handles the search input to filter the system-level tree items.

        Args:
            query (str): The search query to filter items.
        """
        query = query.lower()
        for item in self.system_level_items:
            item.setHidden(query not in item.text(0).lower())
        
        # Hide the special item during search
        self.view.special_item.setHidden(query != "")

    def add_requirement(self):
        """
        Adds a new requirement based on the current selection.
        """
        if not hasattr(self, 'selected_item') or not self.selected_item:
            # Add a new system requirement
            self.add_system_requirement()
        else:
            parent_text = self.selected_item.text(0)

            if parent_text.startswith("System Requirement"):
                # Add a new high-level requirement
                num_children = self.selected_item.childCount() + 1
                new_high_level_req = f"High Level Requirement {parent_text} R{num_children}"
                new_item = QTreeWidgetItem([new_high_level_req])
                self.selected_item.addChild(new_item)
            elif parent_text.startswith("High Level Requirement"):
                # Add a new low-level requirement
                num_children = self.selected_item.childCount() + 1
                new_low_level_req = f"Low Level Requirement {parent_text} R{num_children}"
                new_item = QTreeWidgetItem([new_low_level_req])
                self.selected_item.addChild(new_item)
            else:
                QMessageBox.warning(self.view, "Invalid Selection", "Please select a valid requirement level.")

    def add_system_requirement(self):
        """
        Adds a new system requirement.
        """
        num_system_items = len(self.system_level_items) + 1
        new_system_req = f"System Requirement R{str(num_system_items).zfill(6)}"
        new_item = QTreeWidgetItem([new_system_req])
        self.view.treeWidget.insertTopLevelItem(self.view.treeWidget.topLevelItemCount() - 1, new_item)
        self.system_level_items.append(new_item)

    def sync_with_remote(self):
        """
        Handles syncing with remote.
        """
        pass  # Empty handler for now

    def load_from_local(self):
        """
        Handles loading from local.
        """
        pass  # Empty handler for now

    def handle_project_selection(self, item):
        """
        Handles the project selection from the project list.
        
        Args:
            item (QListWidgetItem): The selected item in the project list.
        """
        project_name = item.text()
        if project_name == "Create New Project":
            self.create_new_project()
        elif project_name in self.project_data:
            self.current_project = project_name
            self.populate_tree(self.project_data[project_name])

    def create_new_project(self):
        """
        Prompts the user to create a new project and adds it to the project list.
        """
        project_name, ok = QInputDialog.getText(self.view, "Create New Project", "Enter project name:")
        if ok and project_name:
            if project_name not in self.project_data:
                self.project_data[project_name] = self.generate_tree_data()
                new_item = QListWidgetItem(project_name)
                self.view.projectListWidget.insertItem(self.view.projectListWidget.count() - 1, new_item)
            else:
                QMessageBox.warning(self.view, "Duplicate Project", "A project with this name already exists.")

    def populate_project_list(self):
        """
        Populates the project list with project names.
        """
        project_names = list(self.project_data.keys())
        self.view.populate_project_list(project_names)

    def show_view(self):
        """
        Shows the main view of the application.
        """
        self.view.show()

    def run(self):
        """
        Runs the application.
        """
        self.show_view()
        sys.exit(self.app.exec())

if __name__ == '__main__':
    controller = Controller()
    controller.run()
