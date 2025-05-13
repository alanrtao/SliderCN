from os import path, listdir
from textwrap import indent
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

import csv

from dataclasses import dataclass

font_latin = './fusion-pixel-12px-proportional-latin.ttf'
font_zh = './fusion-pixel-12px-proportional-zh_hans.ttf'

fonts = (TTFont(font_latin), TTFont(font_zh))
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

def char_not_in_fonts(c: str):
    u = ord(c)

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
                    if char_not_in_fonts(c):
                        log_curr_error(f'Character not supported by font `{c}`')
                
        
