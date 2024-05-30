import json

from hl import HighLevel
from ll import LowLevel
from requirement import Requirement
from system_req import SystemRequirement
from settings import Settings

#
#   TODO: Add try catches to make sure that, if the data is not there, no crashes.
#

class JsonRead:
    def __init__(self, file_path: str) -> None:
        """Creates a new instance of the JsonRead class which is used to extract
           json data from the json requirements file.

        Args:
            file_path (str): Specifies the location of the file to search
        """
        # TODO: Update for remote file
        self.file_path = file_path
        self.read_json = None
        self.settings = None

    def _read_json(self) -> list[Requirement]:
        """Highest level reading method.

        Returns:
            list[Requirement]: All the Requirements objects in the json file
        """
        requirements = []
        with open(self.file_path, "r") as input_file:
            data = json.loads(input_file.read())
            reqs = data["root"]
            for i in range(len(reqs)):
                # Create a Requirement object and add to list
                requirements.append(self._create_requirement(reqs[i]))
            self.settings = self._create_settings(data["settings"])
        return requirements

    def _create_requirement(self, req_req) -> Requirement:
        """Creates a Requirement object from an input json object

        Args:
            req_req (str): json object

        Returns:
            Requirement: Returned Requirement object from json data
        """
        system_reqs = []
        obj = req_req["requirements"]
        for i in range(len(obj["system_requirements"])):
            system_reqs.append(
                self._create_system_requirement(obj["system_requirements"][i])
            )
        return Requirement(system_reqs, obj["title"], obj["description"],
                           obj["status"])

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

    def _get_settings(self) -> Settings:
        """Gets the Settings object stored in the class

        Returns:
            Settings : Stored Settings object
        """
        return self.settings
