import json
import os
from pprint import pprint
import scispacy
import spacy
from spacy import displacy
import pandas

from peewee import SqliteDatabase
from tqdm import tqdm
from spacy import displacy

import requests
import xmltodict

from textmining_mc import logger, database_proxy
from textmining_mc.resources.joint_program.api import JointAPI
from textmining_mc.resources.pubtator.model import create_tables, connect_db, get_models_list, Article, AllAnnotation, \
    Annotation
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables


class Pubtator(object):

    def __init__(self):
        # self.api_url = 'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids='
        self.dbh_proxy = None
        self.database = os.path.join('article_mgt1.db')
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
    def process_article_data():
        fichier = open('/data/list_id_mgt.txt', 'r')
        list_mgt = []
        id_ = ""
        for i in fichier.read():
            if i == " ":
                list_mgt.append(id_)
                id_ = ""
            else:
                id_ = id_ + i
        list_mgt.append(id_)
        list_mgt_final = []
        for i in list_mgt:
            if i not in list_mgt_final:
                list_mgt_final.append(i)
        list_id_100 = []
        for elmt in tqdm(iterable=list_mgt_final, desc='part_1'):
            if len(list_id_100) == 100:
                JointAPI(list_id_100).efetch()
                JointAPI(list_id_100).removal_not_available()
                JointAPI(list_id_100).article_xml_content()
                list_id_100.clear()
                list_id_100.append(elmt)
            else:
                list_id_100.append(elmt)
        for i in tqdm(iterable=range(len(list_id_100)), desc='part_2'):
            JointAPI(list_id_100).efetch()
            JointAPI(list_id_100).removal_not_available()
            JointAPI(list_id_100).article_xml_content()

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

    def get_article_pmids(self):
        """
        Retrieve all article pmids

        Returns:
            list: list of pmids
        """
        query = Article.select()
        liste_id = list()
        for arti in query:
            liste_id.append(arti.id)
        self.pmids_list = liste_id

    @staticmethod
    def get_scispacy_annotation():
        """
        Add the informations available via the pkg Scispacy

        :return:
        """
        nlp = spacy.load("en_core_web_sm")
        annotation_title = []
        annotation_abstract = []
        for elmt in Article.select():
            title = elmt.title
            sci_title = nlp(title)
            for i in sci_title.ents:
                annotation_title.append((i.text, i.label_))
            abstract = elmt.abstract
            sci_abstract = nlp(abstract)
            for i in sci_abstract.ents:
                annotation_abstract.append((i.text, i.label_))
            print('Title: ', annotation_title)
            print('Abs: ', annotation_abstract)
            annotation_title.clear()
            annotation_abstract.clear()

    def get_article_annotation(self):
        """
        Add annotation of an article in the db 'Annotation'

        """
        for pmids in self.pmids_list:
            all_l = []
            query = AllAnnotation.select().where(AllAnnotation.id == pmids)
            for anno in query:
                pmids = anno.id
                mention = anno.mention
                bioconcept = anno.bioconcept
                identifier = anno.identifier
                tuple_anno = (pmids, mention, bioconcept, identifier)
                all_l.append(tuple_anno)
            Annotation.insert_many(all_l, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept, Annotation.identifiers]).execute()

    # def process_article_annotations(self):
    #     pmids = self.get_article_pmids()
    #     print(pmids)
    #     pmids_annots = list()
    #     for tmp_p in pmids:
    #         tmp_pmid_annots = self.get_article_annotation()
    #         pmids_annots.append(tmp_pmid_annots)
    #         exit()

    def run(self):
        # TODO: Method populate Article
        self.check_or_create_db()
        self.process_article_data()
        self.removal_false_positive()
        # self.process_article_annotations()
        # self.afac()


if __name__ == '__main__':
    print('Start')
    p = Pubtator()
    p.run()
    print('END')
