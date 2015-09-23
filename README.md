cheat
=====
Fork of [chrisallenlane/cheat](https://github.com/chrisallenlane/cheat) that
attempts to use markdown syntax highlighting for all cheat sheets.

Markdown syntax highlight depends on
[jhermann/pygments-markdown-lexer](https://github.com/jhermann/pygments-markdown-lexer)

TODO
----
* Ignore file extension (e.g. look up `cat.md` when invoking `cheat cat`)?
* Use cheat-sheet extensions to select pygments lexer (e.g. apply markdown to
  the cheatsheet `cat.md` and bash highlight to `cat.sh`?
* Use `CHEATCOLORS` to select pygments lexer?
* Can we have a markdown parser that applies syntax highlighting for «lang»
  to markdown code blocks (```lang\n```)?
