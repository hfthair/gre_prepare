from peewee import SqliteDatabase, Model, CharField, IntegerField, fn

db = SqliteDatabase('verbal.db')

class Word(Model):
    title = CharField(unique=True)
    brief = CharField(max_length=1024)
    iciba = CharField(max_length=2048)
    merriam = CharField(max_length=2048, default='')
    s1 = CharField(max_length=2048, default='')
    s2 = CharField(max_length=2048, default='')
    s3 = CharField(max_length=2048, default='')
    s4 = CharField(max_length=2048, default='')
    count = IntegerField(default=1)
    class Meta:
        database = db

    @staticmethod
    def ran(cnt):
        return Word.select().order_by((fn.random()*Word.count).desc()).limit(cnt)

class Read(Model):
    title = CharField(unique=True)
    brief = CharField(max_length=1024)
    iciba = CharField(max_length=2048)
    merriam = CharField(max_length=2048, default='')
    s1 = CharField(max_length=2048, default='')
    s2 = CharField(max_length=2048, default='')
    s3 = CharField(max_length=2048, default='')
    s4 = CharField(max_length=2048, default='')
    count = IntegerField(default=1)
    class Meta:
        database = db

# class GreVerbalCq(Model):
#     title = CharField(unique=True)
#     show = CharField(max_length=2048)
#     brief = CharField(max_length=1024)
#     pron = CharField(max_length=256)
#     class Meta:
#         database = db

def save(T, title, brief, detail):
    finds = T.select().where(T.title == title)
    if finds:
        find = finds[0]
        find.count = find.count + 1
        find.save()
    else:
        find = T(title=title, brief=brief, iciba=detail, merriam='')
        find.save()


with db:
    if not Word.table_exists():
        Word.create_table(True)
    if not Read.table_exists():
        Read.create_table(True)

db.connect()