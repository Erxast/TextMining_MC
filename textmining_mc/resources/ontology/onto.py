import os

from textmining_mc import configs
from textmining_mc.resources.utils.superbasemodel import DatabaseModel


class Ontology(DatabaseModel):
    def __init__(self, data_name):
        self.root_data_path = configs['paths']['data']['root']
        database_path = os.path.join(self.root_data_path, data_name)
        super().__init__(database_path)

    def from_txt(self):
        fichier = open(os.path.join(self.root_data_path, 'KW_.twt'), 'r')
        list_ligne = []
        ligne = ''
        for i in fichier.read():
            if i == '\n':
                list_ligne.append(ligne)
                ligne = ''
            else:
                ligne += i
            fichier.close()
        print(list_ligne)

    def run(self):
        self.from_txt()


if __name__ == '__main__':
    print('start')
    p = Ontology('classification')
    p.run()
    print('end')
