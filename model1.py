from peewee import SqliteDatabase, Model, CharField, IntegerField, FloatField, fn

db = SqliteDatabase('verbal3000.db')

class Word(Model):
    title = CharField(unique=True)
    lid = IntegerField(default=0)
    count = FloatField(default=1.0)
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



if False:
    class Wordx(Model):
        title = CharField(unique=True)
        brief_3000 = CharField(max_length=1024, default='')
        full_3000 = CharField(max_length=1024, default='')
        list_of_book3000 = IntegerField(default=0)
        pronunc = CharField(default='')
        iciba = CharField(max_length=1024, default='')
        colins_iciba = CharField(max_length=2048, default='')
        merriam = CharField(max_length=2048, default='')
        eg_merriam = CharField(max_length=2048, default='')
        eg_3000 = CharField(max_length=2048, default='')

        count = FloatField(default=1.0)
        class Meta:
            database = db

        def brief(self):
            return self.brief_3000 if self.brief_3000 else self.iciba

        def full(self):
            return self.full_3000 if self.full_3000 else self.colins_iciba

        def by(self):
            return 'GRE3000' if self.brief_3000 else 'iciba'


    class GreWord(Wordx):

        @staticmethod
        def ran(cnt):
            return GreWord.select().order_by((fn.random()*GreWord.count).desc()).limit(cnt)

        @staticmethod
        def save_or_update(title, brief='', full='', lx=0):
            finds = GreWord.select().where(GreWord.title == title)
            if finds:
                find = finds[0]
                find.count = find.count + 1.0
                find.save()
            else:
                w = GreWord(title=title, brief_3000=brief, \
                    full_3000=full, list_of_book3000=lx)
                w.save()


    class OtherWord(Wordx):

        @staticmethod
        def ran(cnt):
            return OtherWord.select().order_by((fn.random()*OtherWord.count).desc()).limit(cnt)

        @staticmethod
        def save_or_update(title, brief='', full=''):
            finds = OtherWord.select().where(OtherWord.title == title)
            if finds:
                find = finds[0]
                find.count = find.count + 1.0
                find.save()
            else:
                w = OtherWord(title=title)
                gfinds = GreWord.select().where(GreWord.title == title)
                if gfinds:
                    gfind = gfinds[0]
                    w.brief_3000 = gfind.brief_3000
                    w.full_3000 = gfind.full_3000
                else:
                    w.iciba = brief
                    w.colins_iciba = full
                w.save()


    with db:
        if not GreWord.table_exists():
            GreWord.create_table(True)
        if not OtherWord.table_exists():
            OtherWord.create_table(True)

with db:
    if not Word.table_exists():
        Word.create_table(True)

db.connect()

if __name__ == '__main__':

    def mprint(iii):
        from colorama import init, Fore, Style
        from yaoniming3000 import wordByTitle
        init()
        def printw(w):
            t = w.title + ' ' * 15
            t = t[:15]
            ww = wordByTitle[w.title]
            print(Fore.GREEN + t + Fore.RESET + ' | '.join(ww.brief.splitlines()), end='')

        cnt = 0
        for w in Word.select().where(Word.lid==iii).order_by(Word.title):
            cnt += 1
            printw(w)
            q = input()
            if q == 'q':
                break
        print('----- {} ------'.format(cnt))

    import fire
    fire.Fire(mprint)

