from Bio import Entrez
from peewee import *

from textmining_mc.resources.model import Article, ArticleDataset
from textmining_mc.resources.utils.superbasemodel import DatabaseModel


class API(object):

    def __init__(self, pmids_list, article_for_insert_many, dataset_id, pmids_dataset, avaibility_check=None):
        self.pmids_list = pmids_list
        self.dataset_id = dataset_id
        self.pmids_dataset = pmids_dataset
        self.avaibility_check = avaibility_check if avaibility_check is not None else 'no'
        self.records = dict()
        self.article_for_insert_many = article_for_insert_many
        self.efetch()
        self.removal_not_available()
        self.removal_pubmedbookarticle()
        self.article_xml_content()

    def efetch(self):
        """
        Efetch,

        :param pmids_list: List of 100 pmids
        :return:
        """
        Entrez.email = "hugues.escoffier@etu.unsitra.fr"
        handle = Entrez.efetch(db="pubmed", id=self.pmids_list, retmode="xml", rettype="abstract")
        records = Entrez.read(handle)
        self.records = records

    def removal_pubmedbookarticle(self):
        """
        Deletes 'PubmedBookArticles' in the query

        :param pmids_list: List of 100 pmids
        :return: list_id_100: Without pmids of PubmedBookArticles
        """
        data = self.records["PubmedArticle"]
        if len(data) != len(self.pmids_list):
            for i in range(len(self.pmids_list) - len(data)):
                id_unwanted = ''.join(self.records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
                self.pmids_list.remove(id_unwanted)
        return self.pmids_list

    def removal_not_available(self):
        """
        Delete ids of articles that are no longer available

        :return: list_id_100: Without pmids of articles no longer available
        """
        if self.avaibility_check == 'yes':
            ok = 'No'
            while ok == 'No':
                c = 0
                for i in range(len(self.pmids_list)):
                    if self.records["PubmedArticle"][i]["MedlineCitation"]["PMID"] != str(self.pmids_list[i]):
                        self.pmids_list.remove(self.pmids_list[i])
                        break
                    else:
                        c += 1
                if c == len(self.pmids_list):
                    ok = "Yes"

    def article_xml_content(self):
        """
        Recovery of the data contained in the article :
            > Title
            > Publication Type
            > Publication Date
            > Abstract

        :param records:
        :param list_id_100: List of 100 pmids
        :return:
        """
        for i in range(len(self.pmids_list)):
            title = ''.join(self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
            publication_type_list = self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"]
            if len(publication_type_list) != 1:
                z = 0
                for y in range(len(publication_type_list)):
                    if ''.join(self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][
                                   y]) == "Journal Article":
                        publication_type = "Journal Article"
                        z = 1
                if z == 0:
                    publication_type = "Other"
            else:
                publication_type = ''.join(
                    self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
            try:
                abstract = ''.join(
                    self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
            except:
                abstract = "None"

            try:
                date = ''.join(
                    self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"][
                        "Year"])
            except:
                try:
                    date = ''.join(
                        self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
                except:
                    complete_date_ = ''.join(
                        self.records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"][
                            "PubDate"]["MedlineDate"])
                    date = ''
                    c = 0
                    for lettre in complete_date_:
                        if c == 4:
                            break
                        date = date + lettre
                        c += 1
            if publication_type == 'Journal Article' and abstract != 'None' and date != 'Wint' and date != 'Summ' and date != 'Spri' and date != 'Fall':
                self.article_for_insert_many.append((self.pmids_list[i], title, date, publication_type, abstract))
                self.pmids_dataset.append((self.pmids_list[i], self.dataset_id))






