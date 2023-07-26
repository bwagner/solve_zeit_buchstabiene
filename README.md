# Find Some Words For Buchstabiene Riddle Of ["Die Zeit"](https://zeit.de)

Simple Python script that attempts all words in a file for a given map.

See [Buchstabiene](https://spiele.zeit.de/buchstabiene/)

## Prerequisites
- Download a word list which consists of one German word per line, e.g. [this file](https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4).
- The Script assumes the file to be installed here:
  `~/Downloads/wordlist-german.txt`
- install dependencies, e.g. `pip install -r requirements.txt`
- Before running the script, open the riddle in a web browser, then click on
	the terminal from where you'll run the script.  The script will attempt to
	change the focus to the web browser by simulating typing of Cmd-Tab for macOS,
	Ctrl-Tab for Windows

## Map

The script needs to know what the current map is.

The map is defined by the "flower": its center (seeds) and 8 Petals, hence 9 characters.

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

`./solve_zeit_buchstabiene.py towuhratp`

