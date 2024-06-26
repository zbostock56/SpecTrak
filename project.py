from requirement import Requirement
from checksum import checksum, hash_list

class Project:
    def __init__(
        self, Requirements: list[Requirement], title="Unnamed",
        description="No description") -> None:
        """The Project class is representative of each project which
           itself contains many "requirements", each represented as a
           Requirements object.

        Args:
            Requirement (list[Requirement]): Requirement objects related to a
                                             Project.
            name (str): name of the Project.
        """
        self.requirements = Requirements
        self.title = title
        self.description = description

    ############
    #   Setters
    ############
    def _set_title(self, title: str) -> None:
        """Sets the Project object name.

        Args:
            title (str): title of the project.
        """
        self.title = title

    def _set_description(self, desc: str) -> None:
        """Sets the description of the of the project.

        Args:
            desc (str): description to set to.
        """
        self.description = desc

    ############
    #   Getters
    ############
    def _get_title(self) -> str:
        """Gets the title of the Project

        Returns:
            str: Project title string
        """
        return self.title

    def _get_description(self) -> str:
        """Gets the description from the project.

        Returns:
            str: Description from the project.
        """
        return self.description

    ############
    #   Helpers
    ############
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

    def __eq__(self, other) -> bool:
        """Compares between two HighLevel objects.

        Args:
            other (unknown): Other object to compare to.

        Returns:
            bool: If the objects are the same or not.
        """
        if isinstance(other, Project):
            ret = self.description == other.description
            ret = ret and (self.title == other.title)
            # Save time if the other values are already different
            if ret is False:
                return False
            other_reqs = set()
            for req in other.requirements:
                other_reqs.add(checksum(req))
            for req in self.requirements:
                if checksum(req) not in other_reqs:
                    return False
            return True
        else:
            return False

    def __hash__(self) -> hash:
        """Returns a hash of the object.

        Returns:
            hash: hash of the object.
        """
        return hash(
            (self.description, self.title, hash_list(self.requirements)))