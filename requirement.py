from system_req import SystemRequirement
from checksum import checksum, hash_list

class Requirement:
    def __init__(
        self, SystemRequirement: list[SystemRequirement], title='Unnamed',
        description='No description', status='Not Started') -> None:
        """Creates an instance of the Requirement class. This class is the main
           area where requirments are stored and is the top of the hierarchy.

        Args:
            SystemRequirement (SystemRequirement): Denotes all the system
                                                   requirements which are
                                                   children of this requirement.
            title (str, optional): Denotes the title which will be shown on the
                                   UI. Defaults to 'Unnamed'.
            description (str, optional): Denotes the description which will be
                                         shown on the UI. Defaults to 'No
                                         description'.
            status (str, optional): Describes the status of the requirement.
                                    Could be various things like 'Not Started',
                                    'In Progress', 'Under Review', 'Done', etc.
                                    Defaults to 'Not Started'.
        """
        self.status = status
        self.description = description
        self.title = title
        self.SystemRequirement = SystemRequirement

    ############
    #   Setters
    ############
    def _set_title(self, title: str) -> None:
        """Sets the title of a requirement.

        Args:
            title (str): Denotes the title of the requirement
        """
        self.title = title

    def _set_description(self, description: str) -> None:
        """Sets the description of a requirement.

        Args:
            description (str): Denotes the description of the requirement
        """
        self.description = description

    def _set_status(self, status: str) -> bool:
        """Sets the status of a requirement.

        Args:
            status (str): denotes the status of the requirement

        Returns:
            bool: Informs if the passed status is in the valid status options
        """
        status_options = set({
            'In Progress', 'Not Started', 'Under Review', 'Done'
        })
        if status in status_options:
            self.status = status
            return True
        else:
            return False

    def _set_system_requirements(
        self, system_requirement: list[SystemRequirement]) -> bool:
        """Sets the children SystemRequirement objects.

        Args:
            system_requirement (SystemRequirement): SystemRequirement children
                                                    to this Requirement object.

        Returns:
            bool: Checks to ensure that the SystemRequirement is not empty.
        """
        if system_requirement is not None:
            self.SystemRequirement = system_requirement
            return True
        else:
            return False

    ############
    #   Getters
    ############
    def _get_title(self) -> str:
        """Gets the title

        Returns:
            str: Title string
        """
        return self.title

    def _get_description(self) -> str:
        """Gets the description

        Returns:
            str: Description string
        """
        return self.description

    def _get_status(self) -> str:
        """Gets the status

        Returns:
            str: Status string
        """
        return self.status

    def _get_system_requirements(self) -> list[SystemRequirement]:
        """Gets the children SystemRequirement objects.

        Returns:
            SystemRequirement: SystemRequirement object(s) related to the
                               Requirement object.
        """
        return self.SystemRequirement

    ############
    #   Helpers
    ############
    def _remove_system_requirement(self, title: str) -> bool:
        """Removes a system requirement object based on its title.

        Args:
            title (str): title of system requirement to remove.

        Returns:
            bool: If system requirement was found or not.
        """
        for sys_req in self.SystemRequirement:
            if sys_req.title == title:
                self.SystemRequirement.remove(sys_req)
                return True
        return False

    def __eq__(self, other) -> bool:
        """Checks if the object is equal to another.

        Args:
            other (unknown): object to compare against.

        Returns:
            bool: True if equal, false otherwise.
        """
        if isinstance(other, Requirement):
            ret = self.status == other.status
            ret = ret and (self.description == other.description)
            ret = ret and (self.title == other.description)
            # Try to save time and not do the list operation if not needed
            if ret is False:
                return False
            # Set to compare between the lists of objects
            other_sys_req = set()
            for sr in other.SystemRequirement:
                other_sys_req.add(checksum(sr))
            for sr in self.SystemRequirement:
                if checksum(sr) not in other_sys_req:
                    return False
            return True
        else:
            return False

    def __hash__(self) -> bool:
        """Creates a hash of the object.

        Returns:
            hash: hash of the object.
        """
        return hash((
            self.status, self.description, self.title,
            hash_list(self.SystemRequirement)
        ))