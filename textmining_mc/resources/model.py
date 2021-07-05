from peewee import Model, CharField, ForeignKeyField, SqliteDatabase

from textmining_mc import database_proxy, logger
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables, drop_proxy_db_tables

DEBUG = True


class BaseModel(Model):
    class Meta:
        database = database_proxy  # Use proxy for our DB.


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


db = SqliteDatabase('/Users/hugues.escoffier/PycharmProjects/data/TextMining_MC_data/gene_pubtator')


class AllAnnotation(Model):
    id = CharField()
    mention = CharField()
    bioconcept = CharField()
    identifier = CharField()

    class Meta:
        database = db


db_s = SqliteDatabase('/Users/hugues.escoffier/PycharmProjects/data/TextMining_MC_data/geneID')


class Gene(Model):
    id = CharField()
    name = CharField()
    uniprot = CharField()

    class Meta:
         database = db_s


db_t = SqliteDatabase('/Users/hugues.escoffier/PycharmProjects/data/TextMining_MC_data/pmids_gene')


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
