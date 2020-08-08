import copy
import json
import logging
import logging.config
import sys
import traceback

from ecobee_classes_creator.constants import DEFAULT_LOGGING_CONFIGURATION
from ecobee_classes_creator.constants import LOGGING_CONFIGURATION_FILE_PATH

logger = logging.getLogger(__name__)


class Logging(object):
    __slots__ = []

    _logging_configuration_file_watchdog_observer = None
    _log_file_path = None

    @classmethod
    def get_log_file_path(cls):
        return cls._log_file_path

    @classmethod
    def initialize_logging(cls, log_file_path):
        try:
            cls.set_logging_configuration()
        except Exception:
            logging_configuration = copy.copy(DEFAULT_LOGGING_CONFIGURATION)
            logging_configuration['handlers']['rotating_file'][
                'filename'
            ] = log_file_path

            cls.set_logging_configuration(logging_configuration)

    @classmethod
    def set_logging_configuration(cls, configuration=None):
        if configuration is None:
            try:
                with open(
                    LOGGING_CONFIGURATION_FILE_PATH, 'r'
                ) as logging_configuration_file:
                    logging.config.dictConfig(json.load(logging_configuration_file))
            except FileNotFoundError:
                raise
            except Exception:
                (type_, value_, traceback_) = sys.exc_info()
                logger.error(
                    '\n'.join(traceback.format_exception(type_, value_, traceback_))
                )

                raise
        else:
            logging.config.dictConfig(configuration)

    @classmethod
    def set_log_file_path(cls, log_file_path):
        cls._log_file_path = log_file_path

    @classmethod
    def set_logging_level(cls, log_level):
        ecobee_classes_creator_logger = logging.getLogger('ecobee_classes_creator')

        ecobee_classes_creator_logger.setLevel(log_level)

        for handler in ecobee_classes_creator_logger.handlers:
            handler.setLevel(log_level)
