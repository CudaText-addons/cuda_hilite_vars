import os
from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N


fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_hilite_vars.ini')

MYTAG = app_proc(PROC_GET_UNIQUE_TAG, '')

BASH_RE_STR = r'''("|')(\\.|.)*?\1'''
BASH_RE_VAR = r'\$\w+|\$\{.*?\}'

PYTHON_RE_STR = r'''\bf("{1,3}|'{1,3})(\\.|.)*?\1'''
PYTHON_RE_VAR = r'''\{.*?\}'''

PERL_RE_STR = r'''(["'`])(\\.|.)*?\1'''
PERL_RE_VAR = r'''[\$@%]\w+'''  # $scalar, @array, %hash (fm)

config = {
    'Python':
        {
        'ch0': 'f',
        'ch1': '',
        'res_from': '{',
        'res_to': '}',
        'color_id': 'String2',
        },
    }

theme = app_proc(PROC_THEME_SYNTAX_DICT_GET, '')

def log(s):
    print('[HiVars]', s)
    

def get_color(name):

    global theme
    if name in theme:
        return theme[name]['color_font']
    return 0x808080


def load_config():

    global config
    sections = ini_proc(INI_GET_SECTIONS, fn_config)
    for s in sections:
        ch0 = ini_read(fn_config, s, 'ch0', '')
        ch1 = ini_read(fn_config, s, 'ch1', '')
        res_from = ini_read(fn_config, s, 'res_from', '')
        res_to = ini_read(fn_config, s, 'res_to', '')
        color_id = ini_read(fn_config, s, 'color_id', '')
        if not res_from or not res_to:
            continue
        config[s] = {
            'ch0': ch0,
            'ch1': ch1,
            'res_from': res_from,
            'res_to': res_to,
            'color_id': color_id,
            }


class Command:

    def __init__(self):

        load_config()

    def config(self):

        if not os.path.isfile(fn_config):
            ini_write(fn_config, '_', '_', '_')

        if os.path.isfile(fn_config):
            file_open(fn_config)
        else:
            msg_status(_('Config file not found'))


    def on_change_slow(self, ed_self):

        self.work(ed_self, 'on_change_slow')

    def on_lexer(self, ed_self):

        self.work(ed_self, 'on_lexer')

    def on_lexer_parsed(self, ed_self):

        self.work(ed_self, 'on_lexer_parsed')


    def work(self, ed: Editor, reason):

        global config
        #log('reason: '+reason)
        
        ed.attr(MARKERS_DELETE_BY_TAG, tag=MYTAG)
        lex = ed.get_prop(PROP_LEXER_FILE)
        if not lex in config:
            log('not supported lexer')
            return

        props = config[lex]
        ch0 = props['ch0']
        ch1 = props['ch1']
        res_from = props['res_from']
        res_to = props['res_to']
        color_int = get_color(props['color_id'])

        line_top = ed.get_prop(PROP_LINE_TOP)
        line_btm = ed.get_prop(PROP_LINE_BOTTOM)
        #log('line_top: '+str(line_top))
        #log('line_btm: '+str(line_btm))

        tok = ed.get_token(TOKEN_LIST_SUB, index1=line_top, index2=line_btm)
        if not tok:
            #log('no tokens at all')
            return
        tok = [t for t in tok if t['ks']=='s']
        if not tok:
            #log('no tokens-strings')
            return

        if ch0:
            chars = ch0+ch1
            tok = [t for t in tok if t['str'].startswith(chars)]

        for t in tok:
            #log('token: '+repr(t))
            x1 = t['x1']
            x2 = t['x2']
            y1 = t['y1']
            y2 = t['y2']
            s = t['str']
            
            pos_from = -1
            
            while True:
                pos_from = s.find(res_from, pos_from+1)
                if pos_from<0:
                    break
                
                pos_to = s.find(res_to, pos_from)
                if pos_to<0:
                    break
                
                s_before = s[:pos_from]
                count_eol = s_before.count('\n')
                if count_eol>0:
                    offset_eol = s_before.rfind('\n')
                    count_x = pos_from - offset_eol - 1
                else:
                    count_x = x1 + pos_from
    
                ed.attr(MARKERS_ADD,
                    tag = MYTAG,
                    x = count_x,
                    y = y1 + count_eol,
                    len = pos_to - pos_from + 1,
                    color_font = color_int,
                    )
