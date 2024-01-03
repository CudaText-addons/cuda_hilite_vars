import os
import re
from cudatext import *
from cudax_lib import get_translation

_ = get_translation(__file__)  # I18N

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_hilite_vars.ini')
MYTAG = app_proc(PROC_GET_UNIQUE_TAG, '')

config = {
    'Python': {
        'begin': 'f',
        'res': r'{.*?}',
        },
    'Perl': {
        'begin': '',
        'res': r'[\$@%]\w+',  # $scalar, @array, %hash
        },
    'Bash script': {
        'begin': '',
        'res': r'\$\w+|\${.*?}',
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
        begin = ini_read(fn_config, s, 'begin', '')
        res = ini_read(fn_config, s, 'res', '')
        theme = ini_read(fn_config, s, 'theme', 'String2')
        if not res:
            continue
        config[s] = {
            'begin': begin,
            'res': res,
            'theme': theme,
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

    def on_scroll(self, ed_self):

        '''
        self.work(ed_self, 'on_scroll')
        '''
        self.on_focus(ed_self)

    def by_timer(self, tag='', info=''):

        self.work(self.timer_ed, 'by_timer')

    def on_focus(self, ed_self):

        self.timer_ed = ed_self
        timer_proc(TIMER_START_ONE, 'cuda_hilite_vars.by_timer', 150, '0')

    def work(self, ed: Editor, reason):

        global config
        #log('reason: '+reason)

        ed.attr(MARKERS_DELETE_BY_TAG, tag=MYTAG)
        lex = ed.get_prop(PROP_LEXER_FILE)
        if not lex in config:
            log('not supported lexer: '+lex)
            return

        props = config[lex]
        begin = props.get('begin', '')
        res = props['res']
        res_re = re.compile(res, 0)
        color_int = get_color(props.get('theme', 'String2'))

        line_top = ed.get_prop(PROP_LINE_TOP)
        line_btm = ed.get_prop(PROP_LINE_BOTTOM) + 5
        #line_btm = min(ed.get_line_count()-1, line_top + ed.get_prop(PROP_VISIBLE_LINES) + 5)
        # adding N=5...10 is a workaround for API bug: it don't return last partially visible token

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

        if begin:
            tok = [t for t in tok if t['str'].startswith(begin)]

        for t in tok:
            #log('token: '+repr(t))
            x1 = t['x1']
            x2 = t['x2']
            y1 = t['y1']
            y2 = t['y2']
            s = t['str']

            pos_to = -1
            for m in res_re.finditer(s, 0):
                #log('m: '+repr(m))
                span = m.span()
                pos_from = span[0]
                pos_to = span[1]

                s_before = s[:pos_from]
                count_eol = s_before.count('\n')
                if count_eol>0:
                    count_x = pos_from - s_before.rfind('\n') - 1
                else:
                    count_x = x1 + pos_from

                ed.attr(MARKERS_ADD,
                    tag = MYTAG,
                    x = count_x,
                    y = y1 + count_eol,
                    len = pos_to - pos_from,
                    color_font = color_int,
                    )

