#!/usr/bin/env python

import sys
from pathlib import Path

import pyautogui
import pytest

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
    petals = [None] * len(word)
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
    Note: On macOS Ventura 13.4.1 pyautogui.press does not work for Umlauts.
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
                try:
                    type_word(word)
                except Exception:
                    print("error occurred. continuing...")
            else:
                print("nope.")


## Tests #######################################################################

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


def main():
    if len(sys.argv) == 11:
        mapping = "".join(sys.argv[1:11]).lower()
        word = sys.argv[10].lower()
    elif len(sys.argv) == 3:
        mapping = sys.argv[1].lower()
        word = sys.argv[2].lower()
    elif len(sys.argv) in (2, 10):
        if len(sys.argv) == 2:
            mapping = sys.argv[1].lower()
        else:
            mapping = "".join(sys.argv[1:]).lower()
        switch_apps_2()
        handle_file(mapping, word_list)
        return
    else:
        print(
            "expected either 9 chars and 1 word "
            "or 1 mapping "
            f"or 2 words but got {len(sys.argv) - 1}."
        )
        return
    if word_ok(mapping, word):
        switch_apps_2()
        click_coords = type_word(word)
        print(click_coords)

    else:
        print(f"word {word} is not representable with {mapping} or is too short.")


if __name__ == "__main__":
    main()
