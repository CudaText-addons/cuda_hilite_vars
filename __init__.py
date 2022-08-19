import os
import re
from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N


fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_hilite_vars.ini')

MYTAG = app_proc(PROC_GET_UNIQUE_TAG, '')

BASH_RE_STR = r'''("|')(\\.|.)*?\1'''
BASH_RE_VAR = r'\$\w+|\$\{.*?\}'

PYTHON_RE_STR = r'''f("|')(\\.|.)*?\1'''
PYTHON_RE_VAR = r'''\{.*?\}'''

PERL_RE_STR = r'''(["'`])(\\.|.)*?\1'''
PERL_RE_VAR = r'''[\$@%]\w+'''  # $scalar, @array, %hash (fm)

config = {
    'Bash script':
        {
        're_str': BASH_RE_STR,
        're_var': BASH_RE_VAR,
        'o_str': re.compile(BASH_RE_STR, re.I),
        'o_var': re.compile(BASH_RE_VAR, re.I),
        'color_id': 'String2',
        'color_int': 0xFF,
        },
    'Python':
        {
        're_str': PYTHON_RE_STR,
        're_var': PYTHON_RE_VAR,
        'o_str': re.compile(PYTHON_RE_STR, re.I),
        'o_var': re.compile(PYTHON_RE_VAR, re.I),
        'color_id': 'String2',
        'color_int': 0xFF,
        },
    'Perl':
        {
        're_str': PERL_RE_STR,
        're_var': PERL_RE_VAR,
        'o_str': re.compile(PERL_RE_STR, re.I),
        'o_var': re.compile(PERL_RE_VAR, re.I),
        'color_id': 'String2',
        'color_int': 0xFF,
        },
    }

theme = app_proc(PROC_THEME_SYNTAX_DICT_GET, '')

def get_color(name):

    global theme
    if name in theme:
        return theme[name]['color_font']
    return 0x808080


def load_config():

    global config
    sections = ini_proc(INI_GET_SECTIONS, fn_config)
    for s in sections:
        re_str = ini_read(fn_config, s, 'regex_str', '')
        if not re_str: continue
        re_var = ini_read(fn_config, s, 'regex_var', '')
        if not re_var: continue
        color = ini_read(fn_config, s, 'color', '')
        if not color: continue
        config[s] = {
            're_str': re_str,
            're_var': re_var,
            'o_str': re.compile(re_str, re.I),
            'o_var': re.compile(re_var, re.I),
            'color_id': color,
            'color_int': 0xFF,
            }


def update_colors():

    global config
    for key in config.keys():
        c = config[key]
        c['color_int'] = get_color(c['color_id'])


def save_config():

    global config
    for key in config.keys():
        val = config[key]
        ini_write(fn_config, key, 'regex_str', val['re_str'])
        ini_write(fn_config, key, 'regex_var', val['re_var'])
        ini_write(fn_config, key, 'color', val['color_id'])


class Command:

    def __init__(self):

        load_config()
        update_colors()

    def config(self):

        if not os.path.isfile(fn_config):
            save_config()

        if os.path.isfile(fn_config):
            file_open(fn_config)
        else:
            msg_status(_('Config file not found'))


    def on_change_slow(self, ed_self):

        self.work(ed_self)

    def on_lexer(self, ed_self):

        self.work(ed_self)

    def on_open(self, ed_self):

        update_colors() # do it in on_open to use current theme
        self.work(ed_self)


    def work(self, ed):

        global config
        lex = ed.get_prop(PROP_LEXER_FILE)
        if not lex in config:
            ed.attr(MARKERS_DELETE_BY_TAG, tag=MYTAG)
            return

        props = config[lex]
        o_str = props['o_str']
        o_var = props['o_var']
        ncolor = props['color_int']

        ed.attr(MARKERS_DELETE_BY_TAG, tag=MYTAG)

        for index in range(ed.get_line_count()):
            line = ed.get_text_line(index)
            if not line: continue

            for m in o_str.finditer(line):
                span_out = m.span()
                for mm in o_var.finditer(m.group()):
                    span_in = mm.span()
                    ed.attr(MARKERS_ADD,
                        tag = MYTAG,
                        x = span_in[0]+span_out[0],
                        y = index,
                        len = span_in[1]-span_in[0],
                        color_font = ncolor,
                        )
