#encoding=utf-8
import requests
from bs4 import BeautifulSoup

def __provider_name(func):
    def __dec(word):
        o = func(word)
        t = '* provide by ' + func.__name__ + ' *\n\n'
        return t + o
    return __dec

def html2text(html):
    for script in html(["script", "style"]):
        script.extract()
    text = html.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)

def iciba(word):
    word = '%20'.join(w for w in word.strip().split(' ') if w)
    c = requests.get('http://www.iciba.com/' + word, timeout=0.8)
    s = BeautifulSoup(c.text, "lxml")

    menu = None
    base = s.find(class_='in-base')
    if base:
        base_list = base.find(class_='base-list')
        if base_list:
            trans = base_list.find_all(class_='clearfix')
            lines = (i.get_text().replace('\n', ' ').replace('\r', '') for i in trans)
            menu = '\n'.join(lines)
        else:
            trans = base.find_all(class_='clearfix')
            lines = (i.get_text().replace('\n', ' ').replace('\r', '') for i in trans)
            raise Exception('\n'.join(lines))

    if not menu:
        raise Exception('Not Found.')

    colins = None
    cont = s.find(class_='js-main-content')
    if cont:
        articles = cont.find_all(class_='info-article')
        for article in articles:
            if article.get_text().strip().startswith('柯林斯'):
                inner = article.find(class_='article')
                if inner:
                    ens = inner.find_all(class_='family-english size-english prep-en')
                    for en in ens:
                        en.extract()

                    colins = ''
                    sections = inner.find_all(class_='section-prep')
                    for sec in sections:
                        sents = sec.find_all(class_='text-sentence')
                        egs = ''
                        for sent in sents:
                            en = sent.find(class_='family-english').get_text()
                            cn = sent.find(class_='family-chinese').get_text()
                            en = en.strip().replace('\n', '')
                            cn = cn.strip().replace('\n', '')
                            egs += '\n  * ' + en
                            egs += '\n    ' + cn
                            sent.extract()
                        tls = (tl.strip() for tl in sec.get_text().splitlines())
                        ti = ' '.join(t for t in tls if t)
                        colins += ti
                        colins += egs + '\n'
                        colins += '\n'
                break

    return menu, colins[:-1] if colins else ''

def merriam(word):
    c = requests.get('https://www.merriam-webster.com/dictionary/' + word, timeout=1.5)
    s = BeautifulSoup(c.text, "lxml")
    e = s.find(id='entry-1')

    if not e:
        exp = 'Not Found.'
        mis = s.find(class_='mispelled_word')
        if mis:
            li = s.find(class_='inner-box-wrapper')
            exp = html2text(li)
        raise Exception(exp)

    r = e.find(id='first-known-use-explorer')
    if r:
        r.extract()

    r = e.find(class_='link-cta-container')
    if r:
        r.extract()

    r = e.find(class_='uros')
    if r:
        r.extract()

    r = e.find(class_='vg-ins')
    if r:
        r.extract()

    out = html2text(e)

    return out

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

if __name__ == '__main__':
    from colorama import init, Fore, Style
    init(autoreset=True)

    val = False
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'word':
        val = True

    cache = {}
    while True:
        w = input('>>> ' if not val else '$$$ ')
        w = ''.join(x for x in w if x.lower()>='a' and x.lower()<='z' or x in ' -')
        if not w:
            print('q to quit')
            continue

        if w == 'q':
            break
        elif w == 'p':
            for x in cache:
                print(Fore.GREEN + x)
            continue
        elif w == 'r':
            for x in cache:
                print(Fore.GREEN + x + Fore.RESET + '\t' + cache[x])
            continue

        print(Fore.YELLOW + ' ' + w)
        print('===============' * 4)
        try:
            brief, detail = iciba(w)
            meaning = detail if detail else brief
            print(Fore.YELLOW + meaning)
            cache[w] = '|'.join(brief.splitlines())
            T = Read
            if val:
                T = Word
            d = T.select().where(T.title == w)
            if d:
                d[0].count = d[0].count + 1
                d[0].save()
            else:
                ww = T(title=w, brief=brief, iciba=detail, merriam='')
                ww.save()

        except Exception as e:
            print(Fore.RED + str(e))
        print('===============' * 4)
        print('')



