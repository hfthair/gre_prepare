import datetime
from peewee import SqliteDatabase, Model, CharField, IntegerField, \
    FloatField, DateTimeField, fn

db = SqliteDatabase('verbal3000.db')

class Word(Model):
    title = CharField(unique=True)
    lid = IntegerField(default=0)
    count = FloatField(default=1.0)
    last_modify = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.last_modify = datetime.datetime.now()
        return super(Word, self).save(*args, **kwargs)

    def touch(self):
        self.save()

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
    from colorama import init, Fore, Style
    from yaoniming3000 import wordByTitle

    def mprint(iii):
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

