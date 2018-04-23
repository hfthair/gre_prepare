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


def save(title, pron, brief, detail):
    finds = Word.select().where(Word.title == title)
    if finds:
        find = finds[0]
        find.inc()
        find.save()
    else:
        find = Word(title=title, pron=pron, brief=brief, full=detail)
        find.save()

with db:
    if not Word.table_exists():
        Word.create_table(True)

db.connect()

if __name__ == '__main__':

    def change_brief_to_colins():
        from iciba import colins_to_brief
        for w in Word.select():
            c = w.full
            if c and len(c) > 3:
                b = colins_to_brief(c)
                if b:
                    print('modify. ' + w.title)
                    w.brief = b
                    w.save()

    def write_csv():
        import pandas as pd
        id = []
        title = []
        brief = []

        for w in Word.select():
            id.append(w.id)
            title.append(w.title)
            brief.append(w.brief)

        df = pd.DataFrame({'id':id, 'title':title, 'brief':brief})

        writer = pd.ExcelWriter('../read.xlsx')
        df.to_excel(writer, index=False)
        writer.save()

    def mprint():
        from colorama import init, Fore, Style
        init()
        def printw(w):
            t = w.title + ' ' * 15
            t = t[:15]
            print(Fore.GREEN + t + Fore.RESET + ' | '.join(w.brief.splitlines()), end='')

        for w in Word.select().order_by((Word.count * Word.id).desc()):
            printw(w)
            q = input()
            if q == 'q':
                break


    mprint()
    # write_csv()
    # change_brief_to_colins()


