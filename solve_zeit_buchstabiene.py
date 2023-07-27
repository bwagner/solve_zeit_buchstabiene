#!/usr/bin/env python

import sys
from pathlib import Path
from typing import Optional

import pyautogui
import pytest
import typer

LEN_MAPPING = 9

# So far only used on
# macOS 13.4.1 (Ventura).
# Python 3.11.4

# See it in action: https://youtu.be/O0rWH5hdgx0

# wordlist from here:
# https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
word_list = Path("~/Downloads/wordlist-german.txt").expanduser()


def switch_apps_1():
    """
    Supposed to switch between applications by pressing Cmd-Tab.
    Does not work on the tested system macOS 13.4.1 Ventura.
    """
    pyautogui.hotkey("command", "tab")


def switch_apps_2():
    """
    Switches between applications by pressing Cmd-Tab.
    Works on the tested system macOS 13.4.1 Ventura.
    """
    with pyautogui.hold("command"):
        pyautogui.press("tab")


def switch_apps_3():
    """
    Switches between applications by pressing Cmd-Tab.
    Works on the tested system macOS 13.4.1 Ventura.
    """
    pyautogui.keyDown("command")
    pyautogui.press("tab")
    pyautogui.keyUp("command")


def get_petals(mapping: str, word: str) -> list[int]:
    """
    Translates word characters into flower petals as a list with our numbering.
    """
    mapping: list[str] = list(mapping)
    petals = [-1] * len(word)
    i: int
    ch: str
    for i, ch in enumerate(word):
        idx: int = mapping.index(ch)
        mapping[idx] = "-"  # mark char as no longer available
        petals[i] = idx
    return petals


def word_ok(mapping: str, word: str) -> bool:
    """
    Indicates whether word is representable with given mapping.
    """
    # the character in the center of the flower (seed) is mandatory.
    if mapping[0] not in word:
        return False

    # minimum word length: 3
    if len(word) < 3:
        return False

    # every petal of the flower may be used max once.
    map_list = list(mapping)
    try:
        for ch in word:
            map_list.remove(ch)  # removes 1st occurrence of char in list
        return True
    except ValueError:
        return False


def type_word(word: str) -> None:
    """
    Types the given word and concludes with Return.
    Note: On macOS Ventura 13.4.1 pyautogui.press() does not work for Umlauts.
    """
    for ch in word:
        pyautogui.press(ch)
    pyautogui.press("return")


def handle_file(mapping: str, word_list_file: str | Path):
    """
    Tries all words in the given file for the given mapping.
    """
    with open(word_list_file) as f:
        for word in f:
            word = word[:-1].lower()  # cut off newline
            print(f"trying {word}: ", end="")
            if word_ok(mapping, word):
                print("candidate!")
                type_word(word)
            else:
                print("nope.")


## Tests #######################################################################

# noinspection SpellCheckingInspection
test_input_verify = [
    ("aemlbgria", "abla", True),
    ("aemlbgria", "ablaa", False),
    ("aemlbgria", "ablal", False),
    ("aemlbgria", "gabel", True),
    ("aemlbgria", "griaemlba", True),
    ("aemlbgria", "griamlbae", True),
    ("aemlbgria", "griaemlbae", False),
    ("uitcphsts", "usts", True),
]


@pytest.mark.parametrize("mapping,word,ok_exp", test_input_verify)
def test_verify_word(mapping, word, ok_exp):
    assert word_ok(mapping, word) == ok_exp


# noinspection SpellCheckingInspection
test_input_petals = [
    ("aemlbgria", "abla", [0, 4, 3, 8]),
    ("aemlbgria", "gabel", [5, 0, 4, 1, 3]),
    ("aemlbgria", "griaemlba", [5, 6, 7, 0, 1, 2, 3, 4, 8]),
    ("aemlbgria", "griamlbae", [5, 6, 7, 0, 2, 3, 4, 8, 1]),
]


@pytest.mark.parametrize("mapping,word,exp", test_input_petals)
def test_petals(mapping, word, exp):
    assert get_petals(mapping, word) == exp


## Main ########################################################################


def main(
    mapping: str,
    word: Optional[str] = typer.Argument(None),
    filename: Optional[str] = typer.Option(None, "--file", "-f"),
):
    if len(mapping) != LEN_MAPPING:
        typer.echo(
            f"Mapping should be a {LEN_MAPPING}-char word. "
            f"You've provided {mapping} of length {len(mapping)}."
        )
        raise typer.Exit()

    if word and filename:
        typer.echo(
            f"You can't provide both a word ('{word}') "
            f"and a filename ('{filename}'). Choose one."
        )
        raise typer.Exit()

    if word:
        switch_apps_2()
        type_word(word)
    elif filename:
        file_path = Path(filename).expanduser()
        switch_apps_2()
        try:
            handle_file(mapping, file_path)
        except IOError as e:
            switch_apps_2()
            typer.echo(f"Could not open file {file_path}: {e}")
    else:
        typer.echo(
            "You need to provide either a word or a "
            "filename. You provided neither. Choose one."
        )


if __name__ == "__main__":
    typer.run(main)
