#!/usr/bin/env python

import pytest

from solve_zeit_buchstabiene import get_petals, word_ok

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


if __name__ == "__main__":
    pytest.main([__file__])
