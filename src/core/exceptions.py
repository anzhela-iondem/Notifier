# Custom defined exceptions

class InvalidEventTypeException(Exception):
    """Thrown when event type in not defined or defined wrong."""
    message = {"status": "failed", "error": "Invalid event type."}


class InvalidEmailException(Exception):
    """Throw when email address is invalid."""
    message = {"status": "failed", "error": "Invalid email address."}


class EmailIsNotSentException(Exception):
    """Throw when email sending process catches an exception."""
    message = {"status": "failed", "error": "Failed to send email."}


class SlackMessageIsNotSentException(Exception):
    """Throw when slack message sending process catches an exception."""
    message = {"status": "failed", "error": "Failed to send message to slack."}


class MessageBodyIsInvalidException(Exception):
    """Throw when body is not string or is empty string."""
    message = {"status": "failed", "error": "Invalid message body"}


class SerializationFailedException(Exception):
    """Throw when serialization is failed."""
    message = {"status": "failed", "error": "Serialization failed."}


class DeserializationFailedException(Exception):
    """Throw when deserialization is failed."""
    message = {"status": "failed", "error": "Serialization failed."}


class FailedToGetEnvItemEntityException(Exception):
    """Throw when environment variable is None."""
    message = {"status": "failed", "error": "Environmental item is None."}
