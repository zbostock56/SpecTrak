from hl import HighLevel

class SystemRequirement:
    def __init__(
        self, HighLevel: list[HighLevel], title='Unnamed',
        description='No description', status='Not Started') -> None:
        """Creates an instance of the SystemRequirement class. This class is in
           the chain of the requirements specifying complex, architectural
           requirements for a project.

        Args:
            HighLevel (HighLevel): Denotes all the high level requirements which
                                   are children of this system requirement.
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
        self.HighLevel = HighLevel

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

    def _set_high_levels(self, high_level: list[HighLevel]) -> bool:
        """Sets the children HighLevel requirement objects.

        Args:
            high_level (HighLevel): HighLevel objects to set as children

        Returns:
            bool: Checks to make sure the HighLevel objects are not empty
        """
        if high_level is not None:
            self.HighLevel = high_level
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

    def _get_high_levels(self) -> list[HighLevel]:
        """Gets all the HighLevel requirement objects associated with the
           SystemRequirement object

        Returns:
            dict[HighLevel]: Dictionary of all the HighLevel requirement
                             objects.
        """
        return self.HighLevel