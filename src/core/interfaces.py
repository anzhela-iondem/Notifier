import abc

from src.core.entities import EventEntity


class BaseMessengerServiceProvider(abc.ABC):

    @abc.abstractmethod
    def send_message(self, event_entity: EventEntity) -> None:
        """Abstract method is implemented in the inherited class."""


class BaseEmailServiceProvider(abc.ABC):

    @abc.abstractmethod
    def send_email(self, event_entity: EventEntity) -> None:
        """
        Abstract method is implemented in the inherited class.
        """


class BaseLoggerProvider(abc.ABC):

    @abc.abstractmethod
    def info(self, message: str) -> None:
        """ Is implemented in the infrastructure layer."""

    @abc.abstractmethod
    def warning(self, message: str) -> None:
        """ Is implemented in the infrastructure layer."""

    @abc.abstractmethod
    def error(self, message: str) -> None:
        """ Is implemented in the infrastructure layer."""

    @abc.abstractmethod
    def critical(self, message: str) -> None:
        """ Is implemented in the infrastructure layer."""
