import os

import pandas as pd
import spacy
from matplotlib import pyplot as plt
from peewee import SqliteDatabase
from tqdm import tqdm
import sqlite3
from collections import Counter

from wordcloud import WordCloud

from textmining_mc import configs
from textmining_mc.resources.model import Article, Scispacy, Gene, AllAnnotation, PmidsGene, Annotation


def removal_false_positive():
    """
    Deletes articles without abstracts

    :return:
    db
    """
    for arti in Article.select():
        if arti.abstract == "None":
            arti.delete_instance()
        elif arti.type != "Journal Article":
            arti.delete_instance()


def get_scispacy_annotation():
    """
    Add the informations available via the pkg Scispacy for all_article db

    :return:
    """
    nlp = spacy.load("en_core_web_sm")
    scispacy_annotation = []
    for elmt in tqdm(iterable=Article.select(), desc='scispacy'):
        id = elmt.id
        title = elmt.title
        sci_title = nlp(title)
        for i in sci_title.ents:
            scispacy_annotation.append((id, i.text, i.label_))
        abstract = elmt.abstract
        sci_abstract = nlp(abstract)
        for i in sci_abstract.ents:
            scispacy_annotation.append((id, i.text, i.label_))
        Scispacy.insert_many(scispacy_annotation, fields=[Scispacy.pmid, Scispacy.word, Scispacy.type]).execute()
        scispacy_annotation.clear()


def get_list_gene_identifier():
    """
    We store all the pmids containing in their titles or abstracts at least
    one reference to one of the genes involved in congenital myopathies

    :return:
    """
    list_gene_identifier = []
    list_elmt = []
    query = Gene.select()
    for gene in query:
        list_gene_identifier.append(gene.id)
    for gene_ide in tqdm(iterable=list_gene_identifier, desc='pmids_gene'):
        query_bis = AllAnnotation.select().where(AllAnnotation.identifier == str(gene_ide))
        for elmt in query_bis:
            pmids = elmt.id
            gene_id = str(gene_ide)
            gene_name = elmt.mention
            tuple_list_id_gene = (pmids, gene_id, gene_name)
            list_elmt.append(tuple_list_id_gene)
        PmidsGene.insert_many(list_elmt, fields=[PmidsGene.id, PmidsGene.gene_id, PmidsGene.gene_name]).execute()
        list_elmt.clear()


def get_pubtator_annotation():
    """
    Annotate all articles via Pubtator annotations for all_annotation db

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
    i = 0
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
            Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
                                                    Annotation.identifier]).execute()
            list_annotation.clear()
            count = 0
    Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
                                                    Annotation.identifier]).execute()


def spacy_ps_ns():
    df_ns = pd.read_csv(filepath_or_buffer=os.path.join(configs['paths']['data']['root'], 'df_ns_csv'))
    df_ps = pd.read_csv(filepath_or_buffer=os.path.join(configs['paths']['data']['root'], 'df_ps_csv'))
    list_ps = []
    list_ns = []
    list_joint = []
    dict_joint = {}
    for word, count in df_ps.values:
        list_ps.append(word)
    for word, count in df_ns.values:
        list_ns.append(word)
    for ite in tqdm(iterable=list_ps, desc='common'):
        if ite not in list_ns:
            list_joint.append(ite)
    for ite in tqdm(iterable=list_joint, desc='add_to_df'):
        for word, count in df_ps.values:
            if word == ite:
                dict_joint[word] = count
                break
    dataframe_joint = pd.DataFrame.from_dict(dict_joint, orient='index').reset_index()
    dataframe_joint = dataframe_joint.rename(columns={'index': 'word', 0: 'counts'})
    dataframe_joint.to_csv(path_or_buf=os.path.join(configs['paths']['data']['root'], 'df_joint_csv'), index=False)


# spacy_ps_ns()


def joint_wordcloud():
    df = pd.read_csv(filepath_or_buffer=os.path.join(configs['paths']['data']['root'], 'df_joint_bis_csv'))
    d = {}
    for a, x in df.values:
        d[a] = x
    wordcloud = WordCloud(background_color='white')
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


# joint_wordcloud()

