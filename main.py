import requests
import xmltodict

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
    # print(id_all)
    # print(len(id_all)) = 9247
    for elmt in id_all:
        urlfetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+str(elmt)+"&retmode=xml"
        # print(urlfetch)
        all1_art = requests.get(urlfetch)
        dict_all1_art = xmltodict.parse(all1_art.content)
        abstract_ = dict_all1_art["PubmedArticleSet"]["PubmedArticle"]["MedlineCitation"]["Article"]["Abstract"]
        # print(abstract_)
        arti_cle = open("article "+str(elmt), "w+")
        arti_cle.write(str(abstract_))
        arti_cle.close()
        break


api_pubmed()
