import os

from peewee import sqlite3
from tqdm import tqdm

from textmining_mc import configs
from textmining_mc.resources.model import BaseModel
from textmining_mc.resources.utils.superbasemodel import DatabaseModel
from textmining_mc.resources.utils.transform_mtd import removal_false_positive, get_scispacy_annotation


# class Pubtator(BaseModel):
#     id = CharField()
#     mention = CharField()
#     bioconcept = CharField()
#     identifier = CharField()
#
#     @staticmethod
#     def db_pubtator():
#         all_l = []
#         # Changer le path
#         with open("/Users/hugues.escoffier/Documents/Stage/gene2pubtatorcentral.txt", 'r') as fin:
#             for line in tqdm(iterable=fin, desc='reading'):
#                 cols = line.strip('\n').split('\t')
#                 a = (cols[0], cols[1], cols[2], cols[3])
#                 all_l.append(a)
#                 if len(all_l) == 990:
#                     AllAnnotation.insert_many(all_l, fields=[AllAnnotation.id, AllAnnotation.bioconcept, AllAnnotation.identifier, AllAnnotation.mention]).execute()
#                     all_l.clear()
#         c = 0
#         for i in range(0, 1000):
#             c += 1
#         AllAnnotation.insert_many(all_l, fields=[AllAnnotation.id, AllAnnotation.bioconcept, AllAnnotation.identifier, AllAnnotation.mention]).execute()
#
#     def run(self):
#         # TODO: Method populate Article
#         super().check_or_create_db()
#         self.db_pubtator()
#
#
# if __name__ == '__main__':
#     print('start')
#     p = Pubtator('gene_pubtator')
#     p.run()
#     print('end')

