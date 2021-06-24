import os

from textmining_mc import logger
from textmining_mc.resources.pubtator.model import create_tables, connect_db


class Pubtator(object):

    def __init__(self):
        self.dbh_proxy = None
        self.db_name = os.path.join('article_mgt1.db')
        self.db_type = 'sqlite'
        self.__check_or_create_db()
        # self.__connect_db()

    def __check_or_create_db(self):
        if not os.path.isfile(self.db_name):
            logger.warn('Database doest not exist!')
            logger.info('Downloading and creating sqlite database')

            # if not os.path.isdir(config['data_dir_path']):
            #     os.mkdir(config['data_dir_path'])

            self.dbh_proxy = connect_db(name=self.db_name,
                                        db_type=self.db_type,
                                        )

            # Create tables
            create_tables()
            logger.info('Creating database tables')
        else:
            self.dbh_proxy = connect_db(name=self.db_name,
                                        db_type=self.db_type,
                                        )

        return self.dbh_proxy

    # def __connect_db(self):
    #     self.dbh_proxy = connect_db(
    #         name=os.path.join(config['data_dir_path'], config['project'].lower()),
    #         db_type=config['database']['engine']
    #     )
    #     return self.dbh_proxy
    #
    # def __create_db(self):
    #     # Initialize database connection
    #     if not self.dbh_proxy:
    #         self.__connect_db()
    #
    #     # Create tables
    #     create_tables()
    #     logger.info('Creating database tables')
    #
    #     self.dbh_proxy.close()
    #
    # def generate_db(self):
    #     self.__connect_db()
    #     self.__create_db()
    #     self.dbh_proxy.close()

    def run(self):
        pass


if __name__ == '__main__':
    print('Start')
    p = Pubtator()
    p.run()
    print('END')
