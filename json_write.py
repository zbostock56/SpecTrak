import json
from state import State
from ll import LowLevel
from hl import HighLevel
from requirement import Requirement
from system_req import SystemRequirement
from settings import Settings
from project import Project

class JsonWriter:
    def __init__(
        self, state: State, file_path: str) -> None:
        """Creates a new instance or the JsonWriter class which is used to
           output the program state to a json file.

        Args:
            state (State): state of the program when writing to json.
            file_path (str): file path of where to write to.
        """
        self.file_path = file_path
        self.state = state

    def _write_json(self) -> None:
        with open(self.file_path, "w") as output_file:
            self._write_settings(output_file)

    def _write_settings(self, output_file) -> None:
        dictionary = {
            "settings" : {
                "color_theme" : self.state.settings.color_theme,
                "organization_name" : self.state.settings.org_name,
                "software_version" : self.state.settings.sw_version,
                "support" : self.state.settings.support,
                "remote_url" : self.state.settings.remote_url
            }
        }
        for i in range(len(self.state.projects)):
            dictionary[
                self.state.projects[i].title
                ] = self._dictionary_project(self.state.projects[i])
        json.dump(dictionary, output_file, indent=2)

    def _dictionary_project(self, project: Project):
        requires = []
        for i in range(len(project.requirements)):
            requires.append(self._dictionary_requirement(
                project.requirements[i]
            ))
        return {
            "title" : project.title,
            "description" : project.description,
            "requirements" : requires
        }

    def _dictionary_requirement(self, req: Requirement):
        sys_requirements = []
        for i in range(len(req.SystemRequirement)):
            sys_requirements.append(self._dictionary_sys_requirement(
                req.SystemRequirement[i]
            ))
        return {
            "title" : req.title,
            "description" : req.description,
            "status" : req.status,
            "system_requirements" : sys_requirements
        }

    def _dictionary_sys_requirement(self, sys_req: SystemRequirement):
        high_levels = []
        for i in range(len(sys_req.HighLevel)):
            high_levels.append(self._dictionary_high_level(
                sys_req.HighLevel[i]
            ))
        return {
            "title" : sys_req.title,
            "description" : sys_req.description,
            "status" : sys_req.status,
            "high_level_requirements" : high_levels
        }

    def _dictionary_high_level(self, high_level: HighLevel):
        low_levels = []
        for i in range(len(high_level.LowLevel)):
            low_levels.append(self._dictionary_low_level(
                high_level.LowLevel[i]
            ))
        return {
            "title" : high_level.title,
            "description" : high_level.description,
            "status" : high_level.status,
            "low_level_requirements" : low_levels
        }

    def _dictionary_low_level(self, low_level: LowLevel):
        return {
            "title" : low_level.title,
            "description" : low_level.description,
            "status" : low_level.status,
            "comments" : low_level.comment,
            "trace" : low_level.trace,
            "code_comments" : low_level.code_reference
        }