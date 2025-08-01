import logging
import sys

def setup_logger(name="ScribdDownloader", level="INFO"):
    """
    Mengkonfigurasi dan mengembalikan sebuah logger.

    Args:
        name (str): Nama logger.
        level (str): Level logging (DEBUG, INFO, WARNING, ERROR).

    Returns:
        logging.Logger: Instance logger yang sudah dikonfigurasi.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger