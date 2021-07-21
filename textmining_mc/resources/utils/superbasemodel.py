import os

from textmining_mc import logger, database_proxy
from textmining_mc.resources.model import get_models_list
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables


class DatabaseModel(object):
    def __init__(self, data_name):
        self.dbh_proxy = None
        self.database = data_name
        self.db_type = 'sqlite'
        self.check_or_create_db()
        self.pmids_list = []
        # self.__connect_db()

    def check_or_create_db(self, force=False):
        """
        Create and connect resource database.
        Args:
            force (bool): True
        Returns:
        """
        mtd_name = '{cls_name}::{mtd_name}'.format(cls_name=self.__class__.__name__,
                                                   mtd_name=func_name(), )
        # Erase database if it already exists
        if force and os.path.isfile(self.database):
            os.unlink(self.database)

        # Create database if it does not exist
        if not os.path.isfile(self.database):
            logger.debug("{m} - Database '{dbname}' doest not exist!".format(m=mtd_name,
                                                                             dbname=os.path.basename(self.database)))

            # Create database tables
            logger.debug("{m} - Creating database {dbname}".format(m=mtd_name,
                                                                   dbname=os.path.basename(self.database)))
            # Initialize database connection
            if not self.dbh_proxy:
                self.dbh_proxy = connect_proxy_db(proxy=database_proxy,
                                                  name=self.database,
                                                  db_type=self.db_type,
                                                  )

            # Create tables
            create_proxy_db_tables(proxy=self.dbh_proxy,
                                   models_list=get_models_list(),
                                   force=force)
            logger.info("{m} - Creating database tables in {dbname}".format(m=mtd_name,
                                                                            dbname=os.path.basename(self.database)))
            self.dbh_proxy.close()
        else:
            # Initialize database connection
            if not self.dbh_proxy:
                self.dbh_proxy = connect_proxy_db(proxy=database_proxy,
                                                  name=self.database,
                                                  db_type=self.db_type,
                                                  )
