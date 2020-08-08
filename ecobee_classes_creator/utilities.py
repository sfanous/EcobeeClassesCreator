import logging
from argparse import ArgumentParser

from ecobee_classes_creator.constants import DEFAULT_LOG_FILE_PATH

logger = logging.getLogger(__name__)


class Utility(object):
    __slots__ = []

    @classmethod
    def camel_case_to_underscore_case(cls, attribute_name):
        output = []
        for character in attribute_name:
            if character.isupper():
                output.append('_{0}'.format(character.lower()))
            else:
                output.append(character)

        return ''.join(output)

    @classmethod
    def parse_command_line_arguments(cls):
        parser = ArgumentParser()

        parser.add_argument(
            '-l',
            action='store',
            default=DEFAULT_LOG_FILE_PATH,
            dest='log_file_path',
            help='path to the log file',
            metavar='log file path',
        )

        arguments = parser.parse_args()

        return arguments.log_file_path
