from peewee import SqliteDatabase, Model, CharField, IntegerField, FloatField, fn

db = SqliteDatabase('verbal_read.db')

class Word(Model):
    title = CharField(unique=True)
    count = FloatField(default=1.0)
    pron = CharField(default='')
    brief = CharField(default='')
    full = CharField(default='', max_length=2048)
    class Meta:
        database = db

    def inc(self):
        self.count += 1.0

    def dsc(self):
        self.count -= 0.3
        if self.count <= 0:
            self.count = 0

    @staticmethod
    def ran(cnt):
        return Word.select().order_by((fn.random()*Word.count).desc()).limit(cnt)

    @staticmethod
    def increase(title):
        ws = Word.select().where(Word.title==title)
        if ws:
            ws[0].inc()
            ws[0].save()

    @staticmethod
    def descrease(title):
        ws = Word.select().where(Word.title==title)
        if ws:
            ws[0].dsc()
            ws[0].save()

with db:
    if not Word.table_exists():
        Word.create_table(True)

db.connect()

if __name__ == '__main__':
    import time
    from model import Word as OW
    from iciba import search

    Word.drop_table()
    Word.create_table()

    c = 1
    for ow in OW.select():
        title = ow.title
        cnt = ow.count

        pron = ''
        brief = ''
        full = ''
        tc = 5
        while not brief and tc > 0:
            try:
                pron, brief, full = search(title)
            except:
                print('\n... fail --> ' + title)
            if not brief:
                time.sleep(0.7)
            tc = tc - 1

        ws = Word.select().where(Word.title==title)
        if ws:
            print('=== !!!{} duplicated'.format(title))
            w = ws[0]
            w.count += cnt
        else:
            w = Word(title=title, count=cnt, pron=pron, brief=brief, full=full)
        print('\r=== {} of {} saved            '.format(c ,title), end='')
        w.save()
        time.sleep(0.3)
        c = c + 1

