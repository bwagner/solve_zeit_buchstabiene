#!/usr/bin/env python

from pathlib import Path
from typing import Optional

import typer

from solve_zeit_buchstabiene import LEN_MAPPING, switch_apps_2, type_word, handle_file


# get wordlist e.g. from here:
# https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4

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
