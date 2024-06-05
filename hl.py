from ll import LowLevel
from checksum import checksum, hash_list

class HighLevel:
    def __init__(
        self, LowLevel: list[LowLevel], title='Unnamed',
        description='No description', status='Not Started') -> None:
        """Creates an instance of the HighLevel class. This class is in the
           in the chain of requirements, specifying high level concepts for a
           requirement, but are not necessarily speaking directly about
           feature/requirement specifics.

        Args:
            LowLevel (LowLevel): Denotes the LowLevel requirements which are
                                 children of this requirement
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
        self.LowLevel = LowLevel

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

    def _set_low_levels(self, low_level: list[LowLevel]) -> bool:
        """Sets the LowLevel objects

        Args:
            low_level (LowLevel): Denotes the LowLevel objects which are
                                  children of this HighLevel object.

        Returns:
            bool: Check to make sure the passed in value is not empty.
        """
        if low_level is not None:
            self.LowLevel = low_level
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

    def _get_low_levels(self) -> list[LowLevel]:
        """Returns the children LowLevel objects

        Returns:
            LowLevel: LowLevel object(s) related to this HighLevel object
        """
        return self.LowLevel

    ############
    #   Helpers
    ############
    def _remove_low_level_requirement(self, title: str) -> bool:
        """Removes a low level requirement based on name.

        Args:
            title (str): title of the low level requirement.

        Returns:
            bool: If the ll req was found or not.
        """
        for l in self.LowLevel:
            if l.title == title:
                self.LowLevel.remove(l)
                return True
        return False

    def __eq__(self, other) -> bool:
        """Compares between two HighLevel objects.

        Args:
            other (unknown): Other object to compare to.

        Returns:
            bool: If the objects are the same or not.
        """
        if isinstance(other, HighLevel):
            ret = other.description == self.description
            ret = ret and (other.status == self.status)
            ret = ret and (other.title == self.title)
            # Try to save time if the others already fail
            if ret is False:
                return False
            # Create a set of all the LowLevel objects in the other object
            other_low_level = set()
            for ll in other.LowLevel:
                other_low_level.add(checksum(ll))
            for ll in self.LowLevel:
                # If any don't exist in the other objects LowLevel objects,
                # return not equal.
                if checksum(ll) not in other_low_level:
                    return False
            # Since ret above must be True to hit the for loops, we return true
            return True
        else:
            return False

    def __hash__(self) -> hash:
        """Returns a hash of the object.

        Returns:
            hash: hash of the object.
        """
        return hash((self.description, self.title,
                     self.status, hash_list(self.LowLevel)))