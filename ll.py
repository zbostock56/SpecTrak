class LowLevel:
    def __init__(
        self, title='Unnamed', code_reference='None',
        description='No description', status='Not Started',
        comment='No Comment', trace='') -> None:
        """Creates an instance of the LowLevel class. This class is the lowest
           level requirement that can be specified. This requirement would
           be specifying in the narrowest scope possible what is needed to
           fulfill a sub-part of a full requirement.

        Args:
            title (str, optional): Denotes the title which will be shown on the
                                   UI. Defaults to 'Unnamed'.
            code_reference (str, optional): Denotes the place where the code
                                            can be found. This may be a URL
                                            to an external tool, the code itself
                                            or other information.
            description (str, optional): Denotes the description which will be
                                         shown on the UI. Defaults to 'No
                                         description'.
            status (str, optional): Describes the status of the requirement.
                                    Could be various things like 'Not Started',
                                    'In Progress', 'Under Review', 'Done', etc.
                                    Defaults to 'Not Started'.
            comment (str, optional): Allows the requirment to have comments
                                     on it.
            trace (str, optional): Meant for specifying function name of the
                                   module which solves the requirement
        """
        self.status = status
        self.description = description
        self.title = title
        self.code_reference = code_reference
        self.comment = comment
        self.trace = trace

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

    def _set_code_reference(self, code_reference: str) -> None:
        """Sets the code reference for the LowLevel object

        Args:
            code_reference (str): Reference to how the problem is being solved.
                                  Could be a variety of things including URL to
                                  external tool, the code itself, comments about
                                  the solution, etc.
        """
        self.code_reference = code_reference

    def _set_comment(self, comment: str) -> None:
        """Sets the comment of the LowLevel requirement

        Args:
            comment (str): Comments about the solution
        """
        self.comment = comment

    def _set_trace(self, trace: str) -> None:
        """Sets the trace of the LowLevel requirement

        Args:
            trace (str): Name of the function which solve the requirement
        """
        self.trace = trace

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

    def _get_code_reference(self) -> str:
        """Gets the code reference

        Returns:
            str: Code Reference string
        """
        return self.code_reference

    def _get_comment(self) -> str:
        """Gets the comment

        Returns:
            str: Comment string
        """
        return self.comment

    def _get_trace(self) -> str:
        """Gets the trace

        Returns:
            str: Trace string
        """
        return self.trace