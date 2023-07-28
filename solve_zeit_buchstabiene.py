#!/usr/bin/env python
import os
from pathlib import Path

import pyautogui

LEN_MAPPING = 9

# So far only used on
# macOS 13.4.1 (Ventura).
# Python 3.11.4

# See it in action: https://youtu.be/O0rWH5hdgx0

command_key = "command" if os.name == "darwin" else "ctrl"

def switch_apps_2():
    """
    Switches between applications by pressing Cmd-Tab.
    Works on the tested system macOS 13.4.1 Ventura.
    pyautogui.hotkey("command", "tab") does not work.
    """
    with pyautogui.hold(command_key):
        pyautogui.press("tab")


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
