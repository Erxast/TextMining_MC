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

from textmining_mc import logger, database_proxy, configs
from textmining_mc.resources.joint_program.api import JointAPI
from textmining_mc.resources.model import create_tables, connect_db, get_models_list, Article, \
    Scispacy
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables
from textmining_mc.resources.utils.superbasemodel import DatabaseModel
from textmining_mc.resources.utils.transform_mtd import removal_false_positive, get_scispacy_annotation, \
    get_pubtator_annotation


class AllArticle(DatabaseModel):

    def __init__(self, data_name):
        self.root_data_path = configs['paths']['data']['root']
        database_path = os.path.join(self.root_data_path, data_name)
        super().__init__(database_path)
        # self.__connect_db()

    def process_article_data_mgt(self):
        fichier = open(os.path.join(self.root_data_path, 'list_id_mgt.txt'), 'r')
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
        for elmt in tqdm(iterable=list_mgt_final, desc='mgt'):
            list_id_100.append(elmt)
            if len(list_id_100) == 100:
                JointAPI(list_id_100, 'mgt')
                list_id_100.clear()
        JointAPI(list_id_100, 'mgt')

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
        for elmt in tqdm(iterable=id_all, desc='pubmed'):
            list_id_100.append(elmt)
            if len(list_id_100) == 100:
                JointAPI(list_id_100, 'pubmed')
                list_id_100.clear()
        JointAPI(list_id_100, 'pubmed')

    # @staticmethod
    # def get_pubtator_annotation():
    #     list_annotation = []
    #     list_pmids = []
    #     query = MG.select()
    #     for article in query:
    #         article_pmids = str(article.id)
    #         list_pmids.append(article_pmids)
    #         for annot in Annotation_Pubtator.select().where(Annotation_Pubtator.id == article_pmids):
    #             mention = annot.mention
    #             bioconcept = annot.bioconcept
    #             identifier = annot.identifier
    #             tuple_annot = (article_pmids, mention, bioconcept, identifier)
    #             list_annotation.append(tuple_annot)
    #         Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
    #                                                         Annotation.identifier]).execute()
    #         list_annotation.clear()

    def run(self):
        # TODO: Method populate Article
        super().check_or_create_db()
        self.process_article_data_mgt()
        self.process_article_data_pubmed()
        removal_false_positive()
        get_scispacy_annotation()
        get_pubtator_annotation()
        # self.get_pubtator_annotation()


if __name__ == '__main__':
    print('start')
    p = AllArticle('article')
    p.run()
    print('end')
