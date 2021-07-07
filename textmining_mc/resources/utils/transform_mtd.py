import spacy
from peewee import SqliteDatabase
from tqdm import tqdm
import sqlite3
from collections import Counter

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
    Add the informations available via the pkg Scispacy

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
            Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
                                                    Annotation.identifier]).execute()
            list_annotation.clear()
            count = 0
    Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
                                                    Annotation.identifier]).execute()


def spacy_frequency():
    nlp = spacy.load("en_core_web_sm")
    list_word = []
    count = 0
    for article in Article.select():
        count += 1
        doc_title = nlp(article.title)
        doc_abstract = nlp(article.abstract)
        for token in doc_title:
            if not token.is_stop and not token.is_punct:
                list_word.append(token.text)
        for token in doc_abstract:
            if not token.is_stop and not token.is_punct:
                list_word.append(token.text)
        if count == 100:
            break
    word_freq = Counter(list_word)
    print(word_freq)
    most_common = word_freq.most_common(10)
    print(most_common)