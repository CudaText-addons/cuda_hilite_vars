import os
import re
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_hilite_vars.ini')

MAX_CONFIG_SECTIONS = 30
MYTAG = 202 # uniq int for all ed.attr plugins

_theme = app_proc(PROC_THEME_SYNTAX_DATA_GET, '')

def _theme_item(name):
    for i in _theme:
        if i['name']==name:
            return i['color_font']
    return 0x808080


config = {}
config['Bash script'] = {
    're_str': r'''("|')(\\\\|\\\1|.)*?\1''',
    're_var': r'\$\w+|\$\{.*?\}',
    'color_id': 'IdVar',
    }


def load_config():
    global config
    for i in range(MAX_CONFIG_SECTIONS):
        s = str(i)
        lexer = ini_read(fn_config, s, 'lexer', '')
        if not lexer: continue
        regex_str = ini_read(fn_config, s, 'regex_str', '')
        if not regex_str: continue
        regex_var = ini_read(fn_config, s, 'regex_var', '')
        if not regex_var: continue
        color = ini_read(fn_config, s, 'color', '')
        if not color: continue
        config[lexer] = {
            're_str': regex_str,
            're_var': regex_var,
            'color_id': color,
            }

    for key in config.keys():
        c = config[key]
        c['color_int'] = _theme_item(c['color_id'])
        c['o_str'] = re.compile(c['re_str'], re.I)
        c['o_var'] = re.compile(c['re_var'], re.I)


def save_config():
    global config
    for (i, key) in enumerate(config.keys()):
        s = str(i)
        ini_write(fn_config, s, 'lexer', key)
        ini_write(fn_config, s, 'regex_str', config[key]['re_str'])
        ini_write(fn_config, s, 'regex_var', config[key]['re_var'])
        ini_write(fn_config, s, 'color', config[key]['color_id'])


def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'


class Command:

    def __init__(self):

        load_config()

    def config(self):

        if not os.path.isfile(fn_config):
            save_config()

        if os.path.isfile(fn_config):
            file_open(fn_config)
        else:
            msg_status('Config file not found')


    def on_change_slow(self, ed_self):
        self.work(ed_self)

    def on_lexer(self, ed_self):
        self.work(ed_self)

    def on_open(self, ed_self):
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
