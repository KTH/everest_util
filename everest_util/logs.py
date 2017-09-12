"""
Initializes logging with coloredlogs
"""
__author__ = 'tinglev@kth.se'

import os
import coloredlogs

def init_logging(debug_env_var):
    """
    Initializes logging colors and levels. Should be called before any logging
    is done i the calling application.
    Args:
        debug_env_var: the name of the environment variable that decides
                       if logging level should be set to 'DEBUG'
    Returns:
        Nothing
    """
    field_style_override = coloredlogs.DEFAULT_FIELD_STYLES
    level_style_override = coloredlogs.DEFAULT_LEVEL_STYLES
    logging_level = 'INFO'
    if os.environ.get(debug_env_var):
        logging_level = 'DEBUG'
    field_style_override['levelname'] = {"color": "magenta", "bold": True}
    level_style_override['debug'] = {'color': 'blue'}
    coloredlogs.install(level=logging_level,
                        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
                        level_styles=level_style_override,
                        field_styles=field_style_override)
