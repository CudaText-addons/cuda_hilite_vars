plugin for CudaText.
it performs work additional to lexer: highlights "variables" (e.g. in Bash script it's $var or ${var_long}) inside string literals. lexer cannot do this, it highlights string literals with single color.

plugin has config file: Options / Settings-plugins / Hilite Vars / Config.
config file may have sections [0] to [40], section per lexer.
section for "Bash script" lexer is preconfigured:

  [0]
  lexer=Bash script
  regex_str=".*?"
  regex_var=\$\w+|\$\{.*?\}
  color=String2

items:
- lexer name,
- reg.ex. for string literal,
- reg.ex. for variable inside string literal,
- color-id from theme. to see possible color-ids, open CudaText dialog Options / Settings-more / Settings-theme-syntax. also good to use color-id IdVar, it's used for variables outside of strings, but (in default theme) it's greenish color similar to string color.

author: Alexey (CudaText)
license: MIT
