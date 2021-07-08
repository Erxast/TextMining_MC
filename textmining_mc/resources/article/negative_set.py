import requests
import random

from Bio import Entrez
from tqdm import tqdm
from textmining_mc.resources.model import Article, NArticle, AllAnnotation, NAnnotation
from textmining_mc.resources.utils import database

""" 
Problème avec la connection au proxy de la banque Article. 

"""


class NegativeSet(object):
    def __init__(self):
        self.list_all = []

    def count_years(self):
        i = 0
        c = 0
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
                self.list_all.append([date_av, i])
                date_i = date_i2
                date_av = arti.date
                if c == (len(query) - 1):
                    self.list_all.append([arti.date, i])
            else:
                date_i = date_i2
                self.list_all.append([date_av, i])
                date_av = arti.date
                i = 1
            c += 1
        print('count_years_end')

    def selection_article(self):
        list_article_per_y = []
        for T in self.list_all:
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
                            tuple_article = (random_id_all[i], title_, date_, publication_type_, abstract_, 'pubmed')
                            list_article_per_y.append(tuple_article)
                            compteur_article_annee += 1
                        if compteur_article_annee == 1000:
                            NArticle.insert_many(list_article_per_y,
                                                 fields=[NArticle.id, NArticle.title, NArticle.date, NArticle.type,
                                                         NArticle.abstract, NArticle.source])
                            list_article_per_y.clear()
                            OK = 'True'
                            break
        print('selection_article_end')

    @staticmethod
    def annotation_article():
        """
        Annotate all articles via Pubtator annotations
        :return:
        """
        count = 0
        list_article_id = []
        list_annotation = []
        query = Article.select()
        for article in query:
            list_article_id.append(str(article.id))
        # for art_id in tqdm(iterable=list_article_id, desc='annotation'):
        print('ok')
        for annot in AllAnnotation.select().where(AllAnnotation.id.in_(list_article_id)):
            pmid = annot.id
            mention = annot.mention
            bioconcept = annot.bioconcept
            identifier = annot.identifier
            tuple_annot = (pmid, mention, bioconcept, identifier)
            list_annotation.append(tuple_annot)
            count += 1
            if count == 10000:
                print('insert')
                NAnnotation.insert_many(list_annotation,
                                        fields=[NAnnotation.pmid, NAnnotation.mention, NAnnotation.bioconcept,
                                                NAnnotation.identifier]).execute()
                list_annotation.clear()
                count = 0
        NAnnotation.insert_many(list_annotation, fields=[NAnnotation.pmid, NAnnotation.mention, NAnnotation.bioconcept,
                                                         NAnnotation.identifier]).execute()

    def run(self):
        self.count_years()
        self.selection_article()
        self.annotation_article()


if __name__ == '__main__':
    print('start')
    NegativeSet().run()
    print('end')
