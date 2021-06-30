import logging

from peewee import Proxy

logger = logging.getLogger(__name__)
database_proxy = Proxy()  # Create a proxy for our db.
