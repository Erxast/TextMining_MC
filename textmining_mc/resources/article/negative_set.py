import os

import pandas
import pandas as pd
import requests
import random
import spacy
import pprint
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from collections import Counter
from Bio import Entrez
from tqdm import tqdm

from textmining_mc import configs
from textmining_mc.resources.model import Article, NArticle, AllAnnotation, NAnnotation
from textmining_mc.resources.utils import database


class NegativeSet(object):
    def __init__(self):
        self.list_all = []
        self.dataframe_word = pd.DataFrame

    @staticmethod
    def annotation_article():
        """
        Annotate all articles via Pubtator annotations
        :return:
        """
        count = 0
        list_article_id = []
        list_annotation = []
        query = NArticle.select()
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
                NAnnotation.insert_many(list_annotation,
                                        fields=[NAnnotation.pmid, NAnnotation.mention, NAnnotation.bioconcept,
                                                NAnnotation.identifier]).execute()
                list_annotation.clear()
                count = 0
        NAnnotation.insert_many(list_annotation, fields=[NAnnotation.pmid, NAnnotation.mention, NAnnotation.bioconcept,
                                                         NAnnotation.identifier]).execute()

    def spacy_frequency_neg(self):
        """

        Returns:

        """
        nlp = spacy.load("en_core_web_sm")
        list_word = []
        for article in NArticle.select():
            doc_title = nlp(article.title)
            doc_abstract = nlp(article.abstract)
            for token in doc_title:
                if not token.is_stop and not token.is_punct and not token.like_num:
                    list_word.append(token.lemma_)
            for token in doc_abstract:
                if not token.is_stop and not token.is_punct and not token.like_num:
                    list_word.append(token.lemma_)
        word_freq = Counter(list_word)
        dataframe_word = pd.DataFrame.from_dict(word_freq, orient='index').reset_index()
        self.dataframe_word = dataframe_word.rename(columns={'index': 'word', 0: 'counts'})
        self.dataframe_word.to_csv(path_or_buf=os.path.join(configs['paths']['data']['root'], 'df_ns_csv'), index=False)

    def ns_wordcloud(self):
        df = pandas.read_csv(filepath_or_buffer=os.path.join(configs['paths']['data']['root'], 'df_ns_csv'))
        d = {}
        for a, x in df.values:
            d[a] = x
        wordcloud = WordCloud(background_color='white')
        wordcloud.generate_from_frequencies(frequencies=d)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def run(self):
        # self.count_years()
        # self.selection_article()
        # self.annotation_article()
        self.spacy_frequency_neg()
        # self.ns_wordcloud()


if __name__ == '__main__':
    print('start')
    NegativeSet().run()
    print('end')
