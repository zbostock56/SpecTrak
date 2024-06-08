import hashlib
import json
from dictionify import dictionify

def checksum(obj) -> str:
    """Generate a checksum for a given object.

    Args:
        obj: The object to generate a checksum for.
    Return:
        The checksum as a hexadecimal string.
    """
    return hashlib.md5(
                json.dumps(dictionify(obj), sort_keys=True).encode('utf-8')
            ).hexdigest()

def hash_list(lst):
    """Recursively converts lists to tuples for hashing.
    """
    if isinstance(lst, list):
        return tuple(hash_list(sub) for sub in lst)
    return lst