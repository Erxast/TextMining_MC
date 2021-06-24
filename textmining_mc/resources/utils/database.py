# -*- coding: utf-8 -*-
import logging
import peewee
import sys

logger = logging.getLogger(__name__)


def connect_proxy_db(proxy, name, db_type='sqlite', host='localhost', user='', password='', port=3306):
    # Based on configuration, use a different database.
    if db_type == 'sqlite':
        db_name = '{}'.format(name)
        database = peewee.SqliteDatabase(db_name.format(name.lower()))
    elif db_type == 'mysql':
        database = peewee.MySQLDatabase(name, host=host, user=user, password=password, port=port)
    elif db_type == 'postgres':
        database = peewee.PostgresqlDatabase(name, host=host, user=user, password=password, port=port)
    else:
        database = peewee.SqliteDatabase(':memory:')

    proxy.initialize(database)
    proxy.connect()
    return proxy


def create_proxy_db_tables(proxy, models_list, force=False):
    msg = 'Creation of tables in database: '
    if force:
        drop_proxy_db_tables(proxy, models_list)
    try:
        proxy.create_tables(models_list, safe=True)

        # insert initial data
        for db in models_list:
            db().insert_init_db()

        logger.info(msg + 'OK')
    except peewee.DatabaseError as e:
        proxy.rollback()
        logger.error(msg + 'FAILED!')
        logger.error('PeeweeDatabase ERROR MSG : {}'.format(e))
        err_msg = '\n'.join(['[ERROR]: ' + msg + 'FAILED!', '[PeeweeDatabase ERROR]: ' + str(e)])
        exit(err_msg)


def drop_proxy_db_tables(proxy, models_list, ):
    msg = 'Deletion of tables in database: '
    try:
        proxy.drop_tables(reversed(models_list), safe=True, cascade=True)
        logger.info(msg + 'OK')
    except peewee.DatabaseError as e:
        proxy.rollback()
        logger.error(msg + 'FAILED!')
        logger.error('PeeweeDatabase ERROR MSG : {}'.format(e))
        err_msg = '\n'.join(['[ERROR]: ' + msg + 'FAILED!', '[PeeweeDatabase ERROR]: ' + str(e)])
        exit(err_msg)


def peewee_bulk_insert(peewee_db, model, data_source, verbose=False):
    """
    :param peewee_db:
    :param model:
    :param data_source:
    :param verbose:
    :return:
    """
    msg = 'Insertion of {} {} entries: '.format(len(data_source), model.__name__)
    try:
        with peewee_db.transaction():
            for idx in range(0, len(data_source), 1000):
                if verbose:
                    sys.stdout.write('\r' + msg + '{} %'.format((idx * 100) / len(data_source)))
                model.insert_many(data_source[idx:idx + 1000]).execute()

        peewee_db.commit()

        logger.debug(msg + 'OK')
    except peewee.DatabaseError as exp_msg:
        peewee_db.rollback()
        logger.error(msg + 'FAILED!')
        logger.error("PeeweeDatabase ERROR MSG : %s", exp_msg)
        err_msg = '\n'.join(['[ERROR]: ' + msg + 'FAILED!', '[PeeweeDatabase ERROR]: ' + str(exp_msg)])
        exit(err_msg)


def show_peewee_debug():
    """
    Activates the logging debug mode for Peewee
    :return: None
    """
    peewee_logger = logging.getLogger('peewee')
    peewee_logger.setLevel(logging.DEBUG)
