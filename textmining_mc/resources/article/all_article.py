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

    def article_per_keyword(self):
        fichier = open(os.path.join(self.root_data_path, 'Histological Terms.txt'), 'r')
        list_word = []
        word = ""
        for i in fichier.read():
            if i == "\n":
                list_word.append(word)
                word = ""
            else:
                word = word + i
        list_word.append(word)
        fichier.close()
        for elmt in list_word:
            elmt_query = ''
            for i in elmt:
                if i == ' ':
                    elmt_query += '+'
                else:
                    elmt_query += i
            # Request_for_QK_&_WE
            url_request = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=' + str(
                elmt_query) + '+congenital+myopathy+journal+article[publication%20type]+english[language]&retmode=json&usehistory=y'
            rob = requests.get(url_request)
            count = rob.json()['esearchresult']['count']
            if count != '0':
                query_key = rob.json()['esearchresult']['querykey']
                web_env = rob.json()['esearchresult']['webenv']
                # Request_for_list_of_ID
                urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
                    query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json"
                rsearch = requests.get(urlsearch)
                id_keyword = rsearch.json()['esearchresult']['idlist']
                list_pmids_100 = []
                for pmids in tqdm(iterable=id_keyword, desc=str(elmt)):
                    list_pmids_100.append(pmids)
                    if len(list_pmids_100) == 100:
                        API(list_pmids_100, 'pubmed', str(elmt))
                        list_pmids_100.clear()
                API(list_pmids_100, 'pubmed', str(elmt))

    def keyword_disease_gene(self):
        # list_pmids = []
        # list_keyword = []
        # for article in Article.select():
        #     pmids = article.id
        #     keyword = article.keyword
        #     list_pmids.append(pmids)
        #     list_keyword.append(keyword)
        # with open(os.path.join(self.root_data_path, 'keyword_gene_disease.txt'), 'w') as fichier:
        #     i = 0
        #     for pmid in tqdm(iterable=list_pmids, desc='writing'):
        #         keyword = list_keyword[i]
        #         fichier.write(str(keyword) + '\n')
        #         for annotation in Annotation.select().where(Annotation.pmid == str(pmid)):
        #             if annotation.bioconcept == 'Gene':
        #                 fichier.write(str(annotation.identifier) + '\t')
        #             if annotation.bioconcept == 'Disease':
        #                 fichier.write(str(annotation.identifier) + '\t')
        #         i += 1
        #         fichier.write('\n')
        keyword_gene_or_disease = []
        for annotation in Annotation.select().where(Annotation.bioconcept == 'Gene'):
            identifier = annotation.identifier
            for article in Article.select().where(Article.id == annotation.pmid):
                keyword = article.keyword
                keyword_gene_or_disease.append((keyword, annotation.bioconcept, identifier))
            break
        for annotation in Annotation.select().where(Annotation.bioconcept == 'Disease'):
            identifier = annotation.identifier
            for article in Article.select().where(Article.id == annotation.pmid):
                keyword = article.keyword
                keyword_gene_or_disease.append((keyword, annotation.bioconcept, identifier))
            break
        print(keyword_gene_or_disease)







    # def process_article_data_mgt(self):
    #     fichier = open(os.path.join(self.root_data_path, 'list_id_mgt.txt'), 'r')
    #     list_mgt = []
    #     id_ = ""
    #     for i in fichier.read():
    #         if i == " ":
    #             list_mgt.append(id_)
    #             id_ = ""
    #         else:
    #             id_ = id_ + i
    #     list_mgt.append(id_)
    #     list_mgt_final = []
    #     for i in list_mgt:
    #         if i not in list_mgt_final:
    #             list_mgt_final.append(i)
    #     list_id_100 = []
    #     for elmt in tqdm(iterable=list_mgt_final, desc='mgt'):
    #         list_id_100.append(elmt)
    #         if len(list_id_100) == 100:
    #             API(list_id_100, 'mgt', '')
    #             list_id_100.clear()
    #     API(list_id_100, 'mgt', '')
    #     fichier.close()
    #
    # @staticmethod
    # def process_article_data_pubmed():
    #     rob = requests.get(os.path.join(configs['paths']['data']['pubmed'],
    #                                     'esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]+english[language]&retmode=json&usehistory=y'))
    #     query_key = rob.json()['esearchresult']['querykey']
    #     web_env = rob.json()['esearchresult']['webenv']
    #     urlsearch = os.path.join(configs['paths']['data']['pubmed'], 'esearch.fcgi?db=pubmed&query_key=' + str(
    #         query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json")
    #     rsearch = requests.get(urlsearch)
    #     id_all = rsearch.json()['esearchresult']['idlist']
    #     list_id_100 = []
    #     for elmt in tqdm(iterable=id_all, desc='pubmed'):
    #         list_id_100.append(elmt)
    #         if len(list_id_100) == 100:
    #             API(list_id_100, 'pubmed', '')
    #             list_id_100.clear()
    #     API(list_id_100, 'pubmed', '')
    #
    # @staticmethod
    # def intersection():
    #     count_article = 0
    #     count_annotation = 0
    #     list_joint_pmids = []
    #     list_pmids_gene = []
    #     list_article_final = []
    #     list_annotation_final = []
    #     query_pmids_gene = PmidsGene.select()
    #     for pmids in query_pmids_gene:
    #         list_pmids_gene.append(pmids.id)
    #     list_pmids_mc = []
    #     query_pmids_mc = Article.select()
    #     for pmids in query_pmids_mc:
    #         list_pmids_mc.append(pmids.id)
    #     for i in list_pmids_gene:
    #         if i in list_pmids_mc:
    #             list_joint_pmids.append(i)
    #     print('start_article')
    #     for article in Article.select().where(Article.id.in_(list_joint_pmids)):
    #         count_article += 1
    #         id = article.id
    #         title = article.title
    #         date = article.date
    #         type = article.type
    #         abstract = article.abstract
    #         source = article.source
    #         tuple_article = (id, title, date, type, abstract, source)
    #         list_article_final.append(tuple_article)
    #         if count_article == 10000:
    #             FArticle.insert_many(list_article_final,
    #                                  fields=[FArticle.id, FArticle.title, FArticle.date, FArticle.type,
    #                                          FArticle.abstract, FArticle.source]).execute()
    #             list_article_final.clear()
    #             count_article = 0
    #     FArticle.insert_many(list_article_final,
    #                          fields=[FArticle.id, FArticle.title, FArticle.date, FArticle.type,
    #                                  FArticle.abstract, FArticle.source]).execute()
    #     print('start_annotation')
    #     for annotation in Annotation.select().where(Annotation.pmid.in_(list_joint_pmids)):
    #         count_annotation += 1
    #         pmid = annotation.pmid
    #         mention = annotation.mention
    #         bioconcept = annotation.bioconcept
    #         identifier = annotation.identifier
    #         tuple_annotation = (pmid, mention, bioconcept, identifier)
    #         list_annotation_final.append(tuple_annotation)
    #         if count_annotation == 10000:
    #             FAnnotation.insert_many(list_annotation_final,
    #                                     fields=[FAnnotation.pmid, FAnnotation.mention, FAnnotation.bioconcept,
    #                                             FAnnotation.identifier]).execute()
    #             list_annotation_final.clear()
    #             count_annotation = 0
    #     FAnnotation.insert_many(list_annotation_final,
    #                             fields=[FAnnotation.pmid, FAnnotation.mention, FAnnotation.bioconcept,
    #                                     FAnnotation.identifier]).execute()
    #
    # @staticmethod
    # def negative_set():
    #     i = 0
    #     c = 0
    #     list_all = []
    #     query = Article.select().order_by(Article.date.desc())
    #     for arti in query:
    #         date_i = arti.date
    #         break
    #     for arti in query:
    #         date_i2 = arti.date
    #         if date_i == date_i2:
    #             date_i = date_i2
    #             date_av = arti.date
    #             i += 1
    #         elif date_i != date_i2 and i == 1:
    #             list_all.append([date_av, i])
    #             date_i = date_i2
    #             date_av = arti.date
    #             if c == (len(query) - 1):
    #                 list_all.append([arti.date, i])
    #         else:
    #             date_i = date_i2
    #             list_all.append([date_av, i])
    #             date_av = arti.date
    #             i = 1
    #         c += 1
    #     print('count_years_end')
    #     list_article_per_y = []
    #     for T in list_all:
    #         # Le while permet de repeter la boucle 'for' tant qu'il n'y a pas 1000 articles dans la base de données.
    #         compteur_article_annee = 0
    #         OK = 'False'
    #         while OK == 'False':
    #             # Recherche des articles par années
    #             rob = requests.get(
    #                 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=' + str(T[
    #                                                                                                         0]) + '[Date%20-%20Publication]+journal+article[publication%20type]+english[language]&retmode=json&usehistory=y')
    #             query_key = rob.json()['esearchresult']['querykey']
    #             web_env = rob.json()['esearchresult']['webenv']
    #             # Recupération d'une liste d'ID par années
    #             urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
    #                 query_key) + "&WebEnv=" + str(web_env) + "&retmax=5000&usehistory=y&retmode=json"
    #             rsearch = requests.get(urlsearch)
    #             id_all = rsearch.json()['esearchresult']['idlist']
    #             random_id_all = []
    #             # Obtention d'une liste de 1000 articles choisi au hasard parmis les 5000 (déjà pris au hasard)
    #             for F in range(1000):
    #                 random_id = random.choice(id_all)
    #                 random_id_all.append(random_id)
    #                 id_all.remove(random_id)
    #             for elmt in tqdm(iterable=random_id_all, desc='creation_'):
    #                 # Permet de faire sortir de la boucle si on arrive à 1000 articles dans la base de donnée
    #                 if compteur_article_annee == 1000:
    #                     break
    #                 Entrez.email = "hugues.escoffier@etu.unsitra.fr"
    #                 handle = Entrez.efetch(db="pubmed", id=random_id_all, retmode="xml", rettype="abstract")
    #                 records = Entrez.read(handle)
    #                 # Permet de supprimer les éventuels <PubmedBookArticle>
    #                 data_ = records["PubmedArticle"]
    #                 if len(data_) != len(random_id_all):
    #                     for i in range(len(random_id_all) - len(data_)):
    #                         Id_unwanted = ''.join(records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
    #                         random_id_all.remove(Id_unwanted)
    #                 # Récup. des données à l'intérieur des articles :
    #                 for i in range(len(random_id_all)):
    #                     # Récup. Abstract
    #                     try:
    #                         abstract_ = ''.join(
    #                             records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
    #                     except:
    #                         abstract_ = "None"
    #                     # Récup. Title
    #                     title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
    #                     # Récup. PublicationType
    #                     publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"][
    #                         "PublicationTypeList"]
    #                     if len(publication_type_list) != 1:
    #                         z = 0
    #                         for y in range(len(publication_type_list)):
    #                             if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"][
    #                                            "PublicationTypeList"][
    #                                            y]) == "Journal Article":
    #                                 publication_type_ = "Journal Article"
    #                                 z = 1
    #                         if z == 0:
    #                             publication_type_ = "Other"
    #                     else:
    #                         publication_type_ = ''.join(
    #                             records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
    #                     # Récup. Date
    #                     try:
    #                         date_ = ''.join(
    #                             records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"][
    #                                 "PubDate"]["Year"])
    #                     except:
    #                         try:
    #                             date_ = ''.join(
    #                                 records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
    #                         except:
    #                             complete_date_ = ''.join(
    #                                 records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"][
    #                                     "JournalIssue"][
    #                                     "PubDate"]["MedlineDate"])
    #                             date_ = ''
    #                             c = 0
    #                             for lettre in complete_date_:
    #                                 if c == 4:
    #                                     break
    #                                 date_ = date_ + lettre
    #                                 c += 1
    #                     # Ajout à la base de données (le "if" permet d'éviter les faux positifs)
    #                     if publication_type_ == 'Journal Article' and abstract_ != 'None' and date_ == T[0]:
    #                         NArticle.create(id=random_id_all[i], title=title_, date=date_, type=publication_type_, abstract=abstract_, source='pubmed')
    #                         compteur_article_annee += 1
    #                     if compteur_article_annee == 1000:
    #                         OK = 'True'
    #                         print(T[0])
    #                         break
    #     print('selection_article_end')
    #
    # @staticmethod
    # def ps_spacy_frequency():
    #     """
    #
    #     Returns:
    #
    #     pprint(dict_word)
    #     """
    #     nlp = spacy.load("en_core_web_sm")
    #     list_word = []
    #     for article in Article.select():
    #         doc_title = nlp(article.title)
    #         doc_abstract = nlp(article.abstract)
    #         for token in doc_title:
    #             if not token.is_stop and not token.is_punct and not token.like_num:
    #                 list_word.append(token.lemma_)
    #         for token in doc_abstract:
    #             if not token.is_stop and not token.is_punct and not token.like_num:
    #                 list_word.append(token.lemma_)
    #     word_freq = Counter(list_word)
    #     dataframe_word = pd.DataFrame.from_dict(word_freq, orient='index').reset_index()
    #     dataframe_word = dataframe_word.rename(columns={'index': 'word', 0: 'counts'})
    #     dataframe_word.to_csv(path_or_buf=os.path.join(configs['paths']['data']['root'], 'df_ps_csv'), index=False)
    #
    # @staticmethod
    # def ps_wordcloud():
    #     df = pd.read_csv(filepath_or_buffer=os.path.join(configs['paths']['data']['root'], 'df_ps_csv'))
    #     d = {}
    #     for a, x in df.values:
    #         d[a] = x
    #     wordcloud = WordCloud(background_color='white')
    #     wordcloud.generate_from_frequencies(frequencies=d)
    #     plt.figure()
    #     plt.imshow(wordcloud, interpolation="bilinear")
    #     plt.axis("off")
    #     plt.show()
    #
    # @staticmethod
    # def pmids_histology():
    #     """
    #
    #     Returns:
    #
    #     pprint(dict_word)
    #     """
    #     nlp = spacy.load("en_core_web_sm")
    #     list_histo_term = ['histopathological', 'immunohistochemical', 'histological', 'immunohistochemistry', 'histology', 'Histologic', 'histopathology', 'histochemical', 'histopathologic', 'histologic', 'immunohistologic', 'histoenzymology', 'histochemistry', 'histocompatibility', 'immunohistology', 'histologically', 'Immunohistochemistry',
    #                        'Histology', 'histopatological', 'histomorphological', 'histopathologically', 'histoenzymatic', 'Histopathologic', 'Histopathologically', 'neurohistopathological', 'histopathologie', 'Immunohistochemical', 'Histopathology', 'histoenzymological', 'immunohistochemically', 'immunhistochemistry', 'histomorphology', 'immunohistofluorescence',
    #                        'Histochemistry', 'histochemically', 'immunohistological', 'histopathogenic', 'lmmunohistochemical', 'histomorphometric', 'histo', 'clinicohistopathological', 'Histometric', 'histometric', 'histogenic', 'biopsy', 'Biopsy', 'biopsied', 'biopsie', 'biopsye']
    #     list_histo_pmids = []
    #     list_histo_pmids_pre = []
    #     list_word = []
    #     for article in Article.select():
    #         doc_abstract = nlp(article.abstract)
    #         for token in doc_abstract:
    #             if token.lemma_ in list_histo_term:
    #                 list_histo_pmids_pre.append(article.id)
    #     for i in list_histo_pmids_pre:
    #         if i not in list_histo_pmids:
    #             list_histo_pmids.append(i)
    #     for article in Article.select().where(Article.id.in_(list_histo_pmids)):
    #         doc_title = nlp(article.title)
    #         doc_abstract = nlp(article.abstract)
    #         for token in doc_title:
    #             if not token.is_stop and not token.is_punct and not token.like_num:
    #                 list_word.append(token.lemma_)
    #         for token in doc_abstract:
    #             if not token.is_stop and not token.is_punct and not token.like_num:
    #                 list_word.append(token.lemma_)
    #     word_freq = Counter(list_word)
    #     dataframe_word = pd.DataFrame.from_dict(word_freq, orient='index').reset_index()
    #     dataframe_word = dataframe_word.rename(columns={'index': 'word', 0: 'counts'})
    #     dataframe_word.to_csv(path_or_buf=os.path.join(configs['paths']['data']['root'], 'df_only_histo_csv'), index=False)
    #     d = {}
    #     for a, x in dataframe_word.values:
    #         d[a] = x
    #     wordcloud = WordCloud(background_color='white')
    #     wordcloud.generate_from_frequencies(frequencies=d)
    #     plt.figure()
    #     plt.imshow(wordcloud, interpolation="bilinear")
    #     plt.axis("off")
    #     plt.show()
    #     # len = 1857 -> ['9860777', '31403083', '30652412', '9158149', '26846950', '23768516', '17924338', '12687498', '24934289', '11166163', '23109149', '26133662', '22742743', '12369018', '8268915', '8266101', '17923109', '12707075', '20068593', '25260562', '30327447', '7581449', '8968749', '30543681', '22371254', '22187985', '11992570', '11592034', '10677302', '11741828', '26666891', '26208961', '31039582', '10746614', '17444505', '23768512', '9635427', '23975875', '10329755', '25589244', '12644968', '15496425', '21480433', '26437932', '11117544', '15947997', '20554658', '16365872', '18300303', '14575234', '11506403', '24827497', '24488655', '31852522', '27008887', '10071056', '10520946', '19553118', '10848494', '11992252', '25065913', '21835308', '31463572', '10838249', '18006477', '27066570', '21698661', '31092906', '21530252', '12112081', '12192640', '16380616', '15580566', '30611313', '29518281', '21953594', '26718575', '11782989', '28262468', '17337483', '19949035', '30010796', '20045868', '23401021', '12145747', '21388311', '9497249', '15036327', '11294923', '20697106', '22334415', '19726876', '9590299', '27485408', '32779703', '30715496', '7550355', '29718187', '24078737', '3285207', '26828946', '20303757', '26247046', '31132363', '19631309', '9124799', '27066560', '857157', '14606043', '12566280', '16380615', '12136074', '11106718', '30679003', '23844677', '16924011', '23348830', '24500646', '28540413', '17928598', '23313956', '12666119', '9497244', '14512967', '29855340', '22242004', '19576565', '8308722', '26322222', '24838343', '7668821', '12966029', '30701273', '23329375', '26179919', '20083571', '1967823', '29498452', '27858739', '28881388', '11114175', '19251977', '10406984', '12062252', '2300206', '25476234', '8900232', '23543484', '19299310', '18852439', '8789455', '21665002', '28017374', '9585610', '9245996', '23933735', '17036286', '15907287', '23749797', '12499475', '8012388', '10053013', '28224639', '25182138', '27745833', '17430991', '14659406', '21288719', '9829275', '16793270', '16155110', '31955980', '17336526', '24011652', '22286171', '18551513', '30215711', '24610330', '26094573', '20598274', '1659668', '12937085', '25116801', '21984748', '30515627', '25512002', '18274675', '15111675', '18626973', '19085932', '21263134', '14681890', '12554688', '10489050', '26497905', '23188110', '31332381', '32077526', '23434117', '26561570', '15367920', '10588221', '20418530', '21965549', '8000914', '12654965', '8316268', '15894594', '16236538', '27816943', '14508709', '19559397', '31192305', '31796684', '27259757', '17525139', '20839240', '18179888', '23856421', '26553276', '23562820', '26700687', '34204919', '34193198', '34167565', '34151853', '34066362', '33977145', '33963534', '33926407', '33909041', '33860760', '33851717', '33772159', '33755597', '33742414', '33706403', '33693846', '33618039', '33558124', '33497766', '33458580', '33435938', '33396724', '33384202', '33382107', '33376055', '33333461', '33244741', '33190635', '33184643', '33176865', '33170376', '33138863', '32896939', '32862205', '32827036', '32819427', '32809972', '32805447', '32707087', '32684384', '32650001', '32642802', '32607581', '32607476', '32605089', '32578970', '32456280', '32453099', '32453097', '32420686', '32406602', '32403198', '32354746', '32333597', '32307885', '32266982', '32238315', '32222963', '32160286', '32081093', '32065942', '32053901', '31970803', '31953038', '31952901', '31897838', '31897643', '31844279', '31839742', '31794464', '31794073', '31769119', '31729100', '31696431', '31666547', '31666234', '31655143', '31628461', '31627234', '31623094', '31609695', '31578728', '31561939', '31540749', '31504392', '31472299', '31471117', '31455395', '31449669', '31448844', '31410651', '31378432', '31368648', '31360996', '31353864', '31352912', '31332964', '31255525', '31216357', '31211170', '31191425', '31133972', '31133047', '31107960', '31068177', '31060727', '31060726', '31060725', '31060723', '31060721', '31040037', '31034989', '31030121', '31024060', '30993714', '30987788', '30928807', '30908796', '30907627', '30893644', '30873576', '30846217', '30794915', '30791960', '30788618', '30761937', '30738493', '30732915', '30706156', '30689883', '30642739', '30631434', '30630514', '30626539', '30612914', '30601711', '30576443', '30569318', '30566586', '30553274', '30541163', '30496909', '30486920', '30451843', '30451841', '30414326', '30412272', '30406384', '30389963', '30377729', '30365001', '30358464', '30303820', '30291191', '30291184', '30243034', '30241883', '30232666', '30222053', '30200169', '30149909', '30145633', '30103348', '30091961', '30065953', '30061062', '30057997', '30025162', '30016436', '29950440', '29895224', '29882456', '29866061', '29763467', '29726018', '29691892', '29681083', '29669168', '29625576', '29614691', '29539587', '29506908', '29482508', '29478600', '29475025', '29474540', '29465610', '29457652', '29451848', '29445932', '29437916', '29419890', '29391587', '29358615', '29342313', '29328520', '29274205', '29225264', '29212896', '29203592', '29193480', '29187205', '29178655', '29178646', '29175898', '29172004', '29169929', '29152331', '29142168', '29141652', '29129153', '29125502', '29090468', '29067961', '29053704', '28984114', '28971531', '28927399', '28818390', '28818389', '28792153', '28780987', '28760337', '28755659', '28754454', '28744779', '28740838', '28733338', '28729373', '28729039', '28716623', '28714989', '28712002', '28685322', '28676641', '28659438', '28624463', '28622964', '28620495', '28554554', '28548023', '28543538', '28498977', '28478914', '28468212', '28456886', '28453295', '28427446', '28416349', '28357410', '28269794', '28269792', '28237839', '28182637', '28181274', '28125727', '28111795', '28102454', '28082118', '28012042', '28007904', '27976420', '27941137', '27939133', '27932089', '27922501', '27891585', '27882542', '27876398', '27876257', '27870637', '27861221', '27859369', '27854213', '27854204', '27818386', '27798538', '27709505', '27695855', '27683561', '27671536', '27671187', '27659899', '27656840', '27623444', '27618136', '27612189', '27601064', '27600705', '27576556', '27543038', '27538056', '27515125', '27476418', '27473021', '27464418', '27445241', '27443559', '27439679', '27430445', '27393415', '27389816', '27387980', '27376850', '27375477', '27357517', '27357428', '27293330', '27215641', '27193224', '27177998', '27159402', '27155155', '27150099', '27147698', '27134770', '27118449', '27114706', '27102768', '27067155', '27035234', '26995067', '26944597', '26927810', '26927351', '26906428', '26866830', '26844616', '26841830', '26825891', '26802438', '26799446', '26782017', '26782016', '26780752', '26754003', '29485812', '26600317', '26594870', '26583494', '26544689', '26526626', '26520282', '26458037', '26436962', '26418456', '26403434', '26383991', '26379183', '26374066', '26342832', '26338224', '27858741', '26310427', '26296490', '26292175', '26273216', '26255678', '26249246', '26242231', '26234161', '26221953', '26216333', '26204918', '26119801', '26114882', '26098624', '26086764', '26067811', '27858727', '26035394', '26019235', '26006750', '25960145', '25959956', '25958340', '25957634', '25953320', '25949787', '25913210', '25900305', '25891782', '25890230', '25888334', '25882082', '25867930', '25825463', '25821721', '25809233', '25796416', '25747004', '25740612', '25740301', '25728519', '25708584', '25664165', '25661902', '25633151', '25628744', '25609763', '25581576', '25576864', '25566070', '25552303', '28198706', '25541946', '25533456', '25521991', '25501959', '25496057', '25492887', '25477819', '25430424', '25387694', '25387602', '25359222', '25352051', '25326555', '25288803', '25264603', '25262827', '25256213', '25251739', '25239142', '25211533', '25208612', '25208129', '25205138', '25204870', '25187204', '25160016', '25149037', '25121381', '25112543', '25111228', '25088345', '25084811', '25079567', '25078247', '25070542', '25062264', '25023008', '24957499', '24950662', '24928145', '24922523', '24866459', '24828896', '24823402', '24801232', '24788569', '24727567', '24726641', '24725366', '24722334', '24710723', '24706162', '24668768', '24665292', '24642510', '24628803', '24621721', '24611677', '24604798', '24596691', '24581957', '24569376', '24563484', '24549043', '24534542', '24529507', '24508248', '24507666', '24461433', '24456932', '24447024', '24381816', '24361111', '24305446', '24282529', '24263034', '24262449', '24225367', '24223098', '24183756', '24166571', '24134684', '24095155', '24091937', '24084573', '24074500', '24056153', '24046450', '24039817', '24024685', '24021317', '24013109', '23995273', '23977274', '23975679', '23938146', '23938035', '23894444', '23886664', '23860144', '23831158', '23826317', '23800702', '23785461', '23768727', '23762716', '23762378', '23754947', '23743156', '23628358', '23622361', '23622358', '23622357', '23620652', '23617272', '23612654', '23605961', '23587761', '23584160', '23582336', '23572247', '23572184', '23559977', '23553484', '23489661', '23481446', '23480858', '23479141', '23478172', '23453626', '23447650', '23420653', '23394784', '23374900', '23346162', '23338057', '23326516', '23305948', '23288328', '23274062', '23247734', '23245554', '23238123', '23238117', '23235116', '23164031', '23146629', '23142638', '23127960', '23122659', '23071563', '23071445', '23013377', '22980765', '22975586', '22941215', '22924779', '22922256', '22832343', '22825594', '22818856', '22796417', '22789857', '22782513', '22752422', '22723986', '22645112', '22619057', '22613877', '22560515', '22549409', '22547147', '22519952', '22512666', '22499106', '22496423', '22491857', '22473935', '22426012', '22424738', '22411250', '22407809', '22407275', '22392505', '22391739', '22373837', '22366888', '22308874', '22264517', '22242131', '22240398', '22234203', '22226732', '22193842', '22175901', '22172424', '22172422', '22172419', '22172417', '22172416', '22166137', '22153990', '22131272', '22113158', '22106710', '22099478', '22097997', '22085395', '22075033', '22068590', '22067214', '22050238', '22040608', '22030266', '22016142', '22012042', '21978459', '21975507', '21953374', '21947198', '21922472', '21880499', '21798101', '21794876', '21743372', '21708040', '21697078', '21667723', '21625620', '21623381', '21575048', '21544567', '21514436', '21501304', '21496628', '21495178', '21488203', '21488057', '21441569', '21440438', '21314018', '21305017', '21281811', '21248746', '21221624', '21175599', '21165550', '21138615', '21131200', '21129556', '21104864', '21094870', '21062345', '21045422', '21037586', '20976668', '20951040', '20937510', '20927630', '20888934', '20858595', '20850316', '20837309', '20820001', '20817456', '20733148', '20726955', '20688638', '20682747', '20673532', '20655547', '20638880', '20638845', '20610128', '20583297', '20554445', '20547455', '20534754', '20477750', '20467841', '20451479', '20434914', '20431600', '20425232', '20422195', '20400459', '20385271', '20358311', '20349070', '20303224', '20229580', '20227276', '20215985', '20207543', '20205351', '20199207', '20191014', '20189564', '20186778', '20181480', '20051426', '20028211', '20004786', '19968489', '19953533', '19932620', '19932619', '19917824', '19842201', '19838523', '19767415', '19751976', '19736010', '19687455', '19679478', '19632331', '19562689', '19553116', '19547838', '19493611', '19449433', '19396839', '19352249', '19342235', '19330236', '19305075', '19303294', '19294599', '19242871', '19240046', '19232644', '19197364', '19181672', '19181094', '19181090', '19179078', '19133863', '19130742', '19087338', '19084976', '19084402', '19077043', '19072569', '19047562', '19021346', '19008569', '18976909', '18974559', '18947621', '18830929', '18824361', '18817572', '18808525', '18804929', '18796407', '18723302', '18720506', '18707767', '18698612', '18695058', '18658083', '18645206', '18595146', '18593008', '18588847', '18577042', '18574571', '18516331', '18513969', '18487519', '18477565', '18461503', '18394888', '18382475', '18378883', '18367042', '18366090', '18362356', '18351526', '18351524', '18219255', '18202836', '18162732', '18054693', '17991069', '18041051', '18035984', '18032955', '18006961', '17996907', '17966957', '17951086', '17949279', '17932957', '17873513', '17846275', '17785673', '17715269', '17683097', '17672374', '17638428', '17631035', '17621527', '17618867', '17594595', '17537630', '17522883', '17504518', '17483490', '17439981', '17420831', '17395506', '17394203', '17387733', '17376685', '17359409', '17355552', '17336067', '17311848', '17275590', '17272906', '17261181', '17251023', '17236770', '17215366', '17204937', '17187373', '17174499', '17134899', '17118657', '17055682', '17030669', '17017655', '17010933', '16977479', '16959509', '16935502', '16924620', '16917943', '16896922', '16877500', '16869957', '16866299', '16866298', '16847006', '16825283', '16788822', '16760117', '16717122', '16707840', '16650805', '16599279', '16566888', '16550934', '16545565', '16531417', '16531045', '16496270', '16487709', '16466458', '16413720', '16386759', '16300186', '16288675', '16267784', '16258658', '16258657', '16230791', '16227881', '16217076', '16205611', '16183658', '16168598', '16164199', '16138248', '16127134', '16122635', '16087062', '16084089', '16083162', '16042307', '16020312', '16018165', '15986226', '15926054', '15907289', '15887272', '15886997', '15884633', '15882279', '15880682', '15857933', '15843272', '15833425', '15829503', '15804049', '15792869', '15776320', '15730903', '15696781', '15694140', '15690374', '15607216', '15592729', '15591603', '15578095', '15572824', '15564039', '15564033', '15564032', '15546767', '15515520', '15500499', '15478675', '15452315', '15375664', '15353856', '15351017', '15328566', '15328561', '15322429', '15269486', '15221331', '15213246', '15213105', '15198127', '15168109', '15159505', '15136669', '15127309', '15113116', '15085358', '15072110', '15056993', '15038665', '15004883', '14984906', '14983659', '14972325', '14767196', '14732627', '14681888', '14678799', '14670767', '14659780', '14652796', '14652462', '14638363', '14581794', '14580671', '14568816', '14555844', '14555385', '14516314', '12950028', '12942324', '12933945', '12899872', '12875918', '12875448', '12874727', '12861592', '12849864', '12810058', '12804980', '12788039', '12776231', '12757935', '12757359', '12746480', '12736748', '12734542', '12731651', '12715073', '12707973', '12707425', '12690567', '12666124', '12664320', '12661054', '12615171', '12609503', '12601554', '12597091', '12596670', '12596095', '12585716', '12565913', '12564770', '12552556', '12536036', '12536029', '12484565', '12467753', '12467733', '12467726', '12439276', '12409692', '12391344', '12384936', '12365725', '12364941', '12354792', '12351999', '12224470', '12219993', '12207929', '12184464', '12172906', '12138997', '12100373', '12075940', '12057917', '12045563', '12044978', '12031620', '12011280', '11989852', '11950173', '11929189', '11889243', '11870695', '11868073', '11865138', '11860576', '11853349', '11810649', '11798250', '11793470', '11785725', '11751021', '11745945', '11738352', '11695929', '11721063', '11684866', '11589167', '11584042', '11572559', '11571700', '11535231', '11525887', '11525882', '11516613', '11511285', '11504599', '11455396', '11445638', '11418917', '11404123', '11400038', '11381429', '11373316', '11369186', '11303796', '11298373', '11284094', '11248459', '11248458', '11234561', '11195880', '11176995', '11166164', '11166159', '10751809', '11150980', '11123059', '11113224', '11111063', '11071142', '11062006', '11059046', '11053680', '11053679', '11052230', '11045673', '10991996', '10980312', '10924019', '10912916', '10852541', '10838253', '10819959', '10817896', '10817489', '10817032', '10814897', '10762169', '10757473', '10738921', '10724100', '10716265', '10677859', '10707847', '10679036', '10677931', '10694916', '10679962', '10665485', '10651710', '10619716', '10611118', '10577539', '10567819', '10563745', '10549748', '10545049', '10545042', '10513918', '10513694', '10463422', '10454718', '10449659', '10401692', '10399753', '10367979', '10342114', '10329008', '10328285', '10222459', '10222457', '10220864', '10220863', '10211476', '10090674', '10073437', '10073429', '10029346', '10029257', '10025426', '9932958', '9863772', '9857334', '9845296', '9845295', '9840670', '9829280', '9829276', '9788720', '9784647', '9773408', '9763366', '9748045', '9736139', '9720690', '9708547', '9705139', '9686113', '9674785', '9673904', '9638664', '9637197', '9631397', '9631396', '9623038', '9610800', '9600602', '9596013', '9578083', '9577404', '9553297', '9545182', '9545174', '9544647', '9494506', '9492098', '9484391', '9372751', '9400354', '9327401', '9335006', '9307259', '9217218', '9309713', '9309712', '9284193', '9279561', '9270600', '9255393', '9255383', '9171324', '9990278', '9297932', '9253491', '9228495', '9197935', '9185183', '9185176', '9140362', '29512574', '9134386', '9120013', '9135384', '9131648', '9060511', '9042799', '9147066', '9029066', '9484111', '9401107', '9132136', '9071488', '9044410', '9044400', '9039665', '9050048', '9018440', '8985523', '9120218', '8957020', '8952026', '8911899', '8938702', '8930628', '8916167', '8891240', '8888050', '8678932', '8891365', '8887951', '9025864', '8879654', '8878749', '8858709', '8811133', '8807418', '8795848', '8651294', '8806123', '8740702', '8737802', '8628482', '8626895', '8618556', '8596321', '8737730', '8733905', '8618689', '8618688', '9064005', '8741142', '8677029', '8929621', '8928608', '8907344', '8866747', '8856367', '8778704', '8745640', '8588581', '8881867', '8592933', '8576559', '7484683', '8556730', '8548596', '8540815', '8532627', '7561954', '7669390', '7726155', '7633188', '7628166', '7546014', '7706500', '7619191', '7608737', '7773974', '7767098', '7751841', '7606895', '7791947', '8615088', '7722535', '7671985', '7582253', '7547371', '7489436', '7981596', '8060426', '7522681', '8203265', '8170489', '8137223', '8048705', '8048703', '8012191', '8008690', '8114781', '8155933', '8281152', '8249887', '8246011', '7506396', '8247961', '8220948', '8339500', '8284954', '8198769', '8112970', '8403631', '8268726', '8370146', '8240757', '8478760', '8469351', '8444256', '8372669', '7682901', '8461680', '7678595', '8467839', '8460531', '8382571', '8320867', '8307068', '8256590', '1469246', '1456390', '1641160', '1524518', '1388418', '1602315', '1517767', '1374141', '1588016', '1314327', '1637141', '1739302', '1565211', '1552307', '1732764', '1575014', '1513553', '1483054', '1483042', '1407518', '1302142', '1300189', '1686882', '1810161', '1684789', '1922177', '1875518', '1795174', '1785661', '1915449', '1757069', '1930423', '1875028', '1915507', '1957653', '1957651', '1957650', '1957649', '1867258', '1993504', '2044633', '2029290', '2011653', '1892223', '1822780', '1745328', '1648255', '2268764', '1982682', '2284944', '2231701', '2243226', '2213842', '2192302', '2320042', '2324771', '2314559', '2168251', '2295510', '2240464', '2178616', '2092587', '2694131', '2809005', '2604802', '2768783', '2743290', '2725162', '2789739', '2721043', '2709065', '2927021', '2495176', '2759146', '2757601', '2751061', '2712935', '2683560', '2605873', '2540284', '2538089', '2492399', '3249100', '3062133', '3215750', '3065597', '3072008', '3398881', '3390091', '2897824', '3356991', '3356987', '3342545', '3277050', '3251214', '3202738', '3438055', '3666331', '3662706', '3309721', '2821096', '3680647', '3674107', '3673497', '3673494', '3655841', '3610132', '3317765', '3110216', '3575207', '3574691', '3300000', '3585421', '3105522', '3808314', '3470161', '3816882', '3661912', '3605541', '3323392', '3120403', '2451237', '3789054', '3801309', '3491356', '2947254', '3811138', '3808228', '3790384', '3027606', '3508701', '3785883', '3746364', '2426945', '3508696', '3724791', '3723551', '3754424', '3948960', '3753853', '3964144', '3825514', '3799922', '3799921', '3799143', '3766905', '3766904', '3541664', '3460017', '4075080', '4062619', '4055149', '3840649', '4056819', '4030877', '4022386', '2995591', '4030477', '4047349', '3162002', '2854735', '16758596', '16758595', '3978935', '3978931', '2857418', '3981176', '4083385', '3976131', '3970066', '6542063', '6524876', '6095966', '6490995', '6478837', '6094728', '6465204', '6736237', '6730202', '6542524', '6512576', '6496876', '6481414', '6143441', '6091488', '6662143', '6657012', '6577313', '6196637', '6615293', '6636137', '6616347', '6312355', '6687271', '6222163', '6885394', '6870590', '6855798', '6832496', '6879213', '6851300', '6846734', '6842261', '6837268', '6659868', '6650144', '6638396', '6318501', '6315292', '7161420', '7131136', '6296713', '6182741', '7202042', '7069529', '7088021', '7081292', '6461828', '7198731', '7168482', '7158301', '7057203', '6976525', '6302497', '6301720', '7302753', '7299413', '6213881', '7290342', '7286967', '7271044', '7229670', '6267501', '6454877', '7464208', '7207500', '7330669', '6939261', '6789696', '6781906', '6291305', '6271433', '6783595', '7436809', '7431176', '6448277', '7411166', '6997732', '7381515', '6893737', '6247453', '7391631', '6929572', '7354521', '7468147', '7435878', '7435873', '7224095', '392333', '507896', '525348', '497805', '492211', '224846', '516715', '397413', '758421', '551739', '153649', '685892', '213746', '150456', '677209', '739346', '656159', '654876', '77319', '580714', '75955', '604494', '588085', '579444', '579291', '410751', '72134', '193343', '557754', '189737', '872842', '868503', '991722', '988511', '977449', '184767', '135884', '131568', '963533', '55468', '1070214', '962588', '175135', '175134', '55105', '130467', '1195490', '51920', '1242211', '1150706', '1233667', '1138529', '1132187', '4125962', '4714102']

    def run(self):
        # TODO: Method populate Article
        # super().check_or_create_db()
        # self.article_per_keyword()
        # # self.process_article_data_mgt()
        # # self.process_article_data_pubmed()
        # removal_false_positive()
        # get_pubtator_annotation()

        self.keyword_disease_gene()
        # # self.intersection()
        # self.ps_spacy_frequency()
        # self.ps_wordcloud()
        # self.negative_set()
        # self.pmids_histology()


if __name__ == '__main__':
    print('start')
    p = AllArticle('article')
    p.run()
    print('end')
