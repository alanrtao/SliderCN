from os import path, listdir
from textwrap import indent
from fontTools.ttLib import TTFont

import csv

from dataclasses import dataclass

font_latin = 'fusion-pixel-12px-proportional-latin.ttf'
font_zh = 'fusion-pixel-12px-proportional-zh_hans.ttf'

parent = path.realpath(path.dirname(__file__))

header_row_count = 4 # format comments, config name, config val, column names

ban_characters = '。；，“”‘’……'

err_log = './errors.log'

@dataclass
class Record:
    path: str
    orig: str
    translation: str
    metadata: str

@dataclass
class FontDescriptor:
    path: str
    usage: set[str]

fonts: dict[TTFont, FontDescriptor] = { TTFont(p): FontDescriptor(p, set()) for p in (font_latin, font_zh) }

def char_in_font(c: str, f: TTFont) -> bool:
    cmaps = f['cmap'].tables
    for cm in cmaps:
        # if cm.isUnicode():
        if ord(c) in cm.cmap:
            fonts[f].usage.add(c)
            return True
    return False

def char_not_in_fonts(c: str) -> bool:
    for f in fonts.keys():
        if char_in_font(c, f): return False
    return True

with open(err_log, mode='w') as log_file:

    def printdup(*args, **kwargs) -> None:
        print(*args, **kwargs)
        print(*args, **kwargs, file=log_file)

    def log_error(msg: str, lineno: int, rec: Record):
        printdup(msg)
        printdup(lineno)
        printdup('Original:')
        printdup(indent(rec.orig, '  '))
        printdup('Translation:')
        printdup(indent(rec.translation, '  '))

    cmaps = []

    for csv_path in [path.join(parent, f) for f in listdir(parent) if f.endswith('.csv')]:
        with open(csv_path) as csv_file:
            r = csv.reader(csv_file)

            for i in range(header_row_count):
                next(r)
            
            for i, row in enumerate(r):
                rec = Record(*(row[:4]))

                def log_curr_error(msg: str): 
                    log_error(msg, i, rec)

                if rec.translation != '' and rec.translation.lstrip() == '':
                    log_curr_error('Nonempty whitespace line.')
                    continue

                if rec.translation == '' and rec.orig != '':
                    log_curr_error('Missing translation.')
                    continue
                
                for bc in ban_characters:
                    if bc in rec.translation:
                        log_curr_error(f'Character explicitly forbidden: `{bc}`')
                
                for c in rec.translation:
                    # skip whitespaces
                    if c.lstrip() == '':
                        continue
                    if char_not_in_fonts(c):
                        log_curr_error(f'Character not supported by font `{c}`')
                
        
for font, desc in fonts.items():
    with open(f'{desc.path}.log', mode='w') as w:
        for u in sorted(desc.usage):
            print(u, end='', file=w)