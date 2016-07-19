import os
import re

import xlsxwriter

class NumLevelError(Exception):
    pass

class ParseError(Exception):
    pass


def get_ex_label(line, lineno=None, chapter=None):
    # regular expression
    regex = r"^\s*\\begin\{\s*ex\s*\}\s*\\label\{(?P<label>\d+.\d+)\}.*$"
    m = re.match(regex, line)
    if m:
        return m.group('label')
    else:
        print(line)
        print("Unable to extract label at line for exo at line", lineno, "of file", chapter + ".tex")
        return None


def begin_ex(line, lineno=None, chapter=None):
    return line.startswith(r'\begin{ex}')

def end_ex(line, lineno=None, chapter=None):
    return line.startswith(r'\end{ex}')

def begin_sol(line, lineno=None, chapter=None):
    return line.startswith(r'\begin{sol}')

def end_sol(line, lineno=None, chapter=None):
    return line.startswith(r'\end{sol}')

def begin_enum(line, lineno=None, chapter=None):
    return line.startswith(r'\begin{enumerate}')

def end_enum(line, lineno=None, chapter=None):
    return line.startswith(r'\end{enumerate}')

def enum_item(line, lineno=None, chapter=None):
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





def exolist(wb, ws, chapter):
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
        bg_black = wb.add_format()
        bg_black.set_pattern(1)  # This is optional when using a solid fill.
        bg_black.set_bg_color('black')

        header = wb.add_format({'bold': True, 'font_color': 'black', 'align' : 'center'})
        title = wb.add_format({'bold': True, 'font_size': 20})
        subtitle = wb.add_format({'bold': True, 'font_size': 18})

        # largeur des colonnes
        ws.set_column(0, 2, 5)


        ws.write(0, 0, "Exercices du chapitre ", title)
        ws.write(0, 4, chapter, subtitle)
        ws.write(1, 0, "No Exo", header)
        ws.write(1, 1, "item", header)
        ws.write(1, 2, "sous-item", header)
        for i, prof in enumerate(profs):
            ws.write(1, 3+i, prof, header)
        xlsline = 2



        for lineno, line in enumerate(fd):
            line = line.strip()
            if begin_ex(line):
                in_exo = True
                num_level = 0
                # capture the exercise number
                label = get_ex_label(line, lineno, chapter)

                # add exercise to exerise stack
                parse_stack += [('begin_ex', label)]

                ws.write(xlsline, 0, str(label))
                ws.write(xlsline, 1, "", bg_black)
                ws.write(xlsline, 2, "", bg_black)
                xlsline += 1

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

            elif begin_enum(line) and in_exo:
                if num_level > 1:
                    print("Trop de niveaux d'indentation : ", num_level, "line", lineno)
                    print(latexfile)

                num_level += 1

            elif end_enum(line) and in_exo:
                if num_level > 0:
                    counters[num_level].init()
                    num_level -= 1
                else:
                    raise NumLevelError

            elif enum_item(line) and in_exo and not in_sol:
                counters[num_level].incr()
                ws.write(xlsline, num_level, str(counters[num_level]))
                ws.write(xlsline, 0, "", bg_black)
                if num_level == 1:
                    ws.write(xlsline, 2, "", bg_black)
                elif num_level == 2:
                    ws.write(xlsline, 1, "", bg_black)
                xlsline += 1


def get_chapter_list():
    return [
        'ensembles_nombres',
        'calcul_algebrique',
        'equations',
        'systemes',
    ]

def main():
    chapters = get_chapter_list()
    output = "output.xlsx"

    workbook = xlsxwriter.Workbook(output)
    for chapter in chapters:
        worksheet = workbook.add_worksheet(chapter)
        exolist(workbook, worksheet, chapter)

    workbook.close()

profs = '''
SCYJ
CHAR
AEBE
CLEC
GALM
MONC
'''

profs = list(filter(lambda x: x != '', profs.split('\n')))

if __name__ == '__main__':
    main()
