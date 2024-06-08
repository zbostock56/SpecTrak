import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMessageBox, QInputDialog, QTreeWidgetItem, QListWidgetItem
from model import Model
from view import View
from login_view import LoginView

class Controller:
    SETTINGS_FILE = 'spectraksettings.json'

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = Model()

        self.view = None  # This will be set after successful login or loading settings

        # Check for the presence of the settings file
        if self.settings_exist():
            print("Settings file found. Loading settings.")
            self.load_settings()
            print(f"Loaded settings: username={self.username}, remote_path={self.remote_path}, is_password={self.is_password}, is_key={self.is_key}")
            self.show_main_view()
        else:
            print("Settings file not found. Showing login view.")
            self.login_view = LoginView()
            self.login_view.connectButton.clicked.connect(self.handle_login)
            self.login_view.show()

    def settings_exist(self):
        return os.path.exists(self.SETTINGS_FILE)

    def load_settings(self):
        try:
            with open(self.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)
                self.username = settings.get('username')
                self.password_or_key = settings.get('password_or_key')
                self.remote_path = settings.get('remote_path')
                self.is_password = settings.get('is_password')
                self.is_key = settings.get('is_key')
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.username = None
            self.password_or_key = None
            self.remote_path = None
            self.is_password = None
            self.is_key = None

    def save_settings(self):
        settings = {
            'username': self.username,
            'password_or_key': self.password_or_key,
            'remote_path': self.remote_path,
            'is_password': self.is_password,
            'is_key': self.is_key
        }
        try:
            with open(self.SETTINGS_FILE, 'w') as file:
                json.dump(settings, file)
            print("Settings saved successfully.")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def handle_login(self):
        self.username = self.login_view.usernameInput.text()
        self.password_or_key = self.login_view.passwordInput.text()
        self.remote_path = self.login_view.remotePathInput.text()
        self.is_password = self.login_view.radioPassword.isChecked()
        self.is_key = self.login_view.radioKey.isChecked()

        if self.validate_login(self.username, self.password_or_key, self.remote_path, self.is_password, self.is_key):
            self.save_settings()
            self.show_main_view()
        else:
            QMessageBox.warning(self.login_view, "Login Failed", "Invalid username, password/key, or remote path.")

    def validate_login(self, username, password_or_key, remote_path, is_password, is_key):
        # Perform actual validation here (e.g., checking credentials)
        if not is_password and not is_key:
            return False
        return True

    def show_main_view(self):
        print("Showing main view.")
        if hasattr(self, 'login_view'):
            self.login_view.close()
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
        
        self.view.show()  # Ensure the main view is shown
        print("Main view should be visible now.")

    def generate_tree_data(self):
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
        project_data = {
            "Project A": self.generate_tree_data(),
            "Project B": self.generate_tree_data(),
            "Project C": self.generate_tree_data(),
        }
        return project_data

    def populate_tree(self, tree_data=None):
        if tree_data is None:
            tree_data = self.tree_data
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
        for child in children:
            if isinstance(child, dict):
                child_item = QTreeWidgetItem([child["name"]])
                parent_item.addChild(child_item)
                self.add_child_items(child_item, child["children"])
            else:
                child_item = QTreeWidgetItem([child])
                parent_item.addChild(child_item)

    def handle_item_click(self, item, column):
        self.selected_item = item

        if item == self.view.special_item:
            self.add_system_requirement()
        else:
            name = item.text(0)
            description = f"Description for {name}. This is a detailed description that should wrap around to test the word wrapping functionality in the label."
            code_comments = f"Code comments for {name}. This is a sample code comment that is also quite long to test word wrapping."
            trace = f"Trace for {name}. This trace is long enough to require word wrapping to test the functionality."
            general_comments = f"General comments for {name}. This general comment is intended to be long to ensure that word wrapping is tested thoroughly in the label."
            self.view.update_card(name, description, code_comments, trace, general_comments)

    def handle_search(self, query):
        query = query.lower()
        for item in self.system_level_items:
            item.setHidden(query not in item.text(0).lower())
        
        self.view.special_item.setHidden(query != "")

    def add_requirement(self):
        if not hasattr(self, 'selected_item') or not self.selected_item:
            self.add_system_requirement()
        else:
            parent_text = self.selected_item.text(0)

            if parent_text.startswith("System Requirement"):
                num_children = self.selected_item.childCount() + 1
                new_high_level_req = f"High Level Requirement {parent_text} R{num_children}"
                new_item = QTreeWidgetItem([new_high_level_req])
                self.selected_item.addChild(new_item)
            elif parent_text.startswith("High Level Requirement"):
                num_children = self.selected_item.childCount() + 1
                new_low_level_req = f"Low Level Requirement {parent_text} R{num_children}"
                new_item = QTreeWidgetItem([new_low_level_req])
                self.selected_item.addChild(new_item)
            else:
                QMessageBox.warning(self.view, "Invalid Selection", "Please select a valid requirement level.")

    def add_system_requirement(self):
        num_system_items = len(self.system_level_items) + 1
        new_system_req = f"System Requirement R{str(num_system_items).zfill(6)}"
        new_item = QTreeWidgetItem([new_system_req])
        self.view.treeWidget.insertTopLevelItem(self.view.treeWidget.topLevelItemCount() - 1, new_item)
        self.system_level_items.append(new_item)

    def sync_with_remote(self):
        pass  # Empty handler for now

    def load_from_local(self):
        pass  # Empty handler for now

    def handle_project_selection(self, item):
        project_name = item.text()
        if project_name == "Create New Project":
            self.create_new_project()
        elif project_name in self.project_data:
            self.current_project = project_name
            self.populate_tree(self.project_data[project_name])

    def create_new_project(self):
        project_name, ok = QInputDialog.getText(self.view, "Create New Project", "Enter project name:")
        if ok and project_name:
            if project_name not in self.project_data:
                self.project_data[project_name] = self.generate_tree_data()
                new_item = QListWidgetItem(project_name)
                self.view.projectListWidget.insertItem(self.view.projectListWidget.count() - 1, new_item)
            else:
                QMessageBox.warning(self.view, "Duplicate Project", "A project with this name already exists.")

    def populate_project_list(self):
        project_names = list(self.project_data.keys())
        self.view.populate_project_list(project_names)

    def show_view(self):
        self.view.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == '__main__':
    controller = Controller()
    controller.run()
