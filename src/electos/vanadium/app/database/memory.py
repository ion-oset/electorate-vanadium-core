from typing import Any, Dict, List, Set, Tuple

from vanadium.model import ExternalIdentifier
from vanadium.utils import UniqueIds


class MemoryDataStore:

    """Very simple in-memory data storage.

    Keys are UUIDs either generated by the caller or generated from timestamps.
    Values are Python dictionaries or strings.

    In general the store does not throw exceptions as part of its own interface.
    It relies on return values and leaves it to the caller to generate exceptions
    as appropriate.
    Exceptions may still be thrown if there are internal errors.

    This store is for testing the API. Correctness matters, performance is deferred.
    """

    def __init__(self):
        # Entity lookup keyed by object ID
        self.by_id: Dict[str, Any] = {}
        # Entity lookup by model type
        self.by_type: Dict[str, Set[Any]] = {}


    def lookup(self, key):
        """Get the value associated with a key if present.

        Returns:
            Value in the store. If not found return None.
        """
        return self.by_id.get(key, None)


    def insert(self, key, value):
        """Associate a key with a value in the store if not present.

        If the value is already present do not modify it.
        If the key is None, generate one from a UUID.

        Returns:
            The key the value can be found under.
            If the value is already present for that key, return None.
        """
        if key is None:
            key = UniqueIds.timestamp_id()
        if key in self.by_id:
            return None
        self.by_id[key] = value
        # self.by_type.setdefault(type(value).__name__, set()).add(value)
        return key


    def update(self, key, value):
        """Update the value associated with a key if present.

        Returns:
            The value used to update or None if the key is not present.
            A key of None is the same as the key not being present.
        """
        if key is None:
            return None
        if key in self.by_id:
            self.by_id[key] = value
        else:
            value = None
        return value


    def upsert(self, key, value):
        """Update the value associated with key, if present, insert it if not.

        Returns:
            The key the value can be found under.
        """
        if key is None:
            key = UniqueIds.timestamp_id()
        self.by_id[key] = value
        # self.by_type.setdefault(type(value).__name__, set()).add(value)
        return key


    def remove(self, key):
        """Delete the value associated with a key if present.

        Returns:
            The value associated with the key, if it was removed, None otherwise.
        """
        value = self.by_id.pop(key, None)
        return value


    def keys(self) -> Set[Any]:
        """Set of all keys in the store."""
        return set(self.by_id.keys())


    def values(self) -> List[Any]:
        """List of all values in the store."""
        return list(self.by_id.values())
