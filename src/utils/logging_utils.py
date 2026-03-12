import logging
import sys
from src.config import config

def setup_logging(level_name: str = None):
    """
    Setup centralized logging configuration.
    level_name: Name of the log level (debug, info, warning, error)
    """
    if level_name is None:
        level_name = config.get("log_level", "info")
    
    # Map string level to logging constants
    level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR
    }
    
    log_level = level_map.get(level_name.lower(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True # Override any existing configuration
    )
    
    return logging.getLogger("LOSAuto")
