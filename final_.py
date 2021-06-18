import requests
import os
from tqdm import tqdm
from Bio import Entrez


def api_pubmed_():
    # Request_for_QK_&_WE
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]&retmode=json&usehistory=y')
    # print(rob.status_code)
    all_rob = rob.json()
    query_key = rob.json()['esearchresult']['querykey']
    web_env = rob.json()['esearchresult']['webenv']
    print('query_key=', query_key)
    print('web_env=', web_env)
    # Request_for_list_of_ID
    urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
        query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json"
    rsearch = requests.get(urlsearch)
    # Declaration_V
    id_all = rsearch.json()['esearchresult']['idlist']
    list_id_100 = []
    str_id_100 = str()
    # Create_path
    dir = "Art_per"
    parent_dir = "/Users/hugues.escoffier/PycharmProjects/TextMining_MC"
    path = os.path.join(parent_dir, dir)
    try:
        os.mkdir(path)
    except:
        print("Already_C")
    for elmt in tqdm(iterable=id_all, desc='creation_'):
        if len(list_id_100) == 100:
            Entrez.email = "hugues.escoffier@etu.unsitra.fr"
            handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
            records = Entrez.read(handle)
            data_ = records["PubmedArticle"]
            if len(data_) != len(list_id_100):
                for i in range(len(list_id_100) - len(data_)):
                    Id_unwanted = ''.join(records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
                    list_id_100.remove(Id_unwanted)
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
                        date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"])
                with open(path + "/article " + str(list_id_100[i]), "a+") as file:
                    file.write("Title : " + str(title_) + "\n")
                    file.write("Date : " + str(date_) + "\n")
                    file.write("Publication_type : " + str(publication_type_) + "\n")
                    file.write("Abstract : " + str(abstract_) + "\n")
                    file.close()
                if abstract_ == "None":
                    os.remove(path + "/article " + str(list_id_100[i]))
                if publication_type_ != "Journal Article":
                    try:
                        os.remove(path + "/article " + str(list_id_100[i]))
                    except:
                        a = 0
            list_id_100.clear()
            list_id_100.append(elmt)
            str_id_100 = str(elmt)
        else:
            list_id_100.append(elmt)
            str_id_100 = str_id_100 + str(elmt)
    for i in range(len(list_id_100)):
        Entrez.email = "hugues.escoffier@etu.unsitra.fr"
        handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
        records = Entrez.read(handle)
        data_ = records["PubmedArticle"]
        if len(data_) != len(list_id_100):
            for i in range(len(list_id_100) - len(data_)):
                Id_unwanted = ''.join(records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
                list_id_100.remove(Id_unwanted)
        for i in range(len(list_id_100)):
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
                    date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"])
            with open(path + "/article " + str(list_id_100[i]), "a+") as file:
                file.write("Title : " + str(title_) + "\n")
                file.write("Date : " + str(date_) + "\n")
                file.write("Publication_type : " + str(publication_type_) + "\n")
                file.write("Abstract : " + str(abstract_) + "\n")
                file.close()
            if abstract_ == "None":
                os.remove(path + "/article " + str(list_id_100[i]))
            if publication_type_ != "Journal Article":
                try:
                    os.remove(path + "/article " + str(list_id_100[i]))
                except:
                    a = 0


api_pubmed_()
