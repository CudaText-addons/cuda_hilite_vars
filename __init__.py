import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_hilite_vars.ini')

MAX_CONFIG_SECTIONS = 30

config = {}
config['Bash script'] = {
    're_str': '".*?"',
    're_var': '$\w+|${.*?}',
    'color': 'IdVar',
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
            'color': color,
            }
            

def save_config():
    global config
    for (i, key) in enumerate(config.keys()):
        s = str(i)
        ini_write(fn_config, s, 'lexer', key)
        ini_write(fn_config, s, 'regex_str', config[key]['re_str'])
        ini_write(fn_config, s, 'regex_var', config[key]['re_var'])
        ini_write(fn_config, s, 'color', config[key]['color'])


def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'


class Command:
    
    def __init__(self):

        global config
        if not os.path.isfile(fn_config):
            save_config()
        load_config()    
        print(config)

    def config(self):

        if os.path.isfile(fn_config):    
            file_open(fn_config)
        else:
            msg_status('Config file not found')
        
    def on_change_slow(self, ed_self):
        pass
    def on_lexer(self, ed_self):
        pass
    def on_open(self, ed_self):
        pass
