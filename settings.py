from exception import SpecTrakException

class Settings:
    def __init__(
        self, color_theme: str,
        org_name: str, sw_version: str,
        support: str, remote_url: str) -> None:
        self.color_theme = color_theme
        self.org_name = org_name
        self.sw_version = sw_version
        self.support = support
        self.remote_url = remote_url

    ############
    #   Setters
    ############
    def _set_color_theme(self, color_theme: str) -> bool:
        """Sets the color theme of the program.

        Args:
            color_theme (str): Chooses from existing themes.

        Returns:
            bool: Lets the programmer know if a valid theme was chosen.
        """
        color_options = set({
            'Black', 'White', 'Default'
        })

        if color_theme not in color_options:
            return False
        else:
            self.color_theme = color_theme
            # TODO: update colors
            return True

    def _set_org_name(self, org_name: str) -> None:
        """Set the organization name.

        Args:
            org_name (str): The organization name to set to.
        """
        self.org_name = org_name

    def _set_remote_url(self, remote_url: str) -> None:
        """Sets the remote url.

        Args:
            remote_url (str): Remote url to set to.
        """
        self.remote_url = remote_url

    def _set_support(self, support: str) -> None:
        """Sets the support line.

        Args:
            support (str): support line to set to.
        """
        self.support = support

    ############
    #   Getters
    ############
    def _get_color_theme(self) -> str:
        """Gets the color theme.

        Returns:
            str: Color theme as a string.
        """
        return self.color_theme

    def _get_org_name(self) -> str:
        """Gets the organization name.

        Returns:
            str: Organization name to set to.
        """
        if self.org_name == "":
            return "SpecTrak"
        else:
            return self.org_name

    def _get_sw_version(self) -> str:
        """Gets the current software version

        Returns:
            str: Software version string
        """
        if self.sw_version == "":
            return "Unknown Version"
        else:
            return self.sw_version

    def _get_support(self) -> str:
        """Gets the support line

        Returns:
            str: support line string.
        """
        if self.support == "":
            return "No Support Available"
        else:
            return self.support

    def _get_remote_url(self) -> str:
        """Gets the remote URL

        Raises:
            SpecTrakException: If the remote URL is not set and it is attempted
                               to be used, something is very wrong.

        Returns:
            str: the URL
        """
        if self.remote_url == "":
            # We assume that if a user is trying to create use a remote when
            # there isn't one, something has gone very wrong
            # TODO: create non-stopping error message
            raise SpecTrakException("No Remote URL Specified")
        else:
            return self.remote_url