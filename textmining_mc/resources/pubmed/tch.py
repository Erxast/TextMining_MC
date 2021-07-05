import os

from peewee import SqliteDatabase
from tqdm import tqdm
import requests

from textmining_mc import logger, database_proxy
from textmining_mc.resources.joint_program.api import JointAPI
from textmining_mc.resources.model import get_models_list, Article
from textmining_mc.resources.model import Article as PubArticle
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables

from textmining_mc.resources.utils.transfrom_mtd import removal_false_positive, get_scispacy_annotation


class Pubmed(PM):

    def __init__(self, data_name):
        super().__init__(data_name)

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

    def get_pubtator_annotation(self):
        list_annotation = []
        query = Article.select()
        for article in query:
            article_pmids = str(article.id)
            for annot in Annotation_Pubtator.select().where(Annotation_Pubtator.id == article_pmids):
                mention = annot.mention
                bioconcept = annot.bioconcept
                identifier = annot.identifier
                tuple_annot = (article_pmids, mention, bioconcept, identifier)
                list_annotation.append(tuple_annot)
            Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
                                                            Annotation.identifier]).execute()
            list_annotation.clear()

    def run(self):
        # TODO: Method populate Article
        super().check_or_create_db()
        self.process_article_data_pubmed()
        removal_false_positive()
        get_scispacy_annotation()


if __name__ == '__main__':
    print('start')
    p = Pubmed('article_pubmed')
    p.run()
    print('end')

