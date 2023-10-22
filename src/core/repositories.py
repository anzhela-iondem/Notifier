import abc

from src.core.entities import EnvItemEntity


class BaseRepository(abc.ABC):

    @abc.abstractmethod
    def get_one(self, key: str) -> EnvItemEntity:
        """
        Get the key and return the key value pare of the environmental variable.
        """
