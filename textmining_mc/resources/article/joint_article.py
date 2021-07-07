import spacy

from tqdm import tqdm

from textmining_mc.resources.model import FScispacy, FArticle, AllAnnotation, FAnnotation


def get_scispacy_annotation():
    """
    Add the informations available via the pkg Scispacy

    :return:
    """
    nlp = spacy.load("en_core_web_sm")
    scispacy_annotation = []
    for elmt in tqdm(iterable=FArticle.select(), desc='scispacy'):
        id = elmt.id
        title = elmt.title
        sci_title = nlp(title)
        for i in sci_title.ents:
            scispacy_annotation.append((id, i.text, i.label_))
        abstract = elmt.abstract
        sci_abstract = nlp(abstract)
        for i in sci_abstract.ents:
            scispacy_annotation.append((id, i.text, i.label_))
        FScispacy.insert_many(scispacy_annotation, fields=[FScispacy.pmid, FScispacy.word, FScispacy.type]).execute()
        scispacy_annotation.clear()


get_scispacy_annotation()


