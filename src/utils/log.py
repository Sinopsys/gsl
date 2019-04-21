"""
    Configs for loggers
"""

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[{asctime}] [{module} -> {process} -> {thread}] [{levelname}] >> {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'default_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'stdout': {
            'handlers': ['default_console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'manager': {
            'handlers': ['default_console'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}

