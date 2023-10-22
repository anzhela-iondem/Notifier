from email_validator import validate_email, EmailNotValidError

from src import config
from src.core.exceptions import InvalidEventTypeException, \
    MessageBodyIsInvalidException, InvalidEmailException


def check_event_type(event_type: str) -> bool:
    """
    Check if the event_type is one of the defined types.
    :param event_type:
    :return boolean:
    """
    if event_type in [config.NEW_PUBLICATION, config.APPROVED_PUBLICATION]:
        return True
    else:
        raise InvalidEventTypeException


def check_event_body(body: str) -> bool:
    """
    Check if the given string is not an empty string.
    :param body:
    :return boolean:
    """
    if isinstance(body, str) and body:
        return True
    else:
        raise MessageBodyIsInvalidException


def check_email_validation(email_address: str) -> bool:
    """
    Check if the email address is valid.
    :param email_address:
    :return: boolean
    """
    try:
        if validate_email(email_address, timeout=2).email:
            return True
        else:
            raise EmailNotValidError
    except EmailNotValidError as err:
        raise InvalidEmailException(err) from None
    except Exception as err:
        raise InvalidEmailException(err) from None
