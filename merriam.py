import requests
from bs4 import BeautifulSoup


def html2text(html):
    for script in html(["script", "style"]):
        script.extract()
    text = html.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)

def search(word):
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
