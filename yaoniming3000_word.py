
import attr




@attr.s
class Word(object):
    title = attr.ib()
    brief = attr.ib()
    full = attr.ib()
    position = attr.ib(default=0)


def create_word(src):
    lines = src.splitlines()
    title, pron = lines[0].split('  ')
    def get_briefs(line):
        t = line.split('：')[0].strip()
        t = t[t.index(' '):].strip()
        return t

    brief = '\n'.join(get_briefs(i) for i in lines[1:] if i.startswith(' ♠'))
    return Word(title, brief, src)