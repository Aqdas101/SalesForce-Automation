import logging


def setup_logging():

    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    success_handler = logging.FileHandler('success.log')
    success_handler.setLevel(logging.INFO)

    error_handler = logging.FileHandler('errors.log')
    error_handler.setLevel(logging.ERROR)

    success_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    error_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    success_handler.setFormatter(success_format)
    error_handler.setFormatter(error_format)

    logger.addHandler(success_handler)
    logger.addHandler(error_handler)

    return logger


logger = setup_logging()
