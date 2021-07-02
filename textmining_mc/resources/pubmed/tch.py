import os

from peewee import SqliteDatabase
from tqdm import tqdm
import requests

from textmining_mc import logger, database_proxy
from textmining_mc.resources.joint_program.api import JointAPI
from textmining_mc.resources.pubtator.model import get_models_list, Article
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables
from textmining_mc.resources.utils.superbasemodel import DatabaseModel


class Pubmed(DatabaseModel):

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

    def run(self):
        # TODO: Method populate Article
        super().check_or_create_db()
        self.process_article_data_pubmed()
        super().removal_false_positive()
        super().get_scispacy_annotation()


if __name__ == '__main__':
    print('start')
    p = Pubmed('article_pubmed')
    p.run()
    print('end')

