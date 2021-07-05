import sys
import sqlite3
import requests
import spacy
import xmltodict
import os
from tqdm import tqdm
from Bio import Entrez
from peewee import *
import random
from pprint import pprint
import collections


def api_pubmed():
    # Request_for_QK_&_WE
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=congenital+myopathy&retmode=json&usehistory=y')
    # print(rob.status_code)
    query_key = rob.json()['esearchresult']['querykey']
    web_env = rob.json()['esearchresult']['webenv']
    print('query_key=', query_key)
    print('web_env=', web_env)
    # Request_for_list_of_ID
    urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
        query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json"
    rsearch = requests.get(urlsearch)
    # print(rsearch.status_code)
    # print(urlsearch)
    id_all = rsearch.json()['esearchresult']['idlist']
    # print(len(id_all)) = 9247
    # id_all_art = []
    # for she in id_all:
    #     url_art = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=" + str(she) +"&retmode=json"
    #     rart = requests.get(url_art)
    #     print(rart.status_code)
    #     verif_art = rart.json()['result'][str(she)]['pubtype']
    #     print(verif_art)
    #     if verif_art == ['Journal Article']:
    #         id_all_art.append(she)
    # print(id_all_art)
    # print(len(id_all_art)) = 7296
    dir = "Article_"
    parent_dir = "/"
    path = os.path.join(parent_dir, dir)
    try:
        os.mkdir(path)
    except:
        print("Already_C")
    list_id_50 = []
    str_id_50 = str()
    number_file = 1
    for elmt in tqdm(iterable=id_all, desc='download_xml'):
        if len(list_id_50) == 50:
            print(list_id_50)
            # print(str_id_50)
            urlfetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+str(str_id_50)+"&retmode=xml"
            # print(urlfetch)
            all1_art = requests.get(urlfetch)
            dict_all1_art = xmltodict.parse(all1_art.content)
            # arti_cle = open(path + "/article " + str(number_file), "w+")
            # arti_cle.write(str(dict_all1_art))
            # arti_cle.close()
            list_id_50.clear()
            list_id_50.append(elmt)
            str_id_50 = str(elmt) + ","
            number_file += 1
        else:
            list_id_50.append(elmt)
            str_id_50 = str_id_50 + str(elmt) + ","
    urlfetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+str(str_id_50)+"&retmode=xml"
    # print(urlfetch)
    all1_art = requests.get(urlfetch)
    dict_all1_art = xmltodict.parse(all1_art.content)
    # arti_cle = open(path + "/article " + str(number_file), "w+")
    # arti_cle.write(str(dict_all1_art))
    # arti_cle.close()


def work():
    # url_ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=33602879,33811133&retmode=xml"
    url_ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34129875,34120822,34117073,34112090,34106991,34103343,34087854,34068508,34066362,34066119,34058744,34053846,20301480,34033812,33994094,33985321,33977145,33972922,33964023,33963534,33940562,33940157,33933294,33926564,33926407,33923914,33922911,33919826,33917608,33916195,33909041,33898094,33889622,33869891,33860760,33851717,33849607,33811133,33808002,33799993,33775046,33772159,33768912,33762497,33755597,33750322,33748842,33742414,33740643,33731536,33728321,33715228,33713125,33706403,33694278,33693846,33678976,33672664,33671084,33667896,33660968,33659639,33658649,33655926,33649036,33646172,33644647,33642296,33622753,33618039,33610554,33605127,33604899,33602879,33596003,33569209,33558124,33547108,33539007,33530378,33529318,33522658,33513091,33497766,33478553,33476211,33459893,33458580,33458578,33454021,33449170,33441455,33435938,33410539,33407688,33397769,33397003,33396724,33389762,33384202,&retmode=xml"
    url__ = requests.get(url_)
    data_ = xmltodict.parse(url__.content)
    # print(data_)
    PubmedArticle = data_["PubmedArticleSet"]["PubmedArticle"]
    dir = "Art_per"
    parent_dir = "/"
    path = os.path.join(parent_dir, dir)
    try:
        os.mkdir(path)
    except:
        print("Already_C")
    potential_err_pub = ""
    potential_err_abs = ""
    potential_err_dat = ""
    date_art = ""
    abstract_art = ""
    for inf_ in PubmedArticle:
        try:
            id_art_one = inf_["MedlineCitation"]["PMID"]["#text"]
        except:
            try:
                id_art_one = inf_["MedlineCitation"]["PMID"]
            except :
                id_art_one = "None"
        try:
            title_art = inf_["MedlineCitation"]["Article"]["ArticleTitle"]["#text"]
        except:
            try:
                title_art = inf_["MedlineCitation"]["Article"]["ArticleTitle"]
            except:
                title_art = "None"
        for abs_tract in inf_["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]:
                abs_part = abs_tract["#text"]
                abstract_art = abstract_art + abs_part + "\n"
            # TypeError: string indices must be integers
        try:
            date_art = inf_["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]
        except:
            x = 0
        if date_art == "":
            date_art = "None"
        try:
            publication_type_art = inf_["MedlineCitation"]["Article"]["PublicationTypeList"]["PublicationType"]["#text"]
        except:
            try:
                for pub_lication in inf_["MedlineCitation"]["Article"]["PublicationTypeList"]["PublicationType"]:
                    publication_type_art = pub_lication["#text"]
                    break
            except:
                publication_type_art = "None"
        if publication_type_art == "None":
            potential_err_pub = "ERROR PUB "
        if abstract_art == "None":
            potential_err_abs = "ERROR ABS "
        if date_art == "None":
            potential_err_dat = "ERROR DAT "
        with open(path + "/article " + potential_err_abs + potential_err_pub + potential_err_dat + str(id_art_one), "a+") as file:
            file.write("Title : " + str(title_art) + "\n")
            file.write("Date : " + str(date_art) + "\n")
            file.write("Publication_type : " + str(publication_type_art) + "\n")
            file.write("Abstract : " + str(abstract_art) + "\n")
            file.close()


def solution_by_corentin():
    Entrez.email = "hugues.escoffier@etu.unsitra.fr"
    # id_list = ['1310898', '11294660', '15668982', '25476234', '10902626', '20920668', '24726473', '23261301', '15466643', '9536092', '8900232', '17592081', '15455396', '11774073', '20039086', '23543484', '1970420', '7910982', '26385635', '32937143', '29379881', '24268661', '19299310', '16701995', '15322983', '10590411', '18852439', '18313022', '10841809', '9382102', '16216943', '9326939', '16407510', '8789442', '12705874', '12196656', '9537420', '8789455', '21665002', '28017374', '18304497', '10330430', '15542288', '12531876', '9585610', '11528383', '14567970', '12571597', '15178757']
    # id_list = ['32991557', '32991555', '32900739']
    id_list = ['31217819', '15121789', '19122038', '26945885']
    handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml", rettype="abstract")
    records = Entrez.read(handle)
    for i in range(len(id_list)):
        print("Article ID: ", id_list[i])
        # try:
            # abstract_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
        # except:
            # print(id_list[i])
        title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
        publication_type_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
        # pprint(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"])
        print(title_)
        print(publication_type_)
        # print(abstract_)


# solution_by_corentin()


def e_summary():
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=congenital+myopathy&retmode=json&usehistory=y')
    # print(rob.status_code)
    query_key = rob.json()['esearchresult']['querykey']
    web_env = rob.json()['esearchresult']['webenv']
    # print('query_key=', query_key)
    # print('web_env=', web_env)
    # Request_for_list_of_ID
    urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
        query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json"
    rsearch = requests.get(urlsearch)
    # print(rsearch.status_code)
    # print(urlsearch)
    id_all = rsearch.json()['esearchresult']['idlist']
    # print(len(id_all)) = 9247
    Entrez.email = "hugues.escoffier@etu.unistra.fr"
    for i in id_all:
        handle_s = Entrez.esummary(db='pubmed', id=i, retmod='xml')
        records_s = Entrez.parse(handle_s)
        for record in records_s:
            print(record['Title'])
            print(record['Id'])
            print(record['PubTypeList'])
            print(record['PubDate'])
        handle_s.close()
        break


def final_():
    # Request_for_QK_&_WE
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]&retmode=json&usehistory=y')
    # print(rob.status_code)
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
    parent_dir = "/"
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


# final_()


def url_generator():
    url_str = ""
    # url_list = ['33277141', '31060720', '297409383', '27519468', '21073836', '12689691', '11801394', '10665483', '10553983', '8446135']
    # url_list = ['33909041', '33731536', '27519468', '22172415', '21073836', '12689691', '11801394', '10665483', '10553983', '8446135']
    url_list = ['18463901', '25113787', '8361506', '14985381']
    for elmt in url_list:
        url_str = url_str + elmt + ","
    url_ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+url_str+"&retmode=xml"
    print(url_)


# url_generator()


def test_():
    Entrez.email = "hugues.escoffier@etu.unistra.fr"
    id_list = ['34129875', '34120822', '34117073', '34112090', '34106991', '34103343', '34087854', '34068508', '34066362', '34066119', '34058744', '34053846', '20301480', '34033812', '33994094', '33985321', '33977145', '33972922', '33964023', '33963534', '33940562', '33940157', '33933294', '33926564', '33926407', '33923914', '33922911', '33919826', '33917608', '33916195', '33909041', '33898094', '33889622', '33869891', '33860760', '33851717', '33849607', '33811133', '33808002', '33799993', '33775046', '33772159', '33768912', '33762497', '33755597', '33750322', '33748842', '33742414', '33740643', '33731536']
    handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml", rettype="abstract")
    records = Entrez.read(handle)
    data_ = records["PubmedArticle"]
    if len(data_) != len(id_list):
        for i in range(len(id_list) - len(data_)):
            Id_unwanted = ''.join(records["PubmedBookArticle"][i]["BookDocument"]["PMID"])
            id_list.remove(Id_unwanted)
    for i in range(len(id_list)):
        print("Article ID: ", id_list[i])
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
            date_ = ''.join(records["PubmdeArtcle"][i]["MedlineCitation"]["Article"]["ArticleDate"]["Year"])
        print(title_)
        print(date_)
        print(publication_type_)
        print(abstract_)


def new_request():
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=congenital+myopathy+journal+article[publication%20type]&retmode=json&usehistory=y')
    # print(rob.status_code)
    query_key = rob.json()['esearchresult']['querykey']
    web_env = rob.json()['esearchresult']['webenv']
    print('query_key=', query_key)
    print('web_env=', web_env)
    # Request_for_list_of_ID
    urlsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&query_key=" + str(
        query_key) + "&WebEnv=" + str(web_env) + "&retmax=10000&usehistory=y&retmode=json"
    rsearch = requests.get(urlsearch)
    # print(rsearch.status_code)
    # print(urlsearch)
    id_all = rsearch.json()['esearchresult']['idlist']
    print(len(id_all))


def ft_peewee_():

    #DataBase_C
    db = SqliteDatabase('article_pubmed.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db
    db.create_tables([Article])

    #Inf_Recup
    id_list = id_list = ['33246213', '33244741', '33235377', '33200426', '33193651']
    Entrez.email = "hugues.escoffier@etu.unsitra.fr"
    handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml", rettype="abstract")
    records = Entrez.read(handle)
    for i in range(len(id_list)):
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
        # print(id_list[i])
        # print(title_)
        # print(date_)
        # print(publication_type_)
        # print(abstract_)
        #DB_Insert
        article = Article.create(id=id_list[i], title=title_, date=date_, type=publication_type_, abstract=abstract_)
    for arti in Article.select():
        if arti.abstract == "None":
            arti.delete()
        elif arti.type != "Journal Article":
            arti.delete()
        else:
            print(arti.id)
            print(arti.title)

    db.close()

# ft_peewee_()


def api_pubmed_database():

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
    list_id_100 = []
    str_id_100 = str()

    # Database_C
    db = SqliteDatabase('article_pubmed.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db
    db.create_tables([Article])

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
            list_id_100.clear()
            list_id_100.append(elmt)
            str_id_100 = str(elmt)

        else:
            list_id_100.append(elmt)
            str_id_100 = str_id_100 + str(elmt)

    #Treatment_last_A
    for i in range(len(list_id_100)):
        Entrez.email = "hugues.escoffier@etu.unsitra.fr"
        handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
        records = Entrez.read(handle)
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


# api_pubmed_database()


def database_search():
    # article = [['2020', 12], ['2019', 37], ['2018', 29], ['2017', 26], ['2016', 48], ['2015', 42], ['2014', 55], ['2013', 77], ['2012', 51], ['2011', 48], ['2010', 48], ['2009', 42], ['2008', 43], ['2007', 56], ['2006', 53], ['2005', 42], ['2004', 47], ['2003', 54], ['2002', 43], ['2001', 46], ['2000', 35], ['1999', 46], ['1998', 30], ['1997', 31], ['1996', 43], ['1995', 48], ['1994', 31], ['1993', 34], ['1992', 23], ['1991', 17], ['1990', 15], ['1989', 4], ['1988', 6], ['1987', 5], ['1986', 4], ['1984', 1], ['1983', 2], ['1982', 3], ['1981', 1], ['1977', 1], ['1973', 1]]
    # pubmed = [['2021', 908], ['2020', 281], ['2019', 327], ['2018', 295], ['2017', 296], ['2016', 280], ['2015', 289], ['2014', 315], ['2013', 308], ['2012', 238], ['2011', 243], ['2010', 216], ['2009', 188], ['2008', 191], ['2007', 184], ['2006', 180], ['2005', 184], ['2004', 161], ['2003', 179], ['2002', 156], ['2001', 144], ['2000', 156], ['1999', 145], ['1998', 158], ['1997', 143], ['1996', 132], ['1995', 136], ['1994', 90], ['1993', 120], ['1992', 90], ['1991', 107], ['1990', 93], ['1989', 82], ['1988', 68], ['1987', 79], ['1986', 81], ['1985', 99], ['1984', 77], ['1983', 80], ['1982', 54], ['1981', 55], ['1980', 58], ['1979', 39], ['1978', 48], ['1977', 45], ['1976', 40], ['1975', 46], ['1974', 3], ['1973', 3], ['1971', 5], ['1963', 1], ['1962', 1], ['1952', 1]]
    db = SqliteDatabase('article_pubmed.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db
    db.create_tables([Article])
    query = Article.select().where(Article.date == '2021')
    print(len(query))
    i = 0
    for arti in query:
        print
        # print(arti.id)
        i += 1
    # print(i)
    db.close()


# database_search()


def api_mgt_database():
    fichier = open("List_id_MGT.txt", 'r')
    list_mgt = []
    id_ = ""
    for i in fichier.read():
        if i == " ":
            list_mgt.append(id_)
            id_ = ""
        else:
            id_ = id_ + i
    fichier.close()
    list_mgt.append(id_)
    list_mgt_final = []
    for i in list_mgt:
        if i not in list_mgt_final:
            list_mgt_final.append(i)
    # Database_C
    db = SqliteDatabase('article_mgt1.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db

    db.create_tables([Article])

    list_id_100 = []
    str_id_100 = str()
    for elmt in tqdm(iterable=list_mgt_final, desc='creation_'):
        if len(list_id_100) == 100:
            Entrez.email = "hugues.escoffier@etu.unsitra.fr"
            handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
            records = Entrez.read(handle)
            ok = 0
            while ok == 0:
                c = 0
                for i in range(len(list_id_100)):
                    # print(i)
                    # print("Article ID: ", id_list[i])
                    if records["PubmedArticle"][i]["MedlineCitation"]["PMID"] != list_id_100[i]:
                        list_id_100.remove(list_id_100[i])
                        break
                    else:
                        c += 1
                if c == len(list_id_100):
                    ok = 1
            for i in range(len(list_id_100)):
                try:
                    abstract_ = ''.join(
                        records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
                except:
                    abstract_ = "None"

                title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
                publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"]
                if len(publication_type_list) != 1:
                    z = 0
                    for y in range(len(publication_type_list)):
                        if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][
                                       y]) == "Journal Article":
                            publication_type_ = "Journal Article"
                            z = 1
                    if z == 0:
                        publication_type_ = "Other"
                else:
                    publication_type_ = ''.join(
                        records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
                try:
                    date_ = ''.join(
                        records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"][
                            "Year"])
                except:
                    try:
                        date_ = ''.join(
                            records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
                    except:
                        complete_date_ = ''.join(
                            records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"][
                                "PubDate"]["MedlineDate"])
                        date_ = ''
                        c = 0
                        for lettre in complete_date_:
                            if c == 4:
                                break
                            date_ = date_ + lettre
                            c += 1
                # Add_to_db
                article = Article.create(id=list_id_100[i], title=title_, date=date_, type=publication_type_,
                                         abstract=abstract_)
            list_id_100.clear()
            list_id_100.append(elmt)
            str_id_100 = str(elmt)

        else:
            list_id_100.append(elmt)
            str_id_100 = str_id_100 + str(elmt)

    # Treatment_last_A
    for i in range(len(list_id_100)):
        Entrez.email = "hugues.escoffier@etu.unsitra.fr"
        handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
        records = Entrez.read(handle)
        ok = 0
        while ok == 0:
            c = 0
            for i in range(len(list_id_100)):
                # print(i)
                # print("Article ID: ", id_list[i])
                if records["PubmedArticle"][i]["MedlineCitation"]["PMID"] != list_id_100[i]:
                     list_id_100.remove(list_id_100[i])
                     break
                else:
                    c += 1
            if c == len(list_id_100):
                ok = 1
    for i in range(len(list_id_100)):
        Entrez.email = "hugues.escoffier@etu.unsitra.fr"
        handle = Entrez.efetch(db="pubmed", id=list_id_100, retmode="xml", rettype="abstract")
        records = Entrez.read(handle)
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
                if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][
                               y]) == "Journal Article":
                    publication_type_ = "Journal Article"
                    z = 1
            if z == 0:
                publication_type_ = "Other"
        else:
            publication_type_ = ''.join(
                records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
        try:
            date_ = ''.join(
                records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"])
        except:
            try:
                date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
            except:
                complete_date_ = ''.join(
                    records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"][
                        "MedlineDate"])
                date_ = ''
                c = 0
                for lettre in complete_date_:
                    if c == 4:
                        break
                    date_ = date_ + lettre
                    c += 1
        # Add_to_db
        article = Article.create(id=list_id_100[i], title=title_, date=date_, type=publication_type_,
                                 abstract=abstract_)
        #Del_false_positive
    for arti in Article.select():
        if arti.abstract == "None":
            arti.delete_instance()
        elif arti.type != "Journal Article":
            arti.delete_instance()
    db.close()


# api_mgt_database()


def negative_set():

    #Afin d'éviter de relancer plusieurs fois le programme il faudrait faire la liste de toute les années presente dans les différentes bases de données.
    #Partie 1 : Compteur/années
    list_all = []
    i = 0
    c = 0
    db = SqliteDatabase('article_mgt1.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db

    db.create_tables([Article])
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
    db.close()
    # print(list_all) -> Liste du nombre d'article par année

    db = SqliteDatabase('article_negative_set.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db

    db.create_tables([Article])
    # Partie 2 : Selection de 1000 articles/années
################################################################################################################################################################################################################
    for T in list_all:
        #Le while permet de repeter la boucle 'for' tant qu'il n'y a pas 1000 articles dans la base de données.
        compteur_article_annee = 0
        OK = 'False'
        while OK == 'False':
##########################################################################################################################################################################################################################################
            # Recherche des articles par années
            rob = requests.get(
                'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/?db=pubmed&term=' +str(T[0]) +'[Date%20-%20Publication]+journal+article[publication%20type]+&retmode=json&usehistory=y')
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
                    #Récup. Abstract
                    try:
                        abstract_ = ''.join(
                            records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
                    except:
                        abstract_ = "None"
                    #Récup. Title
                    title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
                    #Récup. PublicationType
                    publication_type_list = records["PubmedArticle"][i]["MedlineCitation"]["Article"][
                        "PublicationTypeList"]
                    if len(publication_type_list) != 1:
                        z = 0
                        for y in range(len(publication_type_list)):
                            if ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"][
                                           y]) == "Journal Article":
                                publication_type_ = "Journal Article"
                                z = 1
                        if z == 0:
                            publication_type_ = "Other"
                    else:
                        publication_type_ = ''.join(
                            records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
                    #Récup. Date
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
                                records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"][
                                    "PubDate"]["MedlineDate"])
                            date_ = ''
                            c = 0
                            for lettre in complete_date_:
                                if c == 4:
                                    break
                                date_ = date_ + lettre
                                c += 1
                    #Ajout à la base de données (le "if" permet d'éviter les faux positifs)
                    if publication_type_ == 'Journal Article' and abstract_ !='None' and date_ == T[0]:
                        article = Article.create(id=random_id_all[i], title=title_, date=date_, type=publication_type_, abstract=abstract_)
                        compteur_article_annee += 1
                    if compteur_article_annee == 1000:
                        OK = 'True'
                        print(T[0])
                        break
    db.close()


# negative_set()


def toto(annotation_i):
    identifier_ = annotation_i.keys()
    identifier = annotation_i['infon'][0]
    bioconcept = annotation_i['infon'][1]
    start_offset = annotation_i['location']['@offset']
    length = annotation_i['location']['@length']
    term = annotation_i['text']

    pprint([identifier_,
            identifier,
            bioconcept,
            start_offset,
            length,
            term,
            ])

def pubtator_():

    x = 0

    db = SqliteDatabase('article_mgt1.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db

    #Création de la sous classe "annotation"

    class Annotation(Model):
        pmid = ForeignKeyField(Article, backref='annotation')
        mention = CharField()
        bioconcept = CharField()
        identifiers = CharField()
        start_offset = CharField()
        length = CharField()

        class Meta:
            database = db

    db.create_tables([Article, Annotation])


    #On recup. l'ensemble des IDs de la db de article
    query = Article.select()
    liste_id = []
    for arti in query:
        liste_id.append(arti.id)
    print(liste_id)
    print(db)
    for i in tqdm(iterable=liste_id[:10], desc='verification_'):
        url_pubtator = 'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids=' + i
        # print(url_pubtator)
        rob = requests.get(url_pubtator)
        print(url_pubtator)
        exit()
        data_ = xmltodict.parse(rob.content)
        document = data_["collection"]["document"]
        tree = document['passage']
        for annotation in tree:

            #pprint(annotation)
            print("================================================================================================")
            #pprint(annotation['annotation'])

            annotation_i = annotation['annotation']

            # print("/////////////////////")
            # pprint(annotation_i)
            # print("$$$$$$$$$$$$$$$$$$$$$")
#            identifier_ = annotation_i['infon'][0]['#text']
            print(type(annotation_i), type(annotation_i) == list)
            print(type(annotation_i), type(annotation_i) == dict)
            print(type(annotation_i), type(annotation_i) == collections.OrderedDict)

            if not len(annotation_i) == 4:
                for a in annotation_i:
                    toto(a)
            else:
                print(len(annotation_i))
                toto(annotation_i)
                pass
                # for a in annotation_i:
                #     print(type(a))
                #     print("<<<<<<<<<<<<")
                #     toto(a)
                #     exit()

            # for i, racine in enumerate(annotation_i):
            #     pprint([i,
            #             racine,
            #             ])
            #     print()

                # identifier_ = racine['infon'][0]['#text']
                # bioconcept_ = racine['infon'][1]['#text']
                # start_offset_ = racine[2]['location'][0]['@offset']
                # length_ = racine[2]['location'][1]['@length']
                # term_ = racine[3]['text']
                #
                # pprint([i,
                #         # identifier_,
                #         # bioconcept_,
                #         start_offset_,
                #         length_,
                #         term_,
                #         ])


                # annotation = Annotation.create(pmid=i, mention=term_, bioconcept=bioconcept_,
                #                                identifier=identifier_, start_offset=start_offset_,
                #                                length=length_)
                # annotation.save()

            #exit()



            # try:
            #     annotation_i = annotation['annotation']
            #     if len(annotation_i) == 4:
            #         print(annotation_i)
            #         exit()
            #         # try:
            #         #     for racine in annotation_i:
            #         #         identifier_ = racine['infon'][0]['#text']
            #         #         bioconcept_ = racine['infon'][1]['#text']
            #         #         start_offset_ = racine['location']['@offset']
            #         #         length_ = racine['location']['@length']
            #         #         term_ = racine['text']
            #         #         annotation = Annotation.create(pmid=i, mention=term_, bioconcept=bioconcept_, identifier=identifier_, start_offset=start_offset_, length=length_)
            #         # except:
            #         #     # print(i)
            #         #     identifier_ = annotation_i['infon'][0]['#text']
            #         #     # print(identifier_)
            #         #     bioconcept_ = annotation_i['infon'][1]['#text']
            #         #     # print(bioconcept_)
            #         #     start_offset_ = annotation_i['location']['@offset']
            #         #     # print(start_offset_)
            #         #     length_ = annotation_i['location']['@length']
            #         #     # print(length_)
            #         #     term_ = annotation_i['text']
            #         #     # print(term_)
            #         #     annotation = Annotation.create(pmid=i, mention=term_, bioconcept=bioconcept_,
            #         #                                    identifier=identifier_, start_offset=start_offset_,
            #         #                                    length=length_)
            #         #
            #         # annotation.save()
            #     else:
            #         for racine in annotation_i:
            #             identifier_ = racine['infon'][0]['#text']
            #             bioconcept_ = racine['infon'][1]['#text']
            #             start_offset_ = racine['location']['@offset']
            #             length_ = racine['location']['@length']
            #             term_ = racine['text']
            #             annotation = Annotation.create(pmid=i, mention=term_, bioconcept=bioconcept_,
            #                                            identifier=identifier_, start_offset=start_offset_,
            #                                            length=length_)
            #             annotation.save()
            # except:
            #     #Uniquement pour la forme
            #     x += 1
    print('OK')
    #Permet de savoir environ combien d'article n'avait pas d'annotation, soit dans le titre soit dans l'abs.
    # print(x)
    db.close()


# pubtator_()

def sheesh():
    Entrez.email = "hugues.escoffier@etu.unsitra.fr"
    handle = Entrez.efetch(db="pubmed", id=33277141, retmode="xml", rettype="abstract")
    records = Entrez.read(handle)
    print(records)
    print(type(records))

# sheesh()


class Annotation(Model):
    id = CharField()
    bioconcept = CharField()
    mention = CharField()
    identifier = CharField()


# def db_pubtator():
#     all_l = []
#     connection = sqlite3.connect('cache.db', timeout=10)
#     db.create_tables([Annotation])
#     with open("/Users/hugues.escoffier/Documents/Stage/gene2pubtatorcentral.txt", 'r') as fin:
#         for line in tqdm(iterable=fin, desc='reading'):
#             cols = line.strip('\n').split('\t')
#             a = (cols[0], cols[1], cols[2], cols[3])
#             all_l.append(a)
#             if len(all_l) == 990:
#                 Annotation.insert_many(all_l, fields=[Annotation.id, Annotation.bioconcept, Annotation.identifier,
#                                                       Annotation.mention]).execute()
#                 all_l.clear()
#     c = 0
#     for i in range(0, 1000):
#         c += 1
#     Annotation.insert_many(all_l, fields=[Annotation.id, Annotation.bioconcept, Annotation.identifier,
#                                           Annotation.mention]).execute()
#     db.close()
#
#
# db_pubtator()


db = SqliteDatabase('geneID')


class Gene(Model):
    id = CharField()
    name = CharField()
    uniprot = CharField()

    class Meta:
        database = db

        ######## + db annotation pour gene_pubtator ######

db = SqliteDatabase('pmids_gene')


class Pmids(Model):
    id = CharField()
    gene_id = CharField()
    gene_name = CharField()

    class Meta:
        database = db


def get_list_gene_identifier():
# Créer un db contenant l'ensemble des pmids d'articles sur le sujet d'un gène impliqué dans un type de MC
    list_gene_identifier = []
    list_elmt = []
    query = Gene.select()
    for gene in query:
        list_gene_identifier.append(gene.id)
#################################################################################
    for gene_ide in tqdm(iterable=list_gene_identifier, desc='_'):
        gene_bis = str(gene_ide)
        query_bis = Annotation.select().where(Annotation.identifier == gene_bis)
        for elmt in query_bis:
            pmids = Annotation.id
            gene_id = elmt
            gene_name = Annotation.mention
            tuple_list_id_gene = (pmids, gene_id, gene_name)
            list_elmt.append(tuple_list_id_gene)
        Annotation.insert_many(list_elmt, fields=[Pmids.id, Pmids.gene_id, Pmids.gene_name]).execute()
        list_elmt.clear()


class AnnotationPubtator(Model):
    id = CharField()
    bioconcept = CharField()
    mention = CharField()
    identifier = CharField()


class Article(Model):
    id = CharField()
    title = CharField()
    date = CharField()
    type = CharField()
    abstract = CharField()

    def insert_init_db(self):
        pass


#Sous classe Annotation
class Annotation(Model):
    pmid = ForeignKeyField(Article, backref='annotation')
    mention = CharField()
    bioconcept = CharField()
    identifier = CharField()

    def insert_init_db(self):
        pass
# get_list_gene_identifier()


def annotation_article_mc():
    list_annotation = []
    query = Article.select()
    for article in query:
        article_pmids = str(article.id)
        for annot in AnnotationPubtator.select().where(AnnotationPubtator.id == article_pmids):
            mention = annot.mention
            bioconcept = annot.bioconcept
            identifier = annot.identifier
            tuple_annot = (article_pmids, mention, bioconcept, identifier)
            list_annotation.append(tuple_annot)
        Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept, Annotation.identifier]).execute()
        list_annotation.clear()

        # def get_pubtator_annotation(self):
        #     list_annotation = []
        #     query = Article.select()
        #     for article in query:
        #         article_pmids = str(article.id)
        #         for annot in Annotation_Pubtator.select().where(Annotation_Pubtator.id == article_pmids):
        #             mention = annot.mention
        #             bioconcept = annot.bioconcept
        #             identifier = annot.identifier
        #             tuple_annot = (article_pmids, mention, bioconcept, identifier)
        #             list_annotation.append(tuple_annot)
        #         Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
        #                                                         Annotation.identifier]).execute()
        #         list_annotation.clear()
