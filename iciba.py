import requests
import json
from bs4 import BeautifulSoup

def colins_to_brief(c):
    brs = []
    for ti in c.splitlines():
        if ti and ti[0] >= '0' and ti[0] <= '9':
            b = ti.split(' ')
            if len(b) > 2:
                ty = b[1]
                if '-' in b[1]:
                    idx = b[1].index('-')
                    ty = b[1][:idx]
                b = [ty.lower()+'.'] + b[2:]
                br = ' '.join(b)
                brs.append(br)
    if brs:
        return '\n'.join(brs)


def search(word):
    word = '%20'.join(w for w in word.strip().split(' ') if w)
    c = requests.get('http://www.iciba.com/' + word, timeout=0.8)
    s = BeautifulSoup(c.text, "lxml")

    menu = None
    pron = None
    base = s.find(class_='in-base')
    if base:
        base_list = base.find(class_='base-list')
        if base_list:
            trans = base_list.find_all(class_='clearfix')
            lines = (i.get_text().replace('\n', ' ').replace('\r', '') for i in trans)
            menu = '\n'.join(lines)
            speak = base.find(class_='base-speak')
            if speak:
                pron = ' '.join(speak.get_text().splitlines())
                # sp = speak.find_all('span')
                # if sp and len(sp) >= 4:
                #     pron = sp[3].get_text().strip()
                #     if pron.startswith('美'):
                #         pron = pron.replace('美', '').strip()
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
                    colins = colins.strip()
                break
    if not pron:
        pron = ''
    if not colins or len(colins) < 5:
        colins = ''
    if colins:
        colins_br = colins_to_brief(colins)
        if colins_br:
            menu = colins_br

    return pron, menu, colins

def suggests(p, cnt=10):
    p = '%20'.join(w for w in p.strip().split(' ') if w)
    url = 'http://dict-mobile.iciba.com/interface/index.php?c=word&m=getsuggest&nums={}&timestamp=1&client=6&is_need_mean=1&word={}&_=12'
    c = requests.get(url.format(cnt, p), timeout=0.8)
    j = json.loads(c.text)
    if j['status'] != 1:
        raise Exception('website status wrong!')
    def means2str(m):
        return '\n'.join(i['part'] + ' ' + ', '.join(i['means']) for i in m)

    tmp = {msg['key']: means2str(msg['means']) for msg in j['message']}
    return tmp


if __name__ == '__main__':
    # a, b = search('novice')
    # print(a)
    x = search('suspicion')
    print(x)