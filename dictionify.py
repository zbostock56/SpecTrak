def dictionify(obj) -> dict:
    from project import Project
    from requirement import Requirement
    from hl import HighLevel
    from ll import LowLevel
    """Helper to call the dictionary creation functions.

    Returns:
        dict: dictionary of the passed in object.
    """
    if isinstance(obj, Project):
        return dictionary_project(obj)
    elif isinstance(obj, Requirement):
        return dictionary_requirement(obj)
    elif isinstance(obj, HighLevel):
        return dictionary_high_level(obj)
    elif isinstance(obj, LowLevel):
        return dictionary_low_level(obj)

def dictionary_project(project) -> dict:
        """Creates a dictionary of a project object.

        Args:
            project (Project): Project object to make into dictionary.

        Returns:
            dict: dictionary of the project object.
        """
        requires = []
        for i in range(len(project.requirements)):
            requires.append(dictionary_requirement(
                project.requirements[i]
            ))
        return {
            "title" : project.title,
            "description" : project.description,
            "requirements" : requires
        }

def dictionary_requirement(req) -> dict:
    """Creates a dictionary of a Requirement object.

    Args:
        req (Requirement): Requirement object to create into a dictionary.

    Returns:
        dict: dictionary of the Requirement object.
    """
    sys_requirements = []
    for i in range(len(req.SystemRequirement)):
        sys_requirements.append(dictionary_sys_requirement(
            req.SystemRequirement[i]
        ))
    return {
        "title" : req.title,
        "description" : req.description,
        "status" : req.status,
        "system_requirements" : sys_requirements
    }

def dictionary_sys_requirement(sys_req) -> dict:
    """Creates a dictionary of the passed in SystemRequirement.

    Args:
        sys_req (SystemRequirement): SystemRequirement to make into dict.

    Returns:
        dict: dictionary of the SystemRequirement object.
    """
    high_levels = []
    for i in range(len(sys_req.HighLevel)):
        high_levels.append(dictionary_high_level(
            sys_req.HighLevel[i]
        ))
    return {
        "title" : sys_req.title,
        "description" : sys_req.description,
        "status" : sys_req.status,
        "high_level_requirements" : high_levels
    }

def dictionary_high_level(high_level) -> dict:
    """Creates a dictionary of a HighLevel object.

    Args:
        high_level (HighLevel): HighLevel object to create into dict.

    Returns:
        dict: dictionary of the HighLevel object.
    """
    low_levels = []
    for i in range(len(high_level.LowLevel)):
        low_levels.append(dictionary_low_level(
            high_level.LowLevel[i]
        ))
    return {
        "title" : high_level.title,
        "description" : high_level.description,
        "status" : high_level.status,
        "low_level_requirements" : low_levels
    }

def dictionary_low_level(low_level) -> dict:
    """Creates a dictionary of a LowLevel object.

    Args:
        low_level (LowLevel): LowLevel object to make into dict.

    Returns:
        dict: dictionary of the LowLevel object.
    """
    return {
        "title" : low_level.title,
        "description" : low_level.description,
        "status" : low_level.status,
        "comments" : low_level.comment,
        "trace" : low_level.trace,
        "code_comments" : low_level.code_reference
    }