import abc
from typing import Optional

from flask import jsonify

from src import config
from src.core.exceptions import InvalidEventTypeException, \
    EmailIsNotSentException, SlackMessageIsNotSentException, \
    MessageBodyIsInvalidException, DeserializationFailedException, \
    FailedToGetEnvItemEntityException, InvalidEmailException
from src.core.use_cases import NotifierUseCase
from src.infrastructure.providers import EmailServiceProvider, \
    LoggerServiceProvider, SlackMessengerProvider
from src.infrastructure.repositories import ConfigRepo
from src.infrastructure.serializers import EventSerializer
from src.infrastructure.services import EmailService, LoggerService, \
    SlackService


class BaseController(abc.ABC):

    def __init__(self):
        self._slack_service: Optional[SlackService] = None
        self._email_service: Optional[EmailService] = None
        self._logg_service: Optional[LoggerService] = None
        self._env_repo: Optional[ConfigRepo] = None
        self._messenger_service_provider: Optional[
            SlackMessengerProvider] = None
        self._email_provider: Optional[EmailServiceProvider] = None
        self._logger_service_provider: Optional[LoggerServiceProvider] = None

    @property
    def slack_service(self) -> SlackService:
        """
        Check, create and return a SlackService object instance.
        :return SlackService object:
        """
        if self._slack_service is None:
            self._slack_service = SlackService(
                slack_token=self.env_repo.get_one(config.SLACK_TOKEN).value
            )
        return self._slack_service

    @property
    def email_service(self) -> EmailService:
        """
        Check, create and return an EmailService object instance.
        :return: EmailService object.
        """
        if self._email_service is None:
            self._email_service = EmailService(
                smtp_host=self.env_repo.get_one(config.SMTP_HOST).value,
                smtp_port=self.env_repo.get_one(config.SMTP_PORT).value,
                email_username=self.env_repo.get_one(
                    config.EMAIL_USERNAME).value,
                email_app_pass=self.env_repo.get_one(
                    config.EMAIL_APP_PASS).value,
                from_email=self.env_repo.get_one(config.FROM_EMAIL).value,
                email_subject=config.EMAIL_SUBJECT
            )
        return self._email_service

    @property
    def logger_service(self) -> LoggerService:
        """
        Check, create and return a LoggerService object instance.
        :return: LoggerService object.
        """
        if self._logg_service is None:
            self._logg_service = LoggerService(
                logger_name=config.LOGGER_NAME,
                formatter=config.DEFAULT_LOG_FORMAT,
                log_file_path=config.LOG_FILE_PATH,
                log_level=config.DEFAULT_LOG_LEVEL
            )
        return self._logg_service

    @property
    def env_repo(self) -> ConfigRepo:
        """
        Check, create and return an ConfigRepo object instance.
        :return: LoggerService object.
        """
        if self._env_repo is None:
            self._env_repo = ConfigRepo()
        return self._env_repo

    @property
    def email_service_provider(self):
        """
        Check, create and return an email service provider that provides
        an email service.
        :return EmailServiceProvider:
        """
        if self._email_provider is None:
            self._email_provider = EmailServiceProvider(
                self.logger_service_provider,
                self.email_service
            )
        return self._email_provider

    @property
    def messenger_service_provider(self) -> SlackMessengerProvider:
        """
        Check, create and return a slack service provider that provides
        a slack service.
        :return SlackMessengerProvider:
        """
        if self._messenger_service_provider is None:
            self._messenger_service_provider = SlackMessengerProvider(
                self.logger_service_provider, self.slack_service
            )
        return self._messenger_service_provider

    @property
    def logger_service_provider(self) -> LoggerServiceProvider:
        """
        Check, create and return a logging service provider that provides
        a logging service.
        :return LoggerServiceProvider:
        """
        if self._logger_service_provider is None:
            self._logger_service_provider = LoggerServiceProvider(
                self.logger_service
            )
        return self._logger_service_provider


class APIController(BaseController):

    def process_event(self, event_data: dict[str, str]):
        """
        Get POST request data, deserialize to EventEntity and, according to
        data, continue executing the appropriate use case.
        :param event_data:
        :return None:
        """
        try:
            event_serializer = EventSerializer(self.logger_service_provider)
            event_entity = event_serializer.deserialize(event_data)
            self.logger_service_provider.info("Request data is deserialized.")
            if event_entity.event_type == config.NEW_PUBLICATION:
                notifier_use_case = NotifierUseCase(
                    event_entity,
                    self.messenger_service_provider
                )
                notifier_use_case.execute()
                return jsonify({"status": "success",
                                "message": "Slack message is sent."}), 200
            elif event_entity.event_type == config.APPROVED_PUBLICATION:
                notifier_use_case = NotifierUseCase(
                    event_entity,
                    self.email_service_provider
                )
                notifier_use_case.execute()
                return jsonify({"status": "success",
                                "message": "Email is sent."}), 200
        except InvalidEventTypeException as err:
            return jsonify(err.message), 400
        except InvalidEmailException as err:
            return jsonify(err.message), 400
        except MessageBodyIsInvalidException as err:
            return jsonify(err.message), 400
        except EmailIsNotSentException as err:
            return jsonify(err), 400
        except SlackMessageIsNotSentException as err:
            return jsonify(err.message), 400
        except DeserializationFailedException as err:
            return jsonify(err.message), 400
        except FailedToGetEnvItemEntityException as err:
            self.logger_service_provider.error(
                f"Failed to get an environmental variable.")
            return jsonify(err), 400
        except Exception as err:
            self.logger_service_provider.error(
                f"Unexpected error: event is failed to process:{err}")
            return jsonify({"status": "failed",
                            "error": "Unexpected error"}), 400
