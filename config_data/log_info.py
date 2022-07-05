from loguru import logger


def info_only(record):
    return record["level"].name == "INFO"


def debug_only(record):
    return record["level"].name == "DEBUG"


def warning_only(record):
    return record["level"].name == "WARNING"


my_logger = logger
my_logger.add('config_data/logs/info.log', format='{time} {message}', level='INFO', filter=info_only)
my_logger.add('config_data/logs/debug.log', format='{time} {message}', level='DEBUG', filter=debug_only)
my_logger.add('config_data/logs/warning.log', format='{time} {message}', level='WARNING', filter=warning_only)
