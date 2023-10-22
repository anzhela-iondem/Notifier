from src import config
from src.core.entities import EventEntity
import src.core.validators as validator
from src.core.exceptions import InvalidEventTypeException, \
    MessageBodyIsInvalidException, DeserializationFailedException, \
    SerializationFailedException, InvalidEmailException
from src.infrastructure.providers import LoggerServiceProvider


class EventSerializer:

    def __init__(self, logger_service_provider: LoggerServiceProvider):
        self.logger_service_provider = logger_service_provider

    def serialize(self, event_entity: EventEntity) -> dict[str, str]:
        """
        Based on the given EventEntity class data, check all data values and,
        return a dictionary type data.
        :param event_entity:
        :return dict:
        """
        event_type = event_entity.event_type
        body = event_entity.body
        to = event_entity.to
        try:
            validator.check_event_type(event_type)
            if event_type == config.APPROVED_PUBLICATION:
                validator.check_email_validation(to)
            validator.check_event_body(body)
            return {
                "event_type": event_type,
                "body": body,
                "to": to
            }
        except InvalidEventTypeException as err:
            self.logger_service_provider.error(f"Event Type is invalid: {err}")
            raise InvalidEventTypeException(err) from None
        except InvalidEmailException as err:
            self.logger_service_provider.error(f"Email is invalid: {err}")
            raise InvalidEmailException(err) from None
        except MessageBodyIsInvalidException as err:
            self.logger_service_provider.error(f"Invalid message body: {err}")
            raise MessageBodyIsInvalidException(err) from None
        except Exception as err:
            self.logger_service_provider.error(
                f"Unexpected: error while serializing: {err}")
            raise SerializationFailedException(err) from None

    def deserialize(self, event_entity_dict: dict[str:str]) -> EventEntity:
        """
        Based on the given dictionary type data, check all data values and,
        return an EventEntity type object.
        :param event_entity_dict:
        :return EventEntity:
        """
        event_type = event_entity_dict.get("event_type")
        body = event_entity_dict.get("body")
        to = event_entity_dict.get("to")
        try:
            validator.check_event_type(event_type)
            if event_type == config.APPROVED_PUBLICATION:
                validator.check_email_validation(to)
            validator.check_event_body(body)
            return EventEntity(
                event_type=event_type,
                body=body,
                to=to
            )
        except InvalidEventTypeException as err:
            self.logger_service_provider.error(f"Event Type is invalid: {err}")
            raise InvalidEventTypeException(err) from None
        except InvalidEmailException as err:
            self.logger_service_provider.error(f"Email is invalid: {err}")
            raise InvalidEmailException(err) from None
        except MessageBodyIsInvalidException as err:
            self.logger_service_provider.error(f"Invalid message body: {err}")
            raise MessageBodyIsInvalidException(err) from None
        except Exception as err:
            self.logger_service_provider.error(
                f"Unexpected: error while deserializing: {err}")
            raise DeserializationFailedException(err) from None
