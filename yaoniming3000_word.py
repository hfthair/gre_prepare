
import attr

@attr.s
class Word(object):
    title = attr.ib()
    brief = attr.ib()
    full = attr.ib()
    position = attr.ib(default=0)
