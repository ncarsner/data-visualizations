import logging
import os


def setup_logging(
    default_path="config/logging.ini", default_level=logging.INFO, env_key="LOG_CFG"
):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        logging.config.fileConfig(path)
    else:
        logging.basicConfig(level=default_level)
        logging.warning(f"Logging configuration file not found: {path}")


def get_logger(name):
    """Get a logger with the specified name"""
    return logging.getLogger(name)


if __name__ == "__main__":
    setup_logging()
    logger = get_logger(__name__)
    logger.info("Logging is configured.")
