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


def get_pubtator_annotation():
    """
    Annotate all articles via Pubtator annotations

    :return:
    """
    list_article_id = []
    list_annotation = []
    query = FArticle.select()
    for article in query:
        list_article_id.append(article.id)
    for art_id in tqdm(iterable=list_article_id, desc='annotation'):
        for annot in AllAnnotation.select().where(AllAnnotation.id == str(art_id)):
            mention = annot.mention
            bioconcept = annot.bioconcept
            identifier = annot.identifier
            tuple_annot = (str(art_id), mention, bioconcept, identifier)
            list_annotation.append(tuple_annot)
        FAnnotation.insert_many(list_annotation, fields=[FAnnotation.pmid, FAnnotation.mention, FAnnotation.bioconcept,
                                                        FAnnotation.identifier]).execute()
        list_annotation.clear()


get_scispacy_annotation()
get_pubtator_annotation()


