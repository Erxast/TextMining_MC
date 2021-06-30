import os

from peewee import SqliteDatabase
from tqdm import tqdm
import requests

from textmining_mc import logger, database_proxy
from textmining_mc.resources.joint_program.api import JointAPI
from textmining_mc.resources.pubtator.model import get_models_list, Article
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables


class PubmedPositiveSet(object):

    def __init__(self):
        self.dbh_proxy = None
        self.database = os.path.join('article_pubmed.db')
        self.db_type = 'sqlite'
        self.check_or_create_db()

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

    @staticmethod
    def process_article_data_pubmed():
        rob = requests.get(
            'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]&retmode=json&usehistory=y')
        query_key = rob.json()['esearchresult']['querykey']
        web_env = rob.json()['esearchresult']['webenv']
        urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
            query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json"
        rsearch = requests.get(urlsearch)
        id_all = rsearch.json()['esearchresult']['idlist']
        list_id_100 = []
        for elmt in tqdm(iterable=id_all, desc='creation_'):
            list_id_100.append(elmt)
            if len(list_id_100) == 100:
                JointAPI(list_id_100)
                list_id_100.clear()
        JointAPI(list_id_100)

    @staticmethod
    def removal_false_positive():
        """
        Deletes articles without abstracts

        :return:
        db
        """
        for arti in Article.select():
            if arti.abstract == "None":
                arti.delete_instance()
            elif arti.type != "Journal Article":
                arti.delete_instance()

    def run(self):
        # TODO: Method populate Article
        self.check_or_create_db()
        self.process_article_data_pubmed()
        self.removal_false_positive()
        # self.process_article_annotations()
        # self.afac()


if __name__ == '__main__':
    print('Start')
    p = PubmedPositiveSet()
    p.run()
    print('END')


class PubmedNegativeSet(object):

    def __init__(self):
        self.dbh_proxy = None
        self.database = os.path.join('article_negative.db')
        self.db_type = 'sqlite'
        self.check_or_create_db()

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





