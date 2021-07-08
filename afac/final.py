import requests
from Bio.motifs.jaspar import db
from tqdm import tqdm
from Bio import Entrez
from peewee import *

from textmining_mc.resources.model import Article


def api_pubmed_database():
###############################################################################################################################################
    # Request_for_QK_&_WE
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]&retmode=json&usehistory=y')
    # print(rob.status_code)
    query_key = rob.json()['esearchresult']['querykey']
    web_env = rob.json()['esearchresult']['webenv']
    # print('query_key=', query_key)
    # print('web_env=', web_env)
    # Request_for_list_of_ID
    urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
        query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json"
    rsearch = requests.get(urlsearch)
    # Declaration_V
    id_all = rsearch.json()['esearchresult']['idlist']
###############################################################################################################################################
    list_id_100 = []
#####################################################################################################################
    for elmt in tqdm(iterable=id_all, desc='creation_'):
        if len(list_id_100) == 100:
            Entrez.email = "hugues.escoffier@etu.unsitra.fr"
            handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
            records = Entrez.read(handle)
            print(records)
##################################################################################################################################
            data_ = records["PubmedArticle"]
            if len(data_) != len(list_id_100):
                for i in range(len(list_id_100) - len(data_)):
                    Id_unwanted = ''.join(records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
                    list_id_100.remove(Id_unwanted)
##################################################################################################################################
            for i in range(len(list_id_100)):
                try:
                    abstract_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
                except:
                    abstract_ = "None"
                title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
                publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"]
                if len(publication_type_list) != 1:
                    z = 0
                    for y in range(len(publication_type_list)):
                        if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][y]) == "Journal Article":
                            publication_type_ = "Journal Article"
                            z = 1
                    if z == 0:
                        publication_type_ = "Other"
                else:
                    publication_type_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
                try:
                    date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"])
                except:
                    try:
                        date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
                    except:
                        complete_date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"])
                        date_ = ''
                        c = 0
                        for lettre in complete_date_:
                            if c == 4:
                                break
                            date_ = date_ + lettre
                            c += 1
                #Add_to_db
                article = Article.create(id=list_id_100[i], title=title_, date=date_, type=publication_type_, abstract=abstract_)
###############################################################################################################################################
            list_id_100.clear()
            list_id_100.append(elmt)

        else:
            list_id_100.append(elmt)

    #Treatment_last_A
    for i in range(len(list_id_100)):
        Entrez.email = "hugues.escoffier@etu.unsitra.fr"
        handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
        records = Entrez.read(handle)
########################################################################################################
        data_ = records["PubmedArticle"]
        if len(data_) != len(list_id_100):
            for i in range(len(list_id_100) - len(data_)):
                Id_unwanted = ''.join(records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
                list_id_100.remove(Id_unwanted)
        try:
           abstract_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
        except:
            abstract_ = "None"
            # print(list_id_50[i])
        title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
        publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"]
        if len(publication_type_list) != 1:
            z = 0
            for y in range(len(publication_type_list)):
                if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][y]) == "Journal Article":
                    publication_type_ = "Journal Article"
                    z = 1
            if z == 0:
                publication_type_ = "Other"
        else:
            publication_type_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
        try:
            date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"])
        except:
            try:
                date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
            except:
                complete_date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"])
                date_ = ''
                c = 0
                for lettre in complete_date_:
                    if c == 4:
                        break
                    date_ = date_ + lettre
                    c += 1
        #Add_to_db
        article = Article.create(id=list_id_100[i], title=title_, date=date_, type=publication_type_, abstract=abstract_)
#     #Del_false_positive
    for arti in Article.select():
        if arti.abstract == "None":
            arti.delete_instance()
        elif arti.type != "Journal Article":
            arti.delete_instance()
    db.close()


api_pubmed_database()

#
# def api_mgt_database():
#     fichier = open("List_id_MGT.txt", 'r')
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
#     # # Database_C
#     # db = SqliteDatabase('article_mgt1.db')
#     #
#     # class Article(Model):
#     #     id = CharField()
#     #     title = CharField()
#     #     date = CharField()
#     #     type = CharField()
#     #     abstract = CharField()
#     #
#     #     class Meta:
#     #         database = db
#     #
#     # db.create_tables([Article])
#
#     list_id_100 = []
#     str_id_100 = str()
#     for elmt in tqdm(iterable=list_mgt_final, desc='creation_'):
#         if len(list_id_100) == 100:
#             ####################################################################################################
#             Entrez.email = "hugues.escoffier@etu.unsitra.fr"
#             handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
#             records = Entrez.read(handle)
#             ####################################################################################################
#             # ok = 0
#             # while ok == 0:
#             #     c = 0
#             #     for i in range(len(list_id_100)):
#             #         # print(i)
#             #         # print("Article ID: ", id_list[i])
#             #         if records["PubmedArticle"][i]["MedlineCitation"]["PMID"] != list_id_100[i]:
#             #             list_id_100.remove(list_id_100[i])
#             #             break
#             #         else:
#             #             c += 1
#             #     if c == len(list_id_100):
#             #         ok = 1
#             # récupération des données d'un articles
#             ####################################################################################################
#             # for i in range(len(list_id_100)):
#             #     try:
#             #         abstract_ = ''.join(
#             #             records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
#             #     except:
#             #         abstract_ = "None"
#             #
#             #     title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
#             #     publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"]
#             #     if len(publication_type_list) != 1:
#             #         z = 0
#             #         for y in range(len(publication_type_list)):
#             #             if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][
#             #                            y]) == "Journal Article":
#             #                 publication_type_ = "Journal Article"
#             #                 z = 1
#             #         if z == 0:
#             #             publication_type_ = "Other"
#             #     else:
#             #         publication_type_ = ''.join(
#             #             records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
#             #     try:
#             #         date_ = ''.join(
#             #             records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"][
#             #                 "Year"])
#             #     except:
#             #         try:
#             #             date_ = ''.join(
#             #                 records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
#             #         except:
#             #             complete_date_ = ''.join(
#             #                 records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"][
#             #                     "PubDate"]["MedlineDate"])
#             #             date_ = ''
#             #             c = 0
#             #             for lettre in complete_date_:
#             #                 if c == 4:
#             #                     break
#             #                 date_ = date_ + lettre
#             #                 c += 1
#             ####################################################################################################
#                 # Add_to_db
#                 article = Article.create(id=list_id_100[i], title=title_, date=date_, type=publication_type_,
#                                          abstract=abstract_)
#             list_id_100.clear()
#             list_id_100.append(elmt)
#             str_id_100 = str(elmt)
#
#         else:
#             list_id_100.append(elmt)
#             str_id_100 = str_id_100 + str(elmt)
#
#     # Treatment_last_A
#     for i in range(len(list_id_100)):
#         Entrez.email = "hugues.escoffier@etu.unsitra.fr"
#         handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
#         records = Entrez.read(handle)
#         ####################################################################################################
#         ok = 0
#         while ok == 0:
#             c = 0
#             for i in range(len(list_id_100)):
#                 # print(i)
#                 # print("Article ID: ", id_list[i])
#                 if records["PubmedArticle"][i]["MedlineCitation"]["PMID"] != list_id_100[i]:
#                      list_id_100.remove(list_id_100[i])
#                      break
#                 else:
#                     c += 1
#             if c == len(list_id_100):
#                 ok = 1
#     # Same recuperation
#     for i in range(len(list_id_100)):
#         Entrez.email = "hugues.escoffier@etu.unsitra.fr"
#         handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
#         records = Entrez.read(handle)
#         ####################################################################################################
#         try:
#             abstract_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
#         except:
#             abstract_ = "None"
#             # print(list_id_50[i])
#         title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
#         publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"]
#         if len(publication_type_list) != 1:
#             z = 0
#             for y in range(len(publication_type_list)):
#                 if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][
#                                y]) == "Journal Article":
#                     publication_type_ = "Journal Article"
#                     z = 1
#             if z == 0:
#                 publication_type_ = "Other"
#         else:
#             publication_type_ = ''.join(
#                 records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
#         try:
#             date_ = ''.join(
#                 records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"])
#         except:
#             try:
#                 date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
#             except:
#                 complete_date_ = ''.join(
#                     records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"][
#                         "MedlineDate"])
#                 date_ = ''
#                 c = 0
#                 for lettre in complete_date_:
#                     if c == 4:
#                         break
#                     date_ = date_ + lettre
#                     c += 1
#         # Add_to_db
#         ####################################################################################################
#         article = Article.create(id=list_id_100[i], title=title_, date=date_, type=publication_type_,
#                                  abstract=abstract_)
#         #Del_false_positive
#         ####################################################################################################
#     for arti in Article.select():
#         if arti.abstract == "None":
#             arti.delete_instance()
#         elif arti.type != "Journal Article":
#             arti.delete_instance()
#     db.close()
#
#
# # api_mgt_database()

db = SqliteDatabase('all_pubtator.db')


class Annotation(Model):
    id = CharField()
    bioconcept = CharField()
    mention = CharField()
    identifier = CharField()

    class Meta:
        database = db


def db_pubtator():
    all_l = []
    db.create_tables([Annotation])
    with open("gene2pubtatorcentral.txt", 'r') as fin:
        for line in tqdm(iterable=fin, desc='reading'):
            cols = line.strip('\n').split('\t')
            a = (cols[0], cols[1], cols[2], cols[3])
            all_l.append(a)
            if len(all_l) == 998:
                Annotation.insert_many(all_l, fields=[Annotation.id, Annotation.bioconcept, Annotation.identifier,
                                                      Annotation.mention]).execute()
                all_l.clear()
    # Annotation.insert_many(all_l, fields=[Annotation.id, Annotation.bioconcept, Annotation.identifier,
    #                                       Annotation.mention]).execute()
    db.close()


db_pubtator()


