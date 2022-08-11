plugin for CudaText.
it performs work additional to lexer highlighting: highlights "variables"
inside string literals. lexer cannot do this, it highlights string literals
with single color.

plugin has config file, call menu item:
"Options / Settings-plugins / Highlight Variables / Config".
config file has sections with lexer names.
plugin has predefined sections for:
- Bash script
- Python
- Perl
for example, Bash config:

	[Bash script]
	regex_str=("|')(\\.|.)*?\1
	regex_var=\$\w+|\$\{.*?\}
	color=String2

keys in these sections:
- reg.ex. for string literal,
- reg.ex. for variable inside string literal,
- element id from syntax-theme. to see possible ids, open CudaText dialog:
"Options / Settings-more / Settings-theme-syntax".
it's good to use id 'String2' or 'IdVar'. 


author: Alexey Torgashin (CudaText)
license: MIT
