import os
import datetime
from peewee import SqliteDatabase, Model, CharField, IntegerField, \
    FloatField, DateTimeField, fn

__dir, _ = os.path.split(__file__)

db = SqliteDatabase(os.path.join(__dir, 'data/verbal_read.db'))

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
        # frr = datetime.datetime.combine(fr, datetime.time.min)
        # too = datetime.datetime.combine(fr, datetime.time.max)
        return Word.select().where(~Word.last_modify.is_null()).\
            where(Word.last_modify.year>=fr.year).\
            where(Word.last_modify.month>=fr.month).\
            where(Word.last_modify.day>=to.day).\
            where(Word.last_modify.year<=to.year).\
            where(Word.last_modify.month<=to.month).\
            where(Word.last_modify.day<=to.day)

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
            print('==== review today ({}) ===='.format(ws.count()))
            ws = ws.order_by(fn.random())
            print_ws(ws, False)
        else:
            print('==== new today ====')
            ws = Word.select().where(Word.last_modify.is_null()).\
                order_by(((Word.count-0.8) * Word.id).desc(), Word.id.desc()).\
                limit(65)
            print_ws(ws, True)


    def task_for_review():
        cr = (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 15)
        cr = [datetime.datetime.now().date()-datetime.timedelta(days=i) for i in cr]
        cr = [i.year*10000+i.month*100+i.day for i in cr]

        # how does peewee support |(col1, col2) << ((a,b), (c,d))| ?
        ws = Word.select().\
                where(~Word.last_modify.is_null()). \
                where((Word.last_modify.year*10000+Word.last_modify.month*100+Word.last_modify.day) << cr).\
                order_by(Word.last_modify.desc(), fn.random())

        print_ws(ws, False)

    def stop_watch():
        import time
        import os
        os.system('cls')
        delta = 0
        def strstr(d):
            m = d // 60
            s = d - m * 60
            return '{:0>2d} : {:0>2d}'.format(m, s)
        while True:
            print('\r' + strstr(delta) + '        ', end='')
            time.sleep(1.0)
            delta += 1

    import fire
    fire.Fire({'today': task_for_today, 'review': task_for_review, 'time': stop_watch})
    # write_csv()
    # change_brief_to_colins()


