import json
import os
from pprint import pprint

import requests
import xmltodict

from textmining_mc import logger, database_proxy
from textmining_mc.resources.pubtator.model import create_tables, connect_db, get_models_list, Article
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables


class Pubtator(object):

    def __init__(self):
        self.api_url = 'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids='
        self.dbh_proxy = None
        self.database = os.path.join('article_mgt1.db')
        self.db_type = 'sqlite'
        self.check_or_create_db()
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

    # TODO:
    def process_article_data(self):
        pass

    @staticmethod
    def get_article_pmids():
        """
        Retrieve all article pmids

        Returns:
            list: list of pmids
        """
        query = Article.select()
        liste_id = list()
        for arti in query:
            liste_id.append(arti.id)

        return liste_id

    def get_article_annotation(self, pmid):
        """
        Retrieve Pubtator annotations for a given pmid

        Args:
            pmid (int): Article pmid

        Returns:
            dict: pmid annotations
        """
        result = dict()
        query_url = '{u}{i}'.format(u=self.api_url, i=pmid)
        rob = requests.get(query_url)
        data = xmltodict.parse(rob.content)

        pprint(data)
        # document = data_["collection"]["document"]
        # tree = document['passage']

        return result

    def process_article_annotations(self):
        pmids = self.get_article_pmids()
        print(pmids)
        pmids_annots = list()
        for tmp_p in pmids:
            tmp_pmid_annots = self.get_article_annotation(pmid=tmp_p)
            pmids_annots.append(tmp_pmid_annots)
            exit()

    def afac(self):
        query_url = 'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=28483577'
        response = requests.get(query_url)

        pprint(response.json())
        print()

        json_data = json.loads(response.text)
        pprint(json_data)

    def run(self):
        # TODO: Method populate Article
        self.process_article_data()

        # self.process_article_annotations()

        self.afac()


if __name__ == '__main__':
    print('Start')
    p = Pubtator()
    p.run()
    print('END')
