import datetime
from peewee import SqliteDatabase, Model, CharField, IntegerField, \
    FloatField, DateTimeField, fn

db = SqliteDatabase('verbal_read.db')

class Word(Model):
    title = CharField(unique=True)
    count = FloatField(default=1.0)
    pron = CharField(default='')
    brief = CharField(default='')
    full = CharField(default='', max_length=2048)
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

    from colorama import init, Fore, Style
    init()

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

    def printw(w, cnt):
        t = w.title + ' ' * 15
        t = '({}) '.format(cnt) + t[:15]
        print(Fore.GREEN + t + Fore.RESET + ' | '.join(w.brief.splitlines()), end='')

    def get_data_of_day(fr, to):
        frr = datetime.datetime.combine(fr, datetime.time.min)
        too = datetime.datetime.combine(fr, datetime.time.max)
        return Word.select().where(Word.last_modify>frr and Word.last_modify<too)

    def print_ws(ws, touch):
        cnt = 0
        for w in ws:
            cnt += 1

            printw(w, cnt)
            q = input()
            if touch:
                w.touch()
            if q == 'q':
                break

    def task_for_today():
        ws = get_data_of_day(datetime.date.today(), datetime.date.today())

        if ws.count() > 30:
            ws = ws.order_by(fn.random())
            print_ws(ws, False)
        else:
            ws = Word.select().where(Word.last_modify==None).limit(65).\
                order_by(((Word.count-0.8) * Word.id).desc(), Word.id.desc())
            print_ws(ws, True)


    def task_for_review():
        cr = (1, 2, 3, 5)
        cr = [datetime.datetime.now().date()-datetime.timedelta(days=i) for i in cr]
        cr = [(i.year, i.month, i.day) for i in cr]
        print(cr)

        # not work!!!
        ws = Word.select().\
                where(Word.last_modify!=None and \
                (Word.last_modify.year, Word.last_modify.month, Word.last_modify.day) in cr).\
                order_by(Word.last_modify.desc(), fn.random())

        print_ws(ws, False)


    import fire
    fire.Fire({'new': task_for_today, 'review': task_for_review})
    # write_csv()
    # change_brief_to_colins()


