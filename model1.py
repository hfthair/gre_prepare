from peewee import SqliteDatabase, Model, CharField, IntegerField, FloatField, fn

db = SqliteDatabase('verbal1.db')

class Word(Model):
    title = CharField(unique=True)
    brief_3000 = CharField(max_length=1024, default='')
    full_3000 = CharField(max_length=1024, default='')
    pronunc = CharField(default='')
    iciba = CharField(max_length=1024, default='')
    colins_iciba = CharField(max_length=2048, default='')
    merriam = CharField(max_length=2048, default='')
    merriam_eg = CharField(max_length=2048, default='')

    count = FloatField(default=1.0)
    class Meta:
        database = db

    def brief(self):
        return self.brief_3000 if self.brief_3000 else self.iciba

    def full(self):
        return self.full_3000 if self.full_3000 else self.colins_iciba

    def by(self):
        return 'GRE3000' if self.brief_3000 else 'iciba'


class GreWord(Word):

    @staticmethod
    def ran(cnt):
        return GreWord.select().order_by((fn.random()*GreWord.count).desc()).limit(cnt)

    @staticmethod
    def save_or_update(title):
        finds = GreWord.select().where(GreWord.title == title)
        if finds:
            find = finds[0]
            find.count = find.count + 1.0
            find.save()
        else:
            pass
            # find = T(title=title, brief=brief, iciba=detail, merriam='')
            # find.save()


class OtherWord(Model):

    @staticmethod
    def ran(cnt):
        return OtherWord.select().order_by((fn.random()*OtherWord.count).desc()).limit(cnt)

    @staticmethod
    def save_or_update(title):
        finds = OtherWord.select().where(OtherWord.title == title)
        if finds:
            find = finds[0]
            find.count = find.count + 1.0
            find.save()
        else:
            pass
            # find = T(title=title, brief=brief, iciba=detail, merriam='')
            # find.save()


with db:
    if not GreWord.table_exists():
        GreWord.create_table(True)
    if not OtherWord.table_exists():
        OtherWord.create_table(True)

db.connect()