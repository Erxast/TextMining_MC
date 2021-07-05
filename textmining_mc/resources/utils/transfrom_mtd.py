import spacy
from tqdm import tqdm

from textmining_mc.resources.model import Article, Scispacy


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