#!/usr/bin/env python
import os
from pathlib import Path
from time import sleep

from pynput.keyboard import Controller, Key

LEN_MAPPING = 9
SLEEP_SECS = 0.06

# So far only used on
# macOS 13.4.1 (Ventura).
# Python 3.11.4

# See it in action: https://youtu.be/O0rWH5hdgx0

command_key = Key.cmd if os.name == "posix" else Key.ctrl
keyboard = Controller()


def switch_apps():
    """
    Switches between applications by pressing Cmd-Tab.
    """
    with keyboard.pressed(command_key):
        keyboard.type("\t")
    sleep(SLEEP_SECS)  # do not type too fast after switching apps


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
        mapping[idx] = "-"  # mark char as used
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
    """
    for ch in word:
        keyboard.type(ch)
    keyboard.type("\n")
    sleep(SLEEP_SECS)


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
