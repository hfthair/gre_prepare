import sys

def iinput(msg):
    if 'win' in sys.platform:
        import msvcrt
        print(msg)
        r = msvcrt.getch().decode("utf-8").lower()
        return r
    else:
        return input(msg).lower()
