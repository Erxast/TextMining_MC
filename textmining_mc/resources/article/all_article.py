import json
import os
from collections import Counter
from pprint import pprint
import random

import scispacy
import spacy
from Bio import Entrez
from spacy import displacy
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from peewee import SqliteDatabase
from tqdm import tqdm
from spacy import displacy

import requests
import xmltodict

from textmining_mc import logger, database_proxy, configs
from textmining_mc import configs
from textmining_mc.resources.api.api import API
from textmining_mc.resources.model import create_tables, connect_db, get_models_list, Article, \
    Scispacy, PmidsGene, FArticle, Annotation, FAnnotation, NArticle
from textmining_mc.resources.utils import func_name
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables
from textmining_mc.resources.model import PmidsGene, Article, FArticle, Annotation, FAnnotation
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
                                        'esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]+english[language]&retmode=json&usehistory=y'))
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

    @staticmethod
    def negative_set():
        i = 0
        c = 0
        list_all = []
        query = Article.select().order_by(Article.date.desc())
        for arti in query:
            date_i = arti.date
            break
        for arti in query:
            date_i2 = arti.date
            if date_i == date_i2:
                date_i = date_i2
                date_av = arti.date
                i += 1
            elif date_i != date_i2 and i == 1:
                list_all.append([date_av, i])
                date_i = date_i2
                date_av = arti.date
                if c == (len(query) - 1):
                    list_all.append([arti.date, i])
            else:
                date_i = date_i2
                list_all.append([date_av, i])
                date_av = arti.date
                i = 1
            c += 1
        print('count_years_end')
        list_article_per_y = []
        for T in list_all:
            # Le while permet de repeter la boucle 'for' tant qu'il n'y a pas 1000 articles dans la base de données.
            compteur_article_annee = 0
            OK = 'False'
            while OK == 'False':
                # Recherche des articles par années
                rob = requests.get(
                    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=' + str(T[
                                                                                                            0]) + '[Date%20-%20Publication]+journal+article[publication%20type]+&retmode=json&usehistory=y')
                query_key = rob.json()['esearchresult']['querykey']
                web_env = rob.json()['esearchresult']['webenv']
                # Recupération d'une liste d'ID par années
                urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
                    query_key) + "&WebEnv=" + str(web_env) + "&retmax=5000&usehistory=y&retmode=json"
                rsearch = requests.get(urlsearch)
                id_all = rsearch.json()['esearchresult']['idlist']
                random_id_all = []
                # Obtention d'une liste de 1000 articles choisi au hasard parmis les 5000 (déjà pris au hasard)
                for F in range(1000):
                    random_id = random.choice(id_all)
                    random_id_all.append(random_id)
                    id_all.remove(random_id)
                for elmt in tqdm(iterable=random_id_all, desc='creation_'):
                    # Permet de faire sortir de la boucle si on arrive à 1000 articles dans la base de donnée
                    if compteur_article_annee == 1000:
                        break
                    Entrez.email = "hugues.escoffier@etu.unsitra.fr"
                    handle = Entrez.efetch(db="pubmed", id=random_id_all, retmode="xml", rettype="abstract")
                    records = Entrez.read(handle)
                    # Permet de supprimer les éventuels <PubmedBookArticle>
                    data_ = records["PubmedArticle"]
                    if len(data_) != len(random_id_all):
                        for i in range(len(random_id_all) - len(data_)):
                            Id_unwanted = ''.join(records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
                            random_id_all.remove(Id_unwanted)
                    # Récup. des données à l'intérieur des articles :
                    for i in range(len(random_id_all)):
                        # Récup. Abstract
                        try:
                            abstract_ = ''.join(
                                records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
                        except:
                            abstract_ = "None"
                        # Récup. Title
                        title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
                        # Récup. PublicationType
                        publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"][
                            "PublicationTypeList"]
                        if len(publication_type_list) != 1:
                            z = 0
                            for y in range(len(publication_type_list)):
                                if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"][
                                               "PublicationTypeList"][
                                               y]) == "Journal Article":
                                    publication_type_ = "Journal Article"
                                    z = 1
                            if z == 0:
                                publication_type_ = "Other"
                        else:
                            publication_type_ = ''.join(
                                records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
                        # Récup. Date
                        try:
                            date_ = ''.join(
                                records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"][
                                    "PubDate"]["Year"])
                        except:
                            try:
                                date_ = ''.join(
                                    records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
                            except:
                                complete_date_ = ''.join(
                                    records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"][
                                        "JournalIssue"][
                                        "PubDate"]["MedlineDate"])
                                date_ = ''
                                c = 0
                                for lettre in complete_date_:
                                    if c == 4:
                                        break
                                    date_ = date_ + lettre
                                    c += 1
                        # Ajout à la base de données (le "if" permet d'éviter les faux positifs)
                        if publication_type_ == 'Journal Article' and abstract_ != 'None' and date_ == T[0]:
                            NArticle.create(id=random_id_all[i], title=title_, date=date_, type=publication_type_, abstract=abstract_, source='pubmed')
                            compteur_article_annee += 1
                        if compteur_article_annee == 1000:
                            OK = 'True'
                            print(T[0])
                            break
        print('selection_article_end')

    def ps_spacy_frequency(self):
        """

        Returns:

        pprint(dict_word)
        """
        nlp = spacy.load("en_core_web_sm")
        list_word = []
        for article in Article.select():
            doc_title = nlp(article.title)
            doc_abstract = nlp(article.abstract)
            for token in doc_title:
                if not token.is_stop and not token.is_punct and not token.like_num:
                    list_word.append(token.lemma_)
            for token in doc_abstract:
                if not token.is_stop and not token.is_punct and not token.like_num:
                    list_word.append(token.lemma_)
        word_freq = Counter(list_word)
        dataframe_word = pd.DataFrame.from_dict(word_freq, orient='index').reset_index()
        self.dataframe_word = dataframe_word.rename(columns={'index': 'word', 0: 'counts'})
        self.dataframe_word.to_csv(path_or_buf=os.path.join(configs['paths']['data']['root'], 'df_ps_csv'), index=False)

    def ps_wordcloud(self):
        d = {}
        for a, x in self.dataframe_word.values:
            d[a] = x
        wordcloud = WordCloud(background_color='white')
        wordcloud.generate_from_frequencies(frequencies=d)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def run(self):
        # TODO: Method populate Article
        super().check_or_create_db()
        self.process_article_data_mgt()
        self.process_article_data_pubmed()
        removal_false_positive()
        get_pubtator_annotation()
        self.intersection()
        # self.ps_spacy_frequency()
        # self.ps_wordcloud()
        self.negative_set()


if __name__ == '__main__':
    print('start')
    p = AllArticle('article')
    p.run()
    print('end')
