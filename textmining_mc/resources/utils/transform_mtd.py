import spacy
from peewee import SqliteDatabase
from tqdm import tqdm
import sqlite3

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
    list_article_id = []
    list_annotation = []
    query = Article.select()
    for article in query:
        list_article_id.append(article.id)
    for art_id in tqdm(iterable=list_article_id, desc='annotation'):
        for annot in AllAnnotation.select().where(AllAnnotation.id == str(art_id.id)):
            mention = annot.mention
            bioconcept = annot.bioconcept
            identifier = annot.identifier
            tuple_annot = (str(art_id.id), mention, bioconcept, identifier)
            list_annotation.append(tuple_annot)
        Annotation.insert_many(list_annotation, fields=[Annotation.pmid, Annotation.mention, Annotation.bioconcept,
                                                        Annotation.identifier]).execute()
        list_annotation.clear()


def intersection():
    list_joint_pmids = []
    list_pmids_gene = []
    query_pmids_gene = PmidsGene.select()
    for pmids in query_pmids_gene:
        list_pmids_gene.append(pmids.id)
    list_pmids_mc = []
    query_pmids_mc = Article.select()
    for pmids in query_pmids_mc:
        list_pmids_mc.append(pmids.id)
    for i in list_pmids_gene:
        if i in list_pmids_mc:
            list_joint_pmids.append(i)
    print(list_joint_pmids)
