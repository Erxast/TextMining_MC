
import requests
import xmltodict
import os
from tqdm import tqdm
from Bio import Entrez


class _article:
    def __int__(self, date, titre, abstract, publication_type):
        self.date = date
        self.titre = titre
        self.abstract = abstract
        self.publication_type = publication_type

    def get_date(self):
        return self.date

    def get_titre(self):
        return self.titre

    def get_abstract(self):
        return self.abstract

    def get_publication_type(self):
        return self.publication_type


def api_pubmed():
    # Request_for_QK_&_WE
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=congenital+myopathy&retmode=json&usehistory=y')
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
    parent_dir = "/Users/hugues.escoffier/PycharmProjects/TextMining_MC"
    path = os.path.join(parent_dir, dir)
    try:
        os.mkdir(path)
    except:
        print("Already_C")
    list_id_100 = []
    str_id_100 = str()
    number_file = 1
    for elmt in tqdm(iterable=id_all, desc='download_xml'):
        if len(list_id_100) == 100:
            # print(str_id_100)
            urlfetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+str(str_id_100)+"&retmode=xml"
            # print(urlfetch)
            all1_art = requests.get(urlfetch)
            dict_all1_art = xmltodict.parse(all1_art.content)
            arti_cle = open(path + "/article " + str(number_file), "w+")
            arti_cle.write(str(dict_all1_art))
            arti_cle.close()
            list_id_100.clear()
            list_id_100.append(elmt)
            str_id_100 = str(elmt) + ","
            number_file += 1
        else:
            list_id_100.append(elmt)
            str_id_100 = str_id_100 + str(elmt) + ","
    urlfetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+str(str_id_100)+"&retmode=xml"
    # print(urlfetch)
    all1_art = requests.get(urlfetch)
    dict_all1_art = xmltodict.parse(all1_art.content)
    arti_cle = open(path + "/article " + str(number_file), "w+")
    arti_cle.write(str(dict_all1_art))
    arti_cle.close()


# api_pubmed()


def work():
    url_ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=33602879,33811133&retmode=xml"
    # url_ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34129875,34120822,34117073,34112090,34106991,34103343,34087854,34068508,34066362,34066119,34058744,34053846,20301480,34033812,33994094,33985321,33977145,33972922,33964023,33963534,33940562,33940157,33933294,33926564,33926407,33923914,33922911,33919826,33917608,33916195,33909041,33898094,33889622,33869891,33860760,33851717,33849607,33811133,33808002,33799993,33775046,33772159,33768912,33762497,33755597,33750322,33748842,33742414,33740643,33731536,33728321,33715228,33713125,33706403,33694278,33693846,33678976,33672664,33671084,33667896,33660968,33659639,33658649,33655926,33649036,33646172,33644647,33642296,33622753,33618039,33610554,33605127,33604899,33602879,33596003,33569209,33558124,33547108,33539007,33530378,33529318,33522658,33513091,33497766,33478553,33476211,33459893,33458580,33458578,33454021,33449170,33441455,33435938,33410539,33407688,33397769,33397003,33396724,33389762,33384202,&retmode=xml"
    url__ = requests.get(url_)
    data_ = xmltodict.parse(url__.content)
    # print(data_)
    PubmedArticle = data_["PubmedArticleSet"]["PubmedArticle"]
    dir = "Art_per"
    parent_dir = "/Users/hugues.escoffier/PycharmProjects/TextMining_MC"
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
        try :
            id_art_one = inf_["MedlineCitation"]["PMID"]["#text"]
        except:
            try :
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
        y = 0
        try:
            for abs_tract in inf_["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]:
                    abs_part = abs_tract["#text"]
                    abstract_art = abstract_art + abs_part + "\n"
                    y += 1
        except:
            try:
                if y == 0:
                    abstract_art = inf_["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]["#text"]
            except:
                try:
                    if y == 0:
                        abstract_art = inf_["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
                except:
                    x = 0
        if abstract_art == "":
            abstract_art = "None"
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


work()


def e_summary():
    rob = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=congenital+myopathy&retmode=json&usehistory=y')
    # print(rob.status_code)
    all_rob = rob.json()
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
