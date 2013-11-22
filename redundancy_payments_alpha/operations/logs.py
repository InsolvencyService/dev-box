import logging
from logging import StreamHandler
import sys

def configure_application_logging(app):
    """Configure application logging - this needs to be called very, very early
    in the application lifecycle.

    """
    logging.basicConfig(level=logging.INFO)
    handler = StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
