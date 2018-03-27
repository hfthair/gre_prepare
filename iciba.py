import requests
from bs4 import BeautifulSoup

def search(word):
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

