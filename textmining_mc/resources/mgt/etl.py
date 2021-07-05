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
from textmining_mc.resources.utils.transfrom_mtd import removal_false_positive, get_scispacy_annotation


class Pubtator(DatabaseModel):

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
        for elmt in tqdm(iterable=list_mgt_final, desc='creation'):
            list_id_100.append(elmt)
            if len(list_id_100) == 100:
                JointAPI(list_id_100)
                list_id_100.clear()
        JointAPI(list_id_100)

    # def get_article_pmids(self):
    #     """
    #     Retrieve all article pmids
    #
    #     Returns:
    #         list: list of pmids
    #     """
    #     query = Article.select()
    #     liste_id = list()
    #     for arti in query:
    #         liste_id.append(arti.id)
    #     self.pmids_list = liste_id

    def run(self):
        # TODO: Method populate Article
        super().check_or_create_db()
        self.process_article_data_mgt()
        removal_false_positive()
        get_scispacy_annotation()


if __name__ == '__main__':
    print('start')
    p = Pubtator('article_mgt')
    p.run()
    print('end')
