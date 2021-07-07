import os

from peewee import Model, CharField, ForeignKeyField, SqliteDatabase

from textmining_mc import database_proxy, logger, configs
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables, drop_proxy_db_tables

DEBUG = True

"""
On trouve ici la totalité des modèles pour les différentes db utilisées dans le programme
"""


class BaseModel(Model):
    class Meta:
        database = database_proxy  # Use proxy for our DB.

"""
Article/Annotation/Scispacy sont la db utilisée pour traiter l'ensemble des articles
"""


class Article(BaseModel):
    id = CharField()
    title = CharField()
    date = CharField()
    type = CharField()
    abstract = CharField()
    source = CharField()

    def insert_init_db(self):
        pass


#Sous classe Annotation
class Annotation(BaseModel):
    pmid = ForeignKeyField(Article, backref='annotation')
    mention = CharField()
    bioconcept = CharField()
    identifier = CharField()

    def insert_init_db(self):
        pass


class Scispacy(BaseModel):
    pmid = ForeignKeyField(Article, backref='scispacy')
    word = CharField()
    type = CharField()

    def insert_init_db(self):
        pass


def get_models_list():
    return [Article,
            Annotation,
            Scispacy]


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


def connect_db(name=database_proxy, db_type='sqlite',):
    connect_proxy_db(proxy=database_proxy, name=name, db_type=db_type)
    logger.info('Connection to the {} database {}: OK'.format(db_type, name))
    return database_proxy


def create_tables(force=False):
    create_proxy_db_tables(database_proxy, get_models_list(), force=force)


def delete_tables():
    drop_proxy_db_tables(database_proxy, get_models_list())
