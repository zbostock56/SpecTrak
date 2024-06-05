import json
import datetime
from state import State
from dictionify import dictionify

class JsonWriter:
    def __init__(
        self, state: State, file_handle) -> None:
        """Creates a new instance or the JsonWriter class which is used to
           output the program state to a json file.

        Args:
            state (State): state of the program when writing to json.
            file_handle (io): handle of what to write to
        """
        self.file_handle = file_handle
        self.state = state

    ############
    #   Setters
    ############
    def _set_file_handle(self, handle) -> None:
        """Sets the file handle and sets the status to dirty.

        Args:
            handle (io): File handle to set to.
        """
        self.file_handle = handle

    ############
    #   Getters
    ############
    def _get_file_handle(self):
        """Gets the file handle from the tuple in the object.

        Returns:
            io: file handle
        """
        return self.file_handle

    ############
    #   Helpers
    ############
    def _check_handle_status(self) -> bool:
        """Checks to make sure the handle is valid.

        Returns:
            bool: True is the handle is valid, false otherwise.
        """
        if self.file_handle is not None:
            return True
        print(f"ERR: Trying to write to a file descriptor which is None!")
        # Unrecoverable error if handle is bad
        return False

    def _write_json(self) -> None:
        """Writes all the the projects to the json file.
        """
        self._write_program_state()

    def _write_program_state(self) -> None:
        """Writes the all the program state to the output file.
        """
        if self._check_handle_status() is True:
            dictionary = {}
            if self.state.settings is not None:
                    dictionary["settings"] = {
                        "color_theme" : self.state.settings.color_theme,
                        "organization_name" : self.state.settings.org_name,
                        "software_version" : self.state.settings.sw_version,
                        "support" : self.state.settings.support,
                        "remote_url" : self.state.settings.remote_url
                    }
            projects = []
            for i in range(len(self.state.projects)):
                projects.append(dictionify(
                    self.state.projects[i])
                )
            dictionary["projects"] = projects
            dictionary["timestamp"] = datetime.datetime.now().timestamp()
            json.dump(dictionary, self.file_handle, indent=2)
        else:
            pass