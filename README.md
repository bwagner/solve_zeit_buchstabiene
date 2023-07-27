# Find Some Words For Buchstabiene Riddle Of ["Die Zeit"](https://zeit.de)

Simple Python script that attempts all words in a file for a given map.

See [Buchstabiene](https://spiele.zeit.de/buchstabiene/)

## Prerequisites
- Download a word list which consists of one German word per line, e.g. [this file](https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4).
- install dependencies, e.g. `pip install -r requirements.txt`
- Before running the script, open the riddle in a web browser, then click on
	the terminal from where you'll run the script.  The script will attempt to
	change the focus to the web browser by simulating typing of Cmd-Tab for macOS,
	Ctrl-Tab for Windows

## Mapping

The script needs to know what the current mapping is.

The mapping is defined by the "flower": its center (seeds) and 8 Petals, hence 9 characters.

<img width="764" alt="image" src="https://github.com/bwagner/solve_zeit_buchstabiene/assets/447049/90cfd0b6-73ae-4921-9407-a4c79bbc72be">

Ascii-Representation of the riddle of 26.04.2023:
```

            P   O
           T     W
              T
           A     U
            R   H

```
We map these characters as follows:
```
            8   1
           7     2
              0
           6     3
            5   4

```
Hence the script would be called like this:

`./solve_zeit_buchstabiene_main.py towuhratp -f wordlist_file`

To only enter a single word, e.g. "autor" (instead of testing a whole bunch from a file), call the script as follows:

`./solve_zeit_buchstabiene_main.py towuhratp autor`
# Usage
```
╭─ Arguments ────────────────────────────────────────────────────────────────────╮
│ *    mapping      TEXT    [default: None] [required]                           │
│      word         [WORD]  [default: None]                                      │
╰────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --file  -f      TEXT  [default: None]                                          │
│ --help                Show this message and exit.                              │
╰────────────────────────────────────────────────────────────────────────────────╯
```
# Example Run
See on [Youtube](https://youtu.be/O0rWH5hdgx0)
# Run Tests
In project root directory run:

`pytest`

or

`./solve_zeit_buchstabiene_test.py`