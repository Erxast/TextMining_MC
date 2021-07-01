from peewee import Model, CharField, ForeignKeyField

from textmining_mc import database_proxy, logger
from textmining_mc.resources.utils.database import connect_proxy_db, create_proxy_db_tables, drop_proxy_db_tables

DEBUG = True
db_name = 'article_mgt.db'


class BaseModel(Model):
    class Meta:
        database = database_proxy  # Use proxy for our DB.


class Article(BaseModel):
    id = CharField()
    title = CharField()
    date = CharField()
    type = CharField()
    abstract = CharField()

    def insert_init_db(self):
        pass


#Sous classe Annotation
class Annotation(BaseModel):
    pmid = ForeignKeyField(Article, backref='annotation')
    mention = CharField()
    bioconcept = CharField()
    identifiers = CharField()

    def insert_init_db(self):
        pass


class Scispacy(BaseModel):
    pmid = ForeignKeyField(Article, backref='scispacy')
    word = CharField()
    type = CharField()


def get_models_list():
    return [Article,
            Annotation,
            Scispacy]


def connect_db(name=db_name, db_type='sqlite',):
    connect_proxy_db(proxy=database_proxy, name=name, db_type=db_type)
    logger.info('Connection to the {} database {}: OK'.format(db_type, name))
    return database_proxy


def create_tables(force=False):
    create_proxy_db_tables(database_proxy, get_models_list(), force=force)


def delete_tables():
    drop_proxy_db_tables(database_proxy, get_models_list())
