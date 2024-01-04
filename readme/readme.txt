Plugin for CudaText.
It performs work additional to lexer highlighting: highlights "variables"
inside string literals. Lexer cannot do this, it highlights string literals
with single color. Plugin supports multi-line string literals too.

Plugin has predefined (in memory) configuration for:
- Python
- Bash script
- Perl
For other lexers, you need to add config-file section.

To open config-file, call menu item:
"Options / Settings-plugins / Highlight Variables / Config".
Config file has sections - lexer names. Keys in sections:

"begin"
  Regular expression, which must match at the begin of string literal.
  Can be empty, then any string literal will be handled.
  In-memory value for Python is "f".
"res"
  Regular expression which finds "variables" inside string literals.
  In-memory value for Python is "{.*?}".
  In-memory value for Bash is "\$\w+|\${.*?}".
"theme"
  Sets coloring of fragment. Element id from CudaText syntax-theme.
  To see possible ids, open CudaText dialog: "Options / Settings-theme-syntax".
  This is optional key, 'String2' is the default. Also good to use is 'IdVar'.


Author: Alexey Torgashin (CudaText)
License: MIT
