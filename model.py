from peewee import SqliteDatabase, Model, CharField, IntegerField

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

with db:
    if not Word.table_exists():
        Word.create_table(True)
    if not Read.table_exists():
        Read.create_table(True)

db.connect()