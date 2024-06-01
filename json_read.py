import json
import datetime

from hl import HighLevel
from ll import LowLevel
from requirement import Requirement
from system_req import SystemRequirement
from settings import Settings
from project import Project

# Definitions
FILE_HANDLE = 0
HANDLE_STATUS = 1

class JsonReader:
    def __init__(self, file_handle) -> None:
        """Creates a new instance of the JsonReader class which is used to extract
           json data from the json requirements file.

        Args:
            file_handle (io): File handle of the file to search.
        """
        # Set to dirty initially to denote that the json has not been read
        self.file_handle = (file_handle, False)
        self.read_json = None
        self.settings = None
        self.timestamp = None

    ############
    #   Setters
    ############
    def _set_file_handle(self, handle) -> None:
        """Sets the file handle and sets the status to dirty.

        Args:
            handle (io): File handle to set to.
        """
        self.file_handle = (handle, False)

    ############
    #   Getters
    ############
    def _get_settings(self) -> Settings:
        """Gets the Settings object stored in the class

        Returns:
            Settings : Stored Settings object
        """
        return self.settings

    def _get_file_handle(self):
        """Gets the file handle from the tuple in the object.

        Returns:
            io: file handle
        """
        return self.file_handle[FILE_HANDLE]

    ############
    #   Helpers
    ############
    def _check_handle_status(self) -> bool:
        """Checks to make sure the handle is valid.

        Returns:
            bool: True is the handle is valid, false otherwise.
        """
        if self._get_file_handle() is not None:
            if self.file_handle[HANDLE_STATUS] is False:
                self.read_json = json.loads(
                    self.file_handle[FILE_HANDLE].read()
                    )
                self.file_handle = (self.file_handle[FILE_HANDLE], True)
                # Update the status to show that the new handle
                # has been read
                return True
        print(f"ERR: Trying to read a file descriptor which is None!")
        # Unrecoverable error if handle is bad
        return False


    def _read_timestamp(self) -> float:
        """Reads the json file specified for the timestamp data.

        Returns:
            float: timestamp in seconds as a float.
        """
        if self._check_handle_status() is True:
            data = self.read_json
            self.timestamp = data["timestamp"]
            return self.timestamp
        else:
            return None

    def _compare_timestamp(self) -> bool:
        """Compares the current time with the timestamp in the file from the
           object.

        Returns:
            bool: If the timestamp of the object's file is earlier, return true;
                  otherwise, false.
        """
        if self.timestamp is None:
            self.timestamp = self._read_timestamp
        if self.timestamp < datetime.datetime.now().timestamp():
            return True
        else:
            return False

    def _read_json(self) -> list[Project]:
        """Returns all the projects in the json file.

        Returns:
            list[Project]: Project objects in the json file.
        """
        projects = []
        if self._check_handle_status() is True:
            data = self.read_json
            for i in range(len(data["projects"])):
                reqs = data["projects"][i]
                requirements = []
                for i in range(len(reqs["requirements"])):
                    # Create a Requirement object and add to list
                    requirements.append(
                        self._create_requirement(reqs["requirements"][i])
                    )
                projects.append(Project(
                    requirements, reqs["title"], reqs["description"]
                ))
            return projects
        else:
            return None


    def _read_project(self, project_name: str) -> Project:
        """Looks for specific projects.

        Args:
            project_name (str): Name of the project whose Requirements are
                                desired.

        Returns:
            Project: Project from the json, None if no file handle, or None if
                     project was not found.
        """
        requirements = []
        if self._check_handle_status() is True:
            projs = self.read_json["projects"]
            reqs = None
            for i in range(len(projs)):
                if projs[i]["title"] == project_name:
                    reqs = projs[i]

            # If Project object is not found, return None
            if reqs is None:
                return None

            # Get all the requirements and children of those requirements from
            # the project.
            for i in range(len(reqs["requirements"])):
                # Create a Requirement object and add to list
                requirements.append(
                    self._create_requirement(reqs["requirements"][i])
                )
            return Project(
                requirements, reqs["title"], reqs["description"]
            )
        else:
            return None

    def _read_settings(self) -> None:
        """Reads the settings data from the json.
        """
        if self._check_handle_status() is True:
            self.settings = self._create_settings(self.read_json["settings"])
        else:
            self.settings = None

    def _create_requirement(self, req_req) -> Requirement:
        """Creates a Requirement object from an input json object

        Args:
            req_req (str): json object

        Returns:
            Requirement: Returned Requirement object from json data
        """
        system_reqs = []
        for i in range(len(req_req["system_requirements"])):
            system_reqs.append(
                self._create_system_requirement(req_req["system_requirements"][i])
            )
        return Requirement(system_reqs, req_req["title"], req_req["description"],
                           req_req["status"])

    def _create_system_requirement(self, sys_req) -> SystemRequirement:
        """Creates a SystemRequirement object from an input json object

        Args:
            sys_req (str): json object

        Returns:
            SystemRequirement: Returned SystemRequirement object from json data
        """
        high_level_reqs = []
        for i in range(len(sys_req["high_level_requirements"])):
            high_level_reqs.append(
                self._create_high_level_requirement(sys_req["high_level_requirements"][i])
            )
        return SystemRequirement(high_level_reqs, sys_req["title"],
                                sys_req["description"], sys_req["status"])

    def _create_high_level_requirement(self, hl) -> HighLevel:
        """Creates a HighLevel object from an input json object

        Args:
            hl (str): json object

        Returns:
            HighLevel: Returned HighLevel object from json data
        """
        low_level_reqs = []
        for i in range(len(hl["low_level_requirements"])):
            low_level_reqs.append(
                self._create_low_level_requirement(hl["low_level_requirements"][i])
            )
        return HighLevel(low_level_reqs, hl["title"], hl["description"],
                         hl["status"])

    def _create_low_level_requirement(self, ll) -> LowLevel:
        """Creates a LowLevel object from an input json object

        Args:
            ll (str): json object

        Returns:
            LowLevel: Returned LowLevel object from json object
        """
        return LowLevel(ll["title"], ll["code_comments"], ll["description"],
                        ll["status"], ll["comments"], ll["trace"])

    def _create_settings(self, s) -> Settings:
        """Creates a Settings object from an input json object

        Args:
            s (str): json object

        Returns:
            Settings: Returned Settings object from json object
        """
        return Settings(s["color_theme"], s["organization_name"],
                        s["software_version"], s["support"], s["remote_url"])