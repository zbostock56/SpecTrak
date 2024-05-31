from requirement import Requirement

class Project:
    def __init__(self, Requirements: list[Requirement], name: str) -> None:
        """The Project class is representative of each project which
           itself contains many "requirements", each represented as a
           Requirements object.

        Args:
            Requirement (list[Requirement]): Requirement objects related to a
                                             Project.
            name (str): name of the Project.
        """
        self.requirements = Requirements
        self.name = name

    def _set_name(self, name: str) -> None:
        """Sets the Project object name.

        Args:
            name (str): Name of the project.
        """
        self.name = name

    def _get_name(self) -> str:
        """Gets the name of the Project

        Returns:
            str: Project name string
        """
        return self.name

    def _append_requirement(self, req: Requirement) -> None:
        """Adds a requirement to the end of the Requirements object list.

        Args:
            req (Requirement): Requirements to add.
        """
        self.requirements.append(req)

    def _remove_requirement(self, idx: int) -> bool:
        """Removes a requirement specified.

        Args:
            idx (int): index of requirement to remove.

        Returns:
            bool: If the requirement at that index existed or not.
        """
        try:
            self.requirements.pop(idx)
            return True
        except:
            return False

    def _remove_requirement(self, title: str) -> bool:
        """Removes a requirement based on name

        Args:
            title (str): Name of requirement object to be removed.

        Returns:
            bool: If the requirement with specified name was found or not.
        """
        for requirement in self.requirements:
            if title == requirement.title:
                self.requirements.remove(requirement)
                return True
        return False

    def _pop_end_requirement(self) -> bool:
        """Pops the end requirement off the list.

        Returns:
            bool: If the requirements list had anything in it.
        """
        try:
            self.requirements.pop(-1)
            return True
        except:
            return False