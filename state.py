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
