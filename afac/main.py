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


def afac():
    list_joint = ['28547000', '25747004', '20191014', '15564032', '17631035', '31127036', '20951040', '33909041', '21834041', '31228046', '33775046', '24239060', '25566070', '27726070', '31794073', '15468086', '32670090', '19181090', '24692096', '21798101', '15072110', '19553116', '12805120', '19553121', '25205138', '25182138', '30203143', '21514153', '11166164', '30407167', '19944167', '19206168', '33646172', '23478172', '15960177', '9185179', '23572184', '20422195', '33384202', '29274205', '26578207', '25913210', '20452215', '27074222', '25890230', '14575234', '21642240', '25268244', '22371254', '23273262', '15495263', '23919265', '24787270', '23977274', '29731279', '32456280', '23800289', '18300303', '23650303', '26506308', '20850316', '23826317', '32350326', '23091329', '27293330', '15221331', '25888334', '23183335', '32403337', '22832343', '25088345', '28416349', '21677359', '9140362', '24725366', '26891371', '17187373', '28017374', '11333380', '30406384', '28436394', '28927399', '33706403', '15236405', '15226407', '10844410', '28357410', '33742414', '27888415', '19767415', '30631434', '31004442', '26418456', '22358459', '11257471', '11748499', '7706500', '32066503', '18461503', '22392505', '24642510', '27357517', '17504518', '18487519', '10508519', '29328520', '19953533', '22067542', '19563543', '27576556', '18716557', '25079567', '18574571', '25110572', '33458580', '17227580', '22825594', '25264603', '29338614', '7908614', '30788618', '25353622', '11106625', '32093627', '33190635', '27215641', '14593641', '33740643', '29178646', '29141652', '23620652', '10958653', '19648653', '29178655', '15269663', '23886664', '25428687', '19562689', '17194691', '23762716', '30544720', '8580725', '17387733', '23933735', '27858739', '16941741', '20303757', '23294764', '33397769', '23394784', '33256785', '25949787', '30987788', '12921789', '16230791', '19325803', '30770808', '22407809', '27389816', '19209820', '26172852', '21303860', '21104864', '23613869', '25204870', '26035871', '22174871', '30926871', '16288873', '22431881', '29691892', '33667896', '18976909', '31874912', '30732915', '30567918', '24456932', '30395933', '20888934', '28815944', '23305948', '26751952', '27412953', '20179953', '26436962', '32222963', '27387980', '28780987', '23656990', '33799993', '21305017', '31228046', '17097056', '34066119', '27861123', '20022194', '30701273', '32456280', '15236405', '11846417', '22560515', '32793522', '18716557', '11696561', '33458580', '30900782', '30926871', '31874912', '8887951', '14567970', '24590001', '23938035', '33618039', '17676042', '29103045', '27538056', '25566070', '21482111', '23897157', '25664165', '21129173', '30884204', '27854204', '26273216', '31766224', '27854229', '20839240', '30412272', '32456280', '21347281', '26506308', '22396310', '30611313', '32994313', '23826317', '18434328', '27293330', '27911331', '32403337', '30103348', '30426359', '19197364', '21623381', '30406384', '33926407', '28357410', '29950440', '21762456', '20817456', '20181480', '30894500', '29125502', '22392505', '31450509', '26823526', '27576556', '25260562', '23071563', '18817572', '23278578', '22096584', '24016602', '23917616', '25353622', '21221624', '20927630', '31625632', '25957634', '33190635', '27870637', '33255644', '29141652', '24755653', '20476667', '31449669', '33407688', '27858727', '27858739', '26351754', '29091763', '24668768', '31877772', '23394783', '31017801', '24381816', '25262827', '28740838', '30451843', '23273872', '23975875', '22431881', '28007904', '31874912', '33923914', '18429927', '24456932', '29130937', '23754947', '19084976', '27343996', '31070086', '29950399', '30423015', '21314017', '32381029', '17631035', '28012042', '26247046', '29946067', '25839108', '10944223', '30412272', '32456280', '10892286', '30932294', '30611313', '7987325', '18434328', '27911331', '30103348', '18313359', '34066362', '7847370', '30406384', '8012389', '29950399', '20080402', '30631434', '23894444', '11274444', '9436456', '29193480', '28777491', '20213496', '17504518', '20074522', '9199552', '30824560', '18031562', '25387602', '25353622', '31625632', '33190635', '29141652', '31227654', '30168660', '15269663', '27879676', '32368681', '26700687', '9175745', '10599760', '29091763', '23553787', '25262827', '33667896', '31874912', '17204937', '8395939', '21790973', '28939973', '27343996', '25566070', '31403083', '26578207', '26273216', '32456280', '32403337', '24959344', '30406384', '33926407', '27576556', '25353622', '33190635', '29141652', '27858727', '25168790', '30770808', '22818856', '31874912', '31127036', '31228046', '19181092', '21798101', '25205138', '19944167', '23572184', '27074222', '25890230', '32456280', '32160286', '23826317', '27293330', '25888334', '32403337', '24725366', '30406384', '28436394', '27890461', '32066503', '22392505', '22560515', '29328520', '27576556', '18716557', '33066566', '25110572', '25264603', '33190635', '29178646', '29141652', '23620652', '19562689', '27858739', '24668768', '33397769', '25949787', '25874796', '22407809', '19209820', '21104864', '30926871', '17160903', '24456932', '30395933', '32222963', '22242131', '26578207', '32403337', '19026398', '25353622', '28254648', '26133662', '24243016', '17251023', '23938035', '17676042', '16585051', '27538056', '23338057', '25566070', '22369075', '32670090', '21482111', '21576112', '20865121', '26908122', '32937143', '25633151', '23346162', '25664165', '29669168', '33449170', '33646172', '21129173', '20422195', '30884204', '26273216', '27861221', '27854229', '27035234', '20839240', '30412272', '28544275', '20227276', '32456280', '21347281', '22396310', '30611313', '23826317', '26199319', '18434328', '27293330', '27911331', '32403337', '30103348', '24102355', '17008356', '30426359', '24569368', '24569376', '30406384', '26035394', '33926407', '28357410', '32514412', '22172417', '30631434', '21514436', '27623444', '28842446', '30925452', '21762456', '20817456', '31628461', '20127478', '20181480', '29125502', '22392505', '31450509', '26823526', '24366529', '28971531', '17825552', '27576556', '30733559', '30824560', '25260562', '23071563', '18817572', '23278578', '33458580', '22096584', '20858595', '24016602', '25264603', '32315611', '30788618', '19932619', '19932620', '25353622', '21221624', '20927630', '31625632', '25957634', '33190635', '27870637', '28676641', '33255644', '29141652', '24755653', '29178655', '30232666', '31449669', '23844677', '17376685', '33407688', '30601711', '27858727', '18162732', '24798732', '19130742', '26351754', '15731758', '24668768', '29149770', '22924779', '23394783', '25893792', '31017801', '33097808', '25262827', '26841830', '28740838', '30451841', '30451843', '26842864', '20529869', '23273872', '23975875', '22613877', '22431881', '21737882', '25492887', '18394888', '30874888', '29691892', '33459893', '17134899', '23374900', '28007904', '29506908', '30149909', '20434914', '32028919', '18429927', '24456932', '29130937', '28589938', '33164942', '23754947', '23092955', '17932957', '25501959', '29246969', '32809972', '23813975', '19084976', '27343996', '16227997', '32456280', '32328638', '29091763', '30770808', '31874912', '27939133', '25664165', '32456280', '22106411', '15829503', '31450509', '23071563', '23933735', '33354762', '26160855', '23754947', '25617006', '25700176', '19697368', '23455423', '33000450', '27263464', '27066560', '33458580', '31877772', '24686783', '29566793', '32537934', '31127036', '22449146', '21445359', '17703371', '21063443', '24777450', '25070542', '25668678', '30151950', '31228046', '27538056', '21798101', '12805120', '25205138', '23897157', '23572184', '27074222', '21109227', '25890230', '32456280', '23826317', '27293330', '25888334', '24959344', '24725366', '30406384', '28436394', '33742414', '32066503', '22392505', '22560515', '29328520', '27576556', '25110572', '25264603', '25353622', '33190635', '29178646', '29141652', '27858739', '33397769', '25949787', '33693846', '21104864', '22431881', '24456932', '30395933', '32222963', '26754003', '31228046', '25205138', '24960163', '26578207', '27074222', '25890230', '32352246', '32456280', '32403337', '24959344', '24725366', '28436394', '28357410', '29328520', '23746549', '25110572', '25264603', '25353622', '29178646', '29141652', '25428687', '27858739', '33397769', '25949787', '31970803', '24456932', '28815944', '25721947', '31360996', '31228046', '25205138', '26578207', '27074222', '32456280', '32403337', '26541337', '24959344', '24725366', '28436394', '29328520', '27443559', '25110572', '25264603', '29178646', '29141652', '24268659', '27858739', '33397769', '25949787', '31970803', '28815944', '31228046', '24960163', '30291184', '26578207', '27074222', '32456280', '29152331', '28436394', '29328520', '25250574', '29266598', '29178646', '29141652', '30642739', '27858739', '33397769', '25949787', '26035871', '30395933', '28815944', '22166137', '32456280', '27816943', '25044114', '26322222', '25111228', '23954233', '22371254', '32456280', '32403337', '24959344', '30406384', '26802438', '22101682', '31970803', '30770808', '28681861', '31874912', '30802937', '28498977', '12884002', '29172004', '21881007', '31541013', '17251023', '11552027', '28370029', '23938035', '31127036', '9781038', '33618039', '17676042', '29103045', '33775046', '11119047', '23338057', '12118066', '26995067', '25566070', '22403079', '32925083', '17827085', '11377105', '20700106', '27012108', '21482111', '22645112', '26908122', '9828128', '23390130', '22968136', '29192144', '25633151', '27012153', '27155155', '21478156', '23695157', '23346162', '30541163', '25664165', '7726166', '33449170', '21129173', '26454198', '10790201', '26760201', '21488203', '30884204', '32862205', '26578207', '26273216', '30999217', '8640223', '26338224', '27854229', '25890230', '27035234', '20839240', '14618257', '30047259', '24452262', '23919265', '10900271', '30412272', '7611280', '32456280', '21347281', '12847286', '16828287', '19433289', '30932294', '16042307', '11456308', '22396310', '20358311', '30611313', '32994313', '23826317', '26199319', '28685322', '11275328', '18434328', '27293330', '27911331', '32403337', '30103348', '29567349', '17008356', '22520358', '30426359', '19197364', '24725366', '24569376', '30406384', '25603385', '28934386', '26035394', '17005396', '25281397', '11846405', '12018406', '33926407', '11395408', '28357410', '12859411', '32514412', '22172417', '29343419', '23086420', '10466421', '23109424', '30631434', '21440438', '2926439', '29950440', '31004442', '23071445', '28842446', '12707446', '32805447', '30925452', '21762456', '20817456', '28190456', '20400459', '28624463', '11793470', '20181480', '12687498', '30894500', '29125502', '15829503', '22392505', '21135508', '16959509', '31450509', '11595516', '22264517', '22258523', '26823526', '17621527', '11733541', '12522554', '27576556', '30733559', '30824560', '25260562', '23071563', '14660569', '18817572', '25581576', '23278578', '22096584', '25708584', '15725586', '10714588', '16583589', '22068590', '14690594', '24016602', '9600602', '25087613', '23917616', '25353622', '21221624', '12031625', '20927630', '17537630', '31625632', '25957634', '33190635', '27870637', '28676641', '14593641', '24726641', '33255644', '10802647', '29141652', '24755653', '9305655', '1785661', '25313664', '30232666', '31449669', '16288675', '12489675', '17376685', '25428687', '12554688', '33407688', '22987702', '24011703', '23857703', '30601711', '27858727', '12874727', '12467733', '23933735', '20682747', '12467749', '26351754', '26086764', '28637766', '24668768', '29149770', '9736772', '8710776', '22924779', '10502779', '23394783', '23394784', '19846786', '31017801', '21281811', '24381816', '22841819', '25262827', '10063835', '28740838', '28237839', '30451841', '30451843', '10726846', '16289848', '26160855', '26842864', '23818870', '23273872', '23975875', '18358876', '22431881', '30241883', '29691892', '33667896', '28007904', '30902907', '16157907', '29506908', '30149909', '20434914', '23307925', '11001925', '18429927', '24456932', '28589938', '33164942', '25541946', '23754947', '24581957', '12217958', '18006961', '25197964', '28622964', '29246969', '33076971', '19084976', '23559977', '22153990', '27343996', '12351999', '7493025', '7493026', '32670090', '33449170', '27854229', '21642240', '23273262', '31840275', '32580284', '23800289', '15582318', '21551322', '16651346', '21167350', '23031367', '8358441', '24777450', '17347475', '32793522', '30029526', '27443559', '27683561', '20215591', '25353622', '26752647', '15038665', '26544689', '28125727', '19325803', '22610851', '20045868', '29687901', '27412953', '23636980', '25617006', '21305017', '25149037', '28729039', '21834041', '19181095', '28258125', '23401156', '11114175', '26670220', '11889243', '23273262', '10205275', '32456280', '17434305', '32403337', '22496423', '29070483', '26205529', '20418530', '9708547', '27066560', '33926564', '25353622', '23489661', '26544689', '19325803', '24803840', '32307885', '25529940', '15605950', '27412953', '32578970', '22723986', '27177998', '28547000', '18506004', '26782017', '21305017', '31127036', '31133047', '11733062', '31794073', '32670090', '19181095', '25205138', '20733148', '23401156', '23478172', '31068177', '21642240', '23273262', '32456280', '23800289', '17434305', '30611313', '21551322', '31850331', '32403337', '34103343', '21167350', '7847377', '30406384', '15699387', '28927399', '27888415', '21480433', '30631434', '23152444', '26799446', '24777450', '17347475', '32607476', '29070483', '17504518', '32793522', '31852522', '17336526', '26205529', '19563543', '21965549', '27576556', '33926564', '29802573', '33458580', '19336582', '20215591', '7795598', '16684601', '25264603', '25353622', '30907627', '33190635', '29141652', '29178655', '17118657', '20554658', '23489661', '15136674', '19562689', '26544689', '28503705', '11106718', '21288719', '32833721', '24710723', '28125727', '25564733', '23933735', '21984748', '31721788', '16230791', '19325803', '19712804', '30770808', '34053846', '19138847', '29170849', '25576864', '22431881', '30874888', '29691892', '24828896', '25666907', '31874912', '30794915', '31506931', '24456932', '15605950', '27412953', '32578970', '23636980', '27387980', '15322983', '21378987', '21834041', '29192144', '15036327', '30631434', '25353622', '30215711', '33799993', '21305017', '31127036', '32670090', '8673105', '32456280', '23800289', '21167350', '24777450', '32793522', '27576556', '19325803', '33435938', '27412953', '30016436', '28681861', '30065953', '31228046', '32184166', '26578207', '32456280', '32403337', '28436394', '30631434', '29328520', '25353622', '27858739', '28104788', '28815944', '31228046', '31133047', '22286171', '31647200', '30701273', '32456280', '28017374', '30631434', '18006477', '29328520', '32793522', '28220527', '29266598', '33397769', '28815944', '25541946', '30679003', '20191014', '15564032', '31127036', '31228046', '31133047', '33376055', '16002060', '12715073', '19181091', '24692096', '23715096', '21798101', '21350120', '12805120', '3062133', '25205138', '17525139', '24056153', '24960163', '11166164', '30407167', '19944167', '29669168', '19295172', '23572184', '3319190', '20422195', '26578207', '22941215', '27074222', '25890230', '25268244', '32352246', '30963254', '15495263', '30701273', '23977274', '32456280', '25740301', '23010307', '23826317', '27293330', '29152331', '25888334', '32403337', '24959344', '11738357', '21677359', '24725366', '30406384', '32684384', '29848386', '28436394', '33706403', '28357410', '33742414', '22172417', '31696431', '30631434', '26403434', '24046450', '26418456', '27890461', '11257471', '32066503', '22392505', '29328520', '31852522', '19838523', '19346529', '18716557', '33066566', '25079567', '18574571', '25110572', '33458580', '17227580', '25264603', '26562614', '25353622', '29246625', '33190635', '10051637', '27215641', '14593641', '29178646', '29141652', '23620652', '19648653', '20554658', '21357678', '19562689', '32779703', '30544720', '31060725', '8580725', '7608737', '27858739', '33397769', '26842778', '25949787', '31721788', '19325803', '22407809', '19209820', '25262827', '26841830', '23375831', '30768849', '21104864', '23613869', '16917880', '22431881', '32307885', '24456932', '30395933', '20888934', '12207937', '28815944', '25541946', '27412953', '32222963', '27387980', '26197980', '30057997', '12138997', '27807076', '24522088', '33513091', '24223098', '30462217', '26670220', '31766224', '23954233', '22371254', '29669293', '31850331', '27109386', '32411395', '29498561', '32722643', '31897643', '23626698', '27114706', '33396724', '24381816', '31092906', '28367954', '33799993', '32844998', '30203143', '33694278', '31455395', '30631434', '30515627', '27745833', '32453872', '28547000', '29172004', '21314017', '32381029', '17538032', '21825032', '15564033', '17631035', '31127036', '20951040', '28012042', '31228046', '26247046', '33775046', '19734047', '27531051', '27538056', '12810058', '9508059', '19645060', '25566070', '12161072', '31794073', '1774074', '12136074', '12112081', '25882082', '12937085', '32670090', '25821091', '24561095', '24692096', '30578099', '33124102', '21482111', '24896116', '12805120', '29457121', '31680123', '29192144', '25960145', '23897157', '24706162', '25664165', '29669168', '33449170', '33646172', '23478172', '17365175', '23639175', '26932181', '20422195', '26578207', '32242214', '26273216', '30999217', '11113224', '22028225', '27854229', '26242231', '19346234', '25476234', '26019235', '20839240', '7951247', '22371254', '23919265', '22030266', '23617272', '30412272', '27708273', '32456280', '17596281', '10892286', '23800289', '30932294', '19303294', '20583297', '22396310', '30611313', '23826317', '27293330', '29152331', '27911331', '19191333', '23183335', '32403337', '21691338', '25958340', '32655342', '22832343', '21062345', '1862346', '30103348', '23628358', '8012359', '18313359', '34066362', '19197364', '32272370', '32499372', '21926372', '23329375', '32122377', '12719381', '30406384', '25331388', '28818389', '29950399', '20080402', '27159402', '33926407', '28357410', '30652412', '7299413', '27888415', '19767415', '22172419', '8220422', '22752422', '8220423', '22172424', '31191425', '30631434', '26802438', '31004442', '23894444', '11274444', '28842446', '26799446', '29498452', '24951453', '21762456', '20817456', '9436456', '33333461', '28003463', '29062463', '29456480', '29193480', '23553484', '17483490', '28777491', '20213496', '30715496', '29125502', '32066503', '22392505', '31450509', '15448513', '17504518', '26823526', '29629541', '11709545', '9199552', '27576556', '30824560', '29498561', '18817572', '29802573', '23278578', '33458580', '29391587', '21520599', '25387602', '16380615', '30788618', '25353622', '21221624', '14732627', '20927630', '31625632', '25957634', '33190635', '23069638', '10783639', '12192640', '14593641', '1354642', '33184643', '33255644', '29141652', '31227654', '29178655', '23489661', '15269663', '26870666', '30232666', '19959667', '27879676', '26255678', '32368681', '17376685', '26700687', '25428687', '19562689', '31383689', '21911697', '27114706', '7849712', '23762716', '11063719', '31060725', '12066726', '27858727', '25564733', '23933735', '22418739', '25628744', '9175745', '27858745', '12467748', '26351754', '27259756', '14670767', '24668768', '27134770', '31877772', '10484775', '23394783', '23394784', '33256785', '23553787', '28269792', '25116801', '30770808', '22407809', '25084811', '24381816', '1889818', '15572824', '17226826', '25262827', '26841830', '28740838', '23736855', '28681861', '18713863', '21104864', '31353864', '33176865', '20111871', '23273872', '31856875', '22431881', '1427885', '30874888', '29691892', '33667896', '24828896', '28007904', '31874912', '12565913', '33923914', '19485922', '18253926', '29169929', '24456932', '20888934', '22473935', '11159936', '17204937', '24091937', '8395939', '16917943', '23754947', '15608948', '26751952', '24581957', '23127960', '29067961', '17033962', '15336972', '21790973', '26684984', '12124989', '25521991', '31228046', '31680123', '32456280', '23183335', '30406384', '30631434', '29498452', '25387602', '25353622', '31383689', '12565913', '15336972', '26285000', '30423015', '21314017', '32117035', '19077043', '8242056', '9508059', '29946067', '24943082', '31729100', '25839108', '18008119', '26659129', '2173143', '8058156', '32849172', '10944223', '12766226', '16193245', '32456280', '18434328', '11371347', '1686388', '29950399', '30931400', '20080402', '28357410', '29605429', '30631434', '27224441', '27118449', '24939454', '28262468', '10218481', '20213496', '29125502', '30369522', '24366529', '1310531', '28877545', '30824560', '33458578', '9392583', '27048647', '29141652', '1659668', '8388676', '26700687', '31609695', '8308722', '1654742', '10599760', '1316765', '25755818', '1310898', '25735906', '33923914', '29189923', '17160927', '8395939', '1659948', '28939973', '19251977', '28547000', '29172004', '1790004', '17631035', '31127036', '20951040', '10545040', '31066047', '27531051', '31794073', '17951086', '25821091', '7224095', '23897156', '23897157', '23478172', '17365175', '20422195', '27453230', '26242231', '20425232', '28085238', '22371254', '26789268', '30412272', '31840275', '32456280', '20225280', '23800289', '25653289', '30932294', '18300303', '15961312', '24021317', '27911331', '23183335', '18313359', '34066362', '19197364', '29893365', '11528383', '30406384', '23326386', '21943391', '17005401', '20080402', '33706403', '28357410', '27888415', '19767415', '22172417', '22172419', '22172424', '26802438', '26799446', '16498447', '17885449', '27263464', '10665485', '33762497', '22392505', '17395506', '20937510', '17123513', '17504518', '19953533', '27671536', '27576556', '30824560', '24907562', '25079567', '29802573', '9585610', '16380615', '25353622', '33190635', '30921636', '12192640', '14593641', '33255644', '29141652', '15269663', '32420686', '19562689', '31383689', '22554691', '15122708', '23762716', '23933735', '28688748', '26780752', '23394784', '25168790', '16230791', '17163796', '30770808', '18602826', '26841830', '25410841', '20467841', '25307854', '23736855', '28681861', '18713863', '31353864', '28558865', '15792869', '19557870', '16365872', '22431881', '29691892', '31874912', '30612914', '21078917', '16314926', '12207930', '19085932', '24456932', '17204937', '15608948', '24581957', '29067961', '24988964', '27387980', '26578207', '26273216', '30412272', '32456280', '30103348', '33926407', '30631434', '28624463', '31852522', '29474540', '25087613', '31625632', '33190635', '29141652', '29614691', '27858727', '29691892', '33772159', '28540413', '29141652', '31794073', '30932294', '32350326', '27911331', '29950399', '28003463', '28777491', '29125502', '29498561', '28411587', '33190635', '29141652', '31227654', '30168660', '23736855', '28681861', '20191014', '21305017', '31127036', '31228046', '24692096', '21798101', '12805120', '31680123', '25205138', '33977145', '19944167', '23478172', '23572184', '27074222', '25890230', '23273262', '15495263', '32994279', '32456280', '23826317', '27293330', '25888334', '32403337', '11738357', '21677359', '24725366', '28436394', '25430424', '32819427', '26296490', '22392505', '29328520', '27576556', '25079567', '18574571', '25110572', '29266598', '25264603', '25353622', '33190635', '14593641', '29178646', '29141652', '23620652', '19562689', '30544720', '27858739', '23294764', '33397769', '25949787', '19325803', '31970803', '22407809', '19209820', '33919826', '25262827', '30768849', '21104864', '10952871', '22431881', '24456932', '30395933', '32222963', '12913210', '26322222', '24843229', '31192305', '32403337', '24959344', '22334415', '23543484', '25353622', '23667635', '28547000', '20191014', '21305017', '31127036', '21708040', '21834041', '31228046', '24239060', '27726070', '24657080', '32670090', '24692096', '21798101', '12805120', '33558124', '25205138', '16802141', '32092148', '23401156', '19944167', '23478172', '19155175', '23572184', '21402185', '26578207', '27074222', '23378224', '25890230', '23273262', '15495263', '23678273', '17846275', '32456280', '32580284', '23800289', '17434307', '23826317', '27293330', '25888334', '32403337', '22832343', '11738357', '21677359', '24725366', '7977374', '30406384', '28436394', '28357410', '27888415', '9012416', '17103435', '26418456', '22358459', '17380469', '26708479', '29125502', '19309503', '22392505', '30630514', '29328520', '30029526', '19953533', '29314551', '27576556', '18716557', '27683561', '19047562', '33066566', '25079567', '18574571', '25110572', '33458580', '19345583', '17339586', '25264603', '12592607', '22798622', '25353622', '33190635', '14593641', '29178646', '29141652', '23620652', '29178655', '23489661', '23886664', '24507666', '26255678', '19562689', '17194691', '26373698', '28264711', '32797717', '30544720', '30285720', '23850728', '32767732', '27858739', '20303757', '22980765', '33397769', '25949787', '19325803', '22407809', '25477818', '19209820', '26537820', '33919826', '30768849', '29792862', '21104864', '22431881', '30874888', '22749895', '20457903', '32799913', '24456932', '22084935', '26751952', '22519952', '27412953', '25127990', '17430991', '28547000', '20191014', '31127036', '20951040', '31228046', '24239060', '27726070', '26307083', '24692096', '21798101', '19553118', '12805120', '25205138', '22448145', '24095155', '23897157', '11166159', '11166164', '19944167', '23478172', '23572184', '1347195', '27074222', '25890230', '25268244', '22371254', '23273262', '15495263', '23678273', '32456280', '32580284', '23800289', '33307294', '18300303', '23826317', '27293330', '25888334', '32403337', '22832343', '21677359', '24725366', '30406384', '28436394', '28357410', '20554445', '26418456', '22358459', '11257471', '18382475', '16877500', '29125502', '22392505', '24642510', '29328520', '19953533', '27576556', '18716557', '33066566', '25079567', '18574571', '25110572', '30382595', '25264603', '22798622', '25353622', '11106625', '33190635', '10051637', '27215641', '14593641', '29178646', '29141652', '23620652', '19648653', '23489661', '15269663', '23886664', '24507666', '27879676', '21357678', '19562689', '29699707', '31270709', '23762716', '32797717', '30544720', '8580725', '23933735', '27858739', '23924754', '20303757', '33397769', '23394784', '20004786', '25949787', '19325803', '22407809', '19209820', '33919826', '22749829', '30768849', '28681861', '21104864', '22431881', '29691892', '24456932', '33435938', '28815944', '26751952', '27412953', '20179953', '25617006', '11822024', '16002060', '12715073', '31403083', '26322222', '24843229', '32403337', '15786463', '9634523', '33458580', '25353622', '23142638', '31897643', '29141652', '20554658', '27858741', '25893792', '33250842', '24456932', '30365001', '10053013', '21305017', '7493025', '19608030', '19608031', '17631035', '31127036', '19878039', '24667040', '21708040', '31228046', '16002060', '10655062', '25566070', '31794073', '12715073', '31403083', '32670090', '24361111', '34066119', '25208129', '23479141', '30203143', '24928145', '30407167', '33449170', '23478172', '11763198', '26273216', '2243226', '24843229', '27854229', '21530252', '23273262', '21186264', '16793270', '30412272', '30701273', '23995273', '31840275', '32456280', '27529282', '33127292', '29669293', '10051295', '23826317', '15582318', '29152331', '27911331', '32403337', '30103348', '8469351', '30406384', '32684384', '27109386', '28881388', '28040389', '28818390', '28436394', '17005401', '27159402', '31053406', '33926407', '28357410', '11846417', '12507422', '21480433', '30631434', '24777450', '33333461', '24105469', '17337483', '10462489', '17444505', '32793522', '16483541', '21965549', '27576556', '8618556', '27443559', '30824560', '27066560', '27683561', '15802564', '33926564', '29435569', '27066570', '33458580', '20215591', '16380616', '29575618', '25353622', '28716623', '31625632', '25957634', '33190635', '30245638', '32887649', '29141652', '10958653', '29178655', '20554658', '31660661', '15111675', '26544689', '27114706', '10619716', '31060725', '27858727', '7608737', '12145747', '26351754', '24668768', '27134770', '22366786', '19325803', '30770808', '24668811', '27389816', '32778822', '11788824', '26342832', '28740838', '20467841', '33693846', '32039858', '31353864', '23975875', '32307885', '30874888', '29691892', '24291893', '29687901', '31952901', '28007904', '31874912', '33923914', '26204918', '32028919', '11294923', '24456932', '31664938', '31561939', '25541946', '27412953', '31332964', '33076971', '26383991', '12351997', '28436997', '31852522']
    print(len(list_joint))


afac()
