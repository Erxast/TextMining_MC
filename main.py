class MyArticle(object):
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)

        
a1 = MyArticle("TOTO")

a1.print_name()
