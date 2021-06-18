import requests
import xmltodict
import os
from tqdm import tqdm
from Bio import Entrez
from peewee import *


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
    # id_list = ['32991557', '32991555', '32900739']
    # id_list = ['34129875', '34120822', '34117073', '34112090']
    # id_list = ['34129875', '34120822', '34117073', '34112090', '34106991', '34103343', '34087854', '34068508', '34066362', '34066119', '34058744', '34053846', '20301480', '34033812', '33994094', '33985321', '33977145', '33972922', '33964023', '33963534', '33940562', '33940157', '33933294', '33926564', '33926407', '33923914', '33922911', '33919826', '33917608', '33916195', '33909041', '33898094', '33889622', '33869891', '33860760', '33851717', '33849607', '33811133', '33808002', '33799993', '33775046', '33772159', '33768912', '33762497', '33755597', '33750322', '33748842', '33742414', '33740643', '33731536']
    # id_list = ['33031641', '33030289', '33009919', '33000450', '32994313', '32994279', '32991557', '32991555', '32987629', '32978031', '32939402', '32936536', '32925083', '32921128', '32919980', '32910616', '32902138', '32900739', '32887649', '32865794', '32862205', '32849172', '32847583', '32844998', '32833721', '32827036', '32826616', '32826339', '32823742', '32820518', '32819427', '32818658', '32818283', '32817686', '32815147', '32812332', '32809353', '32809972', '32808237', '32805447', '32799913', '32797717', '32796201', '32793522', '32793418', '32791556', '32788656', '32788638', '32778822', '32777938']
    id_list = ['33382107', '33376055', '33354762', '33351248', '33343299', '33341951', '33337382', '33333461', '33331696', '33325393', '33309881', '33307294', '33304817', '33303358', '33294969', '33288130', '33277420', '33277141', '33272829', '33265937', '33256785', '33255644', '33250842', '33246213', '33244741', '33235377', '33200426', '33193651', '33190635', '33184643', '33176865', '33166523', '33164942', '33164824', '33137814', '33136893', '33131661', '33129849', '33127292', '33124102', '33120694', '33113016', '33112424', '33103395', '33097808', '33076971', '33075681', '33066566', '33064836', '33037480']
    handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml", rettype="abstract")
    records = Entrez.read(handle)
    for i in range(len(id_list)):
        # print(i)
        # print("Article ID: ", id_list[i])
        # pprint(records["PubmedArticle"][i]["MedlineCitation"]["Article"])
        try:
            abstract_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
        except:
            print(id_list[i])
        # title_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["ArticleTitle"])
        # publication_type_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["PublicationTypeList"])
        # pprint(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"])
        # print(title_)
        # print(publication_type_)
        # print(abstract_)


# solution_by_corentin()


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


def final_():
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


# final_()


def url_generator():
    url_str = ""
    # url_list = ['33277141', '31060720', '297409383', '27519468', '21073836', '12689691', '11801394', '10665483', '10553983', '8446135']
    # url_list = ['33909041', '33731536', '27519468', '22172415', '21073836', '12689691', '11801394', '10665483', '10553983', '8446135']
    url_list = ['33246213', '33244741', '33235377', '33200426', '33193651']
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
    print(len(id_all))


def ft_peewee_():

    #DataBase_C
    db = SqliteDatabase('article.db')

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
    all_rob = rob.json()
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
    db = SqliteDatabase('article.db')

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
                        date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"])
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
                date_ = ''.join(records["PubmedArticle"][i]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"])
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


def database_search():
    db = SqliteDatabase('article.db')

    class Article(Model):
        id = CharField()
        title = CharField()
        date = CharField()
        type = CharField()
        abstract = CharField()

        class Meta:
            database = db
    db.create_tables([Article])
    query = Article.select()
    print(len(query))
    i = 0
    for arti in query:
        # print(arti.id)
        i += 1
    print(i)
    db.close()


database_search()

