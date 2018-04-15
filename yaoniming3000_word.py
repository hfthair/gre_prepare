
import attr

@attr.s
class Mean(object):
    cn = attr.ib(default='')
    en = attr.ib(default='')
    synonym = attr.ib(default='')
    antonym = attr.ib(default='')
    derive = attr.ib(default='')
    eg = attr.ib(default='')

@attr.s
class Word(object):
    title = attr.ib()
    brief = attr.ib()
    full = attr.ib()
    means = attr.ib(default=None)
    position = attr.ib(default=0)


def create_word(src):
    lines = src.splitlines()
    title, _ = lines[0].split('  ')

    means = []
    mean = None
    for line in lines[1:]:
        if line.startswith(' ♠'):
            mean = Mean()
            cn = line.split('：')[0].strip()
            mean.cn = cn[cn.index(' '):].strip()
            mean.en = line.replace(cn, '').strip()
            # mean.synonym = ''
            # mean.antonym = ''
            # mean.eg = ''
            # mean.derive = ''
            means.append(mean)
        elif line.startswith(' ♣近'):
            if mean.synonym != '':
                # some error of source
                mean.antonym = line.replace(' ♣近', '').strip()
                continue
            mean.synonym = line.replace(' ♣近', '').strip()
        elif line.startswith(' ♣反'):
            mean.antonym = line.replace(' ♣反', '').strip()
        elif line.startswith(' ♣例'):
            mean.eg = line.replace(' ♣例', '').strip()
        elif line.startswith(' ♣派'):
            mean.derive = line.replace(' ♣派', '').strip()

    brief = '\n'.join(i.cn for i in means)

    return Word(title, brief, src, means)