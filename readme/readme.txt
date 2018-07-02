plugin for CudaText.
it performs work additional to lexer: highlights "variables" (e.g. in Bash script it's $var or ${var_long}) inside string literals. lexer cannot do this: it can highlight string literals with single color only.
plugin has config file: Options / Settings-plugins / Hilite Vars / Config.

config file may have sections [0] to [40], section per lexer:
  [0]
  lexer=Bash script
  regex_str=".*?"
  regex_var=\$\w+|\$\{.*?\}
  color=IdVar

here is the lexer name, reg.ex. for string literal, reg.ex. for variable inside string literal, and color-id (to see possible color-ids, open CudaText dialog Options / Settings-more / Settings-theme-syntax).

author: Alexey (CudaText)
license: MIT
