import abc
from typing import Union

from src.core.entities import EventEntity
from src.core.interfaces import BaseMessengerServiceProvider, \
    BaseEmailServiceProvider


class BaseUseCase(abc.ABC):

    @abc.abstractmethod
    def execute(self):
        """Abstract method is implemented in its inherited class."""


class NotifierUseCase(BaseUseCase):

    def __init__(
            self,
            event_entity: EventEntity,
            service_provider: Union[
                BaseMessengerServiceProvider,
                BaseEmailServiceProvider
            ]
    ):
        self.event_entity = event_entity
        self.service_provider = service_provider

    def execute(self) -> None:
        """
        Check the service type of an instance and run corresponding
        data sending method.
        :return None:
        """
        if isinstance(self.service_provider, BaseMessengerServiceProvider):
            self.service_provider.send_message(
                event_entity=self.event_entity
            )
        if isinstance(self.service_provider, BaseEmailServiceProvider):
            self.service_provider.send_email(
                event_entity=self.event_entity
            )
