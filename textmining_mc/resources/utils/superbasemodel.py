import os

import spacy

from tqdm import tqdm
from textmining_mc import logger, database_proxy
from textmining_mc.resources.pubtator.model import get_models_list, Article, Scispacy
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables


class DatabaseModel(object):
    def __init__(self, data_name):
        self.dbh_proxy = None
        self.database = os.path.join(data_name)
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

    @staticmethod
    def get_scispacy_annotation():
        """
        Add the informations available via the pkg Scispacy

        :return:
        """
        nlp = spacy.load("en_core_web_sm")
        scispacy_annotation = []
        for elmt in tqdm(iterable=Article.select(), desc='scispacy'):
            id = elmt.id
            title = elmt.title
            sci_title = nlp(title)
            for i in sci_title.ents:
                scispacy_annotation.append((id, i.text, i.label_))
            abstract = elmt.abstract
            sci_abstract = nlp(abstract)
            for i in sci_abstract.ents:
                scispacy_annotation.append((id, i.text, i.label_))
            Scispacy.insert_many(scispacy_annotation, fields=[Scispacy.pmid, Scispacy.word, Scispacy.type]).execute()
            scispacy_annotation.clear()
