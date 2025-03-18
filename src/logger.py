import logging


def get_logger(task_name: str) -> logging.Logger:
    """
    Returns a logger object with handlers to log messages to the console.
    If a logger with the given name already exists, returns that logger.

    Args:
        task_name (str): The name of the task to include in the log messages.

    Returns:
        logging.Logger: A logger object with the specified handlers.
    """
    logger = logging.getLogger(task_name)

    # Check if this logger already has handlers configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
