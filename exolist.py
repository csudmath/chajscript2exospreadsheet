import os

class NumLevelError(Exception):
    pass

class ParseError(Exception):
    pass


def get_ex_label(line):
    if line.startswith(r'\begin{ex}\label{'):
        return line.split('label')[1].strip('{}')
    else:
        return ''

def begin_ex(line):
    return line.startswith(r'\begin{ex}')

def end_ex(line):
    return line.startswith(r'\end{ex}')

def begin_sol(line):
    return line.startswith(r'\begin{sol}')

def end_sol(line):
    return line.startswith(r'\end{sol}')

def begin_enum(line):
    return line.startswith(r'\begin{enumerate}')

def end_enum(line):
    return line.startswith(r'\end{enumerate}')

def enum_item(line):
    return line.startswith(r'\item')


class Counter(object):

    def __init__(self, initvalue, updater):
        self.initvalue = initvalue
        self.init()
        self.updater = updater

    def init(self):
        self.counter = self.initvalue

    def incr(self):
        self.counter = self.updater(self.counter)

    def __str__(self):
        return str(self.counter)





def exolist(chapter):
    latexfile = os.path.join("script-chaj", "chapitres", chapter + ".tex")

    exos = []
    parse_stack = []
    ex_structure = []
    label = ''
    num_level = 0
    in_exo = False
    in_sol = False
    counters = [
        # level 0 is a dummy level representing nothing interesting
        Counter(0, lambda x: 0),
        Counter(0, lambda x: x+1),
        Counter('a', lambda x: chr(ord(x)+1)),
    ]



    with open(latexfile, "r", encoding="utf-8") as fd:
        for line in fd:
            line = line.strip()
            if begin_ex(line):
                in_exo = True
                num_level = 0
                # capture the exercise number
                label = get_ex_label(line)

                # add exercise to exerise stack
                parse_stack += [('begin_ex', label)]

                print('"{}"'.format(label))

            elif end_ex(line):
                in_exo = False
                if not parse_stack[-1][0] == 'begin_ex':
                    raise ParseError
                else:
                    exos += {label : ex_structure}

            elif begin_sol(line):
                in_sol = True

            elif end_sol(line):
                in_sol = False

            elif begin_enum(line):
                if num_level > 1:
                    print("Trop de niveaux d'indentation")

                num_level += 1

            elif end_enum(line):
                if num_level > 0:
                    counters[num_level].init()
                    num_level -= 1
                else:
                    raise NumLevelError

            elif enum_item(line) and in_exo and not in_sol:
                counters[num_level].incr()
                print(';' * num_level, end="")
                print(counters[num_level])


if __name__ == '__main__':
    exolist('ensembles_nombres')
