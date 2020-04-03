import logging
import sys
import traceback

from ecobee_classes_creator.constants import VERSION
from ecobee_classes_creator.class_creator import ClassCreator
from ecobee_classes_creator.logging import Logging
from ecobee_classes_creator.scraper import Scraper
from ecobee_classes_creator.utilities import Utility

logger = logging.getLogger(__name__)


def main():
    try:
        log_file_path = Utility.parse_command_line_arguments()

        Logging.initialize_logging(log_file_path)

        logger.info('Starting up Ecobee Classes Creator {0}\n'
                    'Log file path                => {1}'.format(VERSION, log_file_path))

        Scraper.run()
        ClassCreator.run()
    except Exception:
        (type_, value_, traceback_) = sys.exc_info()
        logger.error('\n'.join(traceback.format_exception(type_, value_, traceback_)))
    finally:
        logger.info('Shutting down Ecobee Classes Creator {0}'.format(VERSION))
