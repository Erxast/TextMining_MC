import os

from peewee import Model, CharField, ForeignKeyField, IntegerField, SqliteDatabase

from textmining_mc import database_proxy, logger, configs
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables, drop_proxy_db_tables
from textmining_mc import configs

DEBUG = True

"""
On trouve ici la totalité des modèles pour les différentes db utilisées dans le programme
"""


class BaseModel(Model):
    class Meta:
        database = database_proxy  # Use proxy for our DB.


"""

"""

db_all = SqliteDatabase(os.path.join(configs['paths']['data']['root'], 'project'))


# KW
class HistopathKw(Model):
    # id = CharField()
    name = CharField()
    category = CharField()
    histological_feature = CharField()


    def insert_init_db(self):
        pass


# Syno. KW
class KwSynonyms(Model):
    # id = CharField()
    id_histopath_kw = ForeignKeyField(HistopathKw, backref='kw_synonyms')
    alias = CharField()

    def insert_init_db(self):
        pass


# Pmids article/KW
class ArticleKw(Model):
    id_article = CharField()
    id_histopath = ForeignKeyField(HistopathKw, backref='pmid_article')

    def insert_init_db(self):
        pass


# Article/inf
class Article(Model):
    id = ForeignKeyField(ArticleKw, backref='id_article')
    title = CharField()
    date = CharField()
    type = CharField()
    abstract = CharField()
    source = CharField()

    def insert_init_db(self):
        pass


# Pubtator annotation
class ArticleAnnotation(Model):
    id_article = ForeignKeyField(Article, backref='annotation')
    mention = CharField()
    bioconcept = CharField()
    identifier = CharField()


    def insert_init_db(self):
        pass


# class Scispacy(BaseModel):
#     pmid = ForeignKeyField(article, backref='scispacy')
#     word = CharField()
#     type = CharField()
#
#     def insert_init_db(self):
#         pass


def get_models_list():
    return [HistopathKw,
            KwSynonyms,
            ArticleKw,
            Article,
            ArticleAnnotation]


"""
FArticle/FAnnotation/FScispacy sont la db contenant les articles sur les gènes impliquées dans les MC 
"""

db_f = SqliteDatabase(os.path.join(configs['paths']['data']['root'], 'article_joint'))


class FArticle(Model):
    id = CharField()
    title = CharField()
    date = CharField()
    type = CharField()
    abstract = CharField()
    source = CharField()

    class Meta:
        database = db_f


class FAnnotation(Model):
    pmid = ForeignKeyField(FArticle, backref='annotation')
    mention = CharField()
    bioconcept = CharField()
    identifier = CharField()

    class Meta:
        database = db_f


class FScispacy(Model):
    pmid = ForeignKeyField(FArticle, backref='scispacy')
    word = CharField()
    type = CharField()

    class Meta:
        database = db_f


db_f.create_tables([FArticle,
                    FAnnotation,
                    FScispacy])

"""
NArticle/NAnnotation/NScispacy correspond a la db contenant le negative set
"""

db_n = SqliteDatabase(os.path.join(configs['paths']['data']['root'], 'article_negative'))


class NArticle(Model):
    id = CharField()
    title = CharField()
    date = CharField()
    type = CharField()
    abstract = CharField()
    source = CharField()

    class Meta:
        database = db_n


class NAnnotation(Model):
    pmid = ForeignKeyField(FArticle, backref='annotation')
    mention = CharField()
    bioconcept = CharField()
    identifier = CharField()

    class Meta:
        database = db_n


class NScispacy(Model):
    pmid = ForeignKeyField(FArticle, backref='scispacy')
    word = CharField()
    type = CharField()

    class Meta:
        database = db_n


db_n.create_tables([NArticle,
                    NAnnotation,
                    NScispacy])
"""
AllAnnotation est la db qui contient l'ensemble des annotations pubtator sur les gènes 
"""

db = SqliteDatabase(os.path.join(configs['paths']['data']['root'], 'all_annotation'))


class AllAnnotation(Model):
    id = CharField()
    mention = CharField()
    bioconcept = CharField()
    identifier = CharField()

    class Meta:
        database = db


"""
Gene contient les 45 gènes impliquées dans les MC 
"""

db_s = SqliteDatabase(os.path.join(configs['paths']['data']['root'], 'geneID'))


class Gene(Model):
    id = CharField()
    name = CharField()
    uniprot = CharField()

    class Meta:
        database = db_s


"""
PmidsGene contient l'ensemble des pmids des articles qui traitent d'un gène impliqué dans les MC 
"""

db_t = SqliteDatabase(os.path.join(configs['paths']['data']['root'], 'pmids_gene'))


class PmidsGene(Model):
    id = CharField()
    gene_name = CharField()
    gene_id = CharField()

    class Meta:
        database = db_t


db_t.create_tables([PmidsGene])

"""
KeywordAnnotation stock les identifiants des genes et des maladies ainsi que leurs nobmre d'occurence
"""

db_k = SqliteDatabase(os.path.join(configs['paths']['data']['root'], 'keyword'))


class Keyword(Model):
    keyword = CharField()
    bioconcept = CharField()
    identifier = CharField()
    mention = CharField()

    class Meta:
        database = db_k


db_k.create_tables([Keyword])


def connect_db(name=database_proxy, db_type='sqlite', ):
    connect_proxy_db(proxy=database_proxy, name=name, db_type=db_type)
    logger.info('Connection to the {} database {}: OK'.format(db_type, name))
    return database_proxy


def create_tables(force=False):
    create_proxy_db_tables(database_proxy, get_models_list(), force=force)


def delete_tables():
    drop_proxy_db_tables(database_proxy, get_models_list())
