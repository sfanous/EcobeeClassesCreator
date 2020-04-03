import os
import sys

if getattr(sys, 'frozen', False):
    directory_containing_script = os.path.dirname(sys.executable)
else:
    directory_containing_script = sys.path[0]

DEFAULT_LOGGING_CONFIGURATION = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'MultiLine': {
            'format': '%(asctime)s %(name)-50s %(funcName)-40s %(levelname)-8s %(message)s',
            '()': 'ecobee_classes_creator.formatters.MultiLineFormatter',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'MultiLine',
            'class': 'logging.StreamHandler'
        },
        'rotating_file': {
            'level': 'INFO',
            'formatter': 'MultiLine',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.join(directory_containing_script, 'logs'),
                                     'ecobee_classes_creator.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10
        }
    },
    'loggers': {
        'ecobee_classes_creator': {
            'handlers': ['console', 'rotating_file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
DEFAULT_LOG_DIRECTORY_PATH = os.path.join(directory_containing_script, 'logs')
DEFAULT_LOG_FILE_PATH = os.path.join(DEFAULT_LOG_DIRECTORY_PATH, 'ecobee_classes_creator.log')
LOGGING_CONFIGURATION_FILE_PATH = os.path.join(directory_containing_script,
                                               'ecobee_classes_creator_logging_configuration.json')
VERSION = '1.0.0.0'
