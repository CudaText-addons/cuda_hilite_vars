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
Config file has sections with lexer names. Keys in these sections:

"begin"
  If not empty, string literal must begin with specified text.
  For example, for Python it is "f".
"res"
  Regular expression which finds "variables" inside string literals.
  For example, for Python it is "{.*?}".
"theme"
  Element id from current CudaText syntax-theme.
  To see possible ids, open CudaText dialog: "Options / Settings-theme-syntax".
  Suggested value is 'String2', also good is 'IdVar'. 


Author: Alexey Torgashin (CudaText)
License: MIT
