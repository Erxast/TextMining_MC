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
from textmining_mc.resources.api.api import API
from textmining_mc.resources.model import create_tables, connect_db, get_models_list, Article, \
    Scispacy, PmidsGene, FArticle, Annotation, FAnnotation
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
                API(list_id_100, 'mgt')
                list_id_100.clear()
        API(list_id_100, 'mgt')

    @staticmethod
    def process_article_data_pubmed():
        rob = requests.get(os.path.join(configs['paths']['data']['pubmed'],
                                        'esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]&retmode=json&usehistory=y'))
        query_key = rob.json()['esearchresult']['querykey']
        web_env = rob.json()['esearchresult']['webenv']
        urlsearch = os.path.join(configs['paths']['data']['pubmed'], 'esearch.fcgi?db=pubmed&query_key=' + str(
            query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json")
        rsearch = requests.get(urlsearch)
        id_all = rsearch.json()['esearchresult']['idlist']
        list_id_100 = []
        for elmt in tqdm(iterable=id_all, desc='pubmed'):
            list_id_100.append(elmt)
            if len(list_id_100) == 100:
                API(list_id_100, 'pubmed')
                list_id_100.clear()
        API(list_id_100, 'pubmed')

    @staticmethod
    def intersection():
        count_article = 0
        count_annotation = 0
        list_joint_pmids = []
        list_pmids_gene = []
        list_article_final = []
        list_annotation_final = []
        query_pmids_gene = PmidsGene.select()
        for pmids in query_pmids_gene:
            list_pmids_gene.append(pmids.id)
        list_pmids_mc = []
        query_pmids_mc = Article.select()
        for pmids in query_pmids_mc:
            list_pmids_mc.append(pmids.id)
        for i in list_pmids_gene:
            if i in list_pmids_mc:
                list_joint_pmids.append(i)
        print(len(list_joint_pmids))
        print('start_article')
        for article in Article.select().where(Article.id.in_(list_joint_pmids)):
            count_article += 1
            id = article.id
            title = article.title
            date = article.date
            type = article.type
            abstract = article.abstract
            source = article.source
            tuple_article = (id, title, date, type, abstract, source)
            list_article_final.append(tuple_article)
            if count_article == 10000:
                FArticle.insert_many(list_article_final,
                                     fields=[FArticle.id, FArticle.title, FArticle.date, FArticle.type,
                                             FArticle.abstract, FArticle.source]).execute()
                list_article_final.clear()
                count_article = 0
        FArticle.insert_many(list_article_final,
                             fields=[FArticle.id, FArticle.title, FArticle.date, FArticle.type,
                                     FArticle.abstract, FArticle.source]).execute()
        print('start_annotation')
        for annotation in Annotation.select().where(Annotation.pmid.in_(list_joint_pmids)):
            count_annotation += 1
            pmid = annotation.pmid
            mention = annotation.mention
            bioconcept = annotation.bioconcept
            identifier = annotation.identifier
            tuple_annotation = (pmid, mention, bioconcept, identifier)
            list_annotation_final.append(tuple_annotation)
            if count_annotation == 10000:
                FAnnotation.insert_many(list_annotation_final,
                                        fields=[FAnnotation.pmid, FAnnotation.mention, FAnnotation.bioconcept,
                                                FAnnotation.identifier]).execute()
                list_annotation_final.clear()
                count_annotation = 0
        FAnnotation.insert_many(list_annotation_final,
                                fields=[FAnnotation.pmid, FAnnotation.mention, FAnnotation.bioconcept,
                                        FAnnotation.identifier]).execute()

    def run(self):
        # # TODO: Method populate Article
        # super().check_or_create_db()
        # self.process_article_data_mgt()
        # self.process_article_data_pubmed()
        # removal_false_positive()
        # get_pubtator_annotation()
        self.intersection()


if __name__ == '__main__':
    print('start')
    p = AllArticle('article')
    p.run()
    print('end')
