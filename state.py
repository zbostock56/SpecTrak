from project import Project
from settings import Settings

class State:
    def __init__(
        self, projects: list[Project], username: str,
        settings: Settings) -> None:
        """The State class represents the program state and houses all Projects
           and what user is logged in.

        Args:
            projects (list[Project]): Projects that are currently loaded in the
                                      program.
            username (str): User who is logged in.
            settings (settings): Settings of the program
        """
        self.projects = projects
        self.username = username
        self.settings = settings

    ############
    #   Setters
    ############
    def _set_settings(self, settings: Settings) -> None:
        """Sets the settings of the program state.

        Args:
            settings (Settings): Object of settings to set to program state.
        """
        self.settings = settings

    def _set_username(self, username: str) -> None:
        """Sets the username of the user logged in.

        Args:
            username (str): Username to set as logged in.
        """
        self.username = username

    def _set_projects(self, projects: list[Project]) -> None:
        """Sets the projects list which is currently loaded into the program.

        Args:
            projects (list[Project]): List of projects to set to program state.
        """
        self.projects = projects

    ############
    #   Getters
    ############
    def _get_settings(self) -> Settings:
        """Gets the settings object that is currently loaded to program state.

        Returns:
            Settings: Settings object.
        """
        return self.settings

    def _get_username(self) -> str:
        """Gets the username of the user who is currently logged in.

        Returns:
            str: username.
        """
        return self.username

    def _get_projects(self) -> list[Project]:
        """Gets the currently set projects for the program state.

        Returns:
            list[Project]: List of the projects loaded to program state.
        """
        return self.projects

    ############
    #   Helpers
    ############
    def _append_project(self, project: Project) -> None:
        """Append a Project object to the program state.

        Args:
            project (Project): Project object to append.
        """
        self.projects.append(project)

    def _remove_project(self, name: str) -> bool:
        """Removes a project in the program.

        Args:
            name (str): Name of the project to remove.

        Returns:
            bool: If the project was found or not.
        """
        for project in self.projects:
            if project.name == name:
                self.projects.remove(project)
                return True
        return False
