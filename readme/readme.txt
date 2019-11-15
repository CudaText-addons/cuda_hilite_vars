plugin for CudaText.
it performs work additional to lexer: highlights "variables" (e.g. in Bash script it's $var or ${var_long}) inside string literals. lexer cannot do this, it highlights string literals with single color.

plugin has config file, call menu item "Options / Settings-plugins / Highlight Variables".
config file has sections [lexer_name] with lexer names.
plugin has predefined config for "Bash script" and "Perl":

[Bash script]
regex_str=".*?"
regex_var=\$\w+|\$\{.*?\}
color=IdVar

items:
- reg.ex. for string literal,
- reg.ex. for variable inside string literal,
- color-id from theme. to see possible color-ids, open CudaText dialog Options / Settings-more / Settings-theme-syntax. also good to use color-id IdVar, it's used for variables outside of strings, but (in default theme) it's greenish color similar to string color.

author: Alexey Torgashin (CudaText)
license: MIT
