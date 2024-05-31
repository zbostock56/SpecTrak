import json
import datetime

from hl import HighLevel
from ll import LowLevel
from requirement import Requirement
from system_req import SystemRequirement
from settings import Settings
from project import Project

class JsonReader:
    def __init__(self, file_path: str, remote: str) -> None:
        """Creates a new instance of the JsonReader class which is used to extract
           json data from the json requirements file.

        Args:
            file_path (str): Specifies the location of the file to search.
            remote (str): Specifies the remote location to store the json
        """
        self.file_path = file_path
        self.read_json = None
        self.settings = None
        self.remote_file_path = remote
        self.timestamp = None

    ############
    #   Setters
    ############
    def _set_remote_file_path(self, remote: str) -> None:
        """Sets the remote file path for the writer.

        Args:
            remote (str): remote file path.
        """
        self.remote_file_path = remote

    ############
    #   Getters
    ############
    def _get_remote_file_path(self) -> str:
        """Gets the remote file path that is set in the writer.

        Returns:
            str: remote file path.
        """
        return self.remote_file_path

    def _get_settings(self) -> Settings:
        """Gets the Settings object stored in the class

        Returns:
            Settings : Stored Settings object
        """
        return self.settings

    ############
    #   Helpers
    ############
    def _read_timestamp(self) -> float:
        """Reads the json file specified for the timestamp data.

        Returns:
            float: timestamp in seconds as a float.
        """
        with open(self.file_path, "r") as input_file:
            data = json.loads(input_file.read())
            self.timestamp = data["timestamp"]
            return self.timestamp

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

    def _read_json(self, project_name: str) -> Project:
        """Highest level reading method. Looks for specific projects

        Args:
            project_name (str): Name of the project whose Requirements are
                                desired

        Returns:
            Project: Project from the json
        """
        requirements = []
        with open(self.file_path, "r") as input_file:
            data = json.loads(input_file.read())
            reqs = data[project_name]
            for i in range(len(reqs["requirements"])):
                # Create a Requirement object and add to list
                requirements.append(
                    self._create_requirement(reqs["requirements"][i])
                )
        return Project(
            requirements, reqs["title"], reqs["description"]
        )

    def _read_settings(self) -> None:
        """Reads the settings data from the json.
        """
        with open(self.file_path, "r") as input_file:
            data = json.loads(input_file.read())
            self.settings = self._create_settings(data["settings"])

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