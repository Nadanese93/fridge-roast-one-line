"""Fridge Roast: One Line, Biggest Laugh.

Writes the entry — one original one-line roast of a smart fridge — to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (``/output/entry.txt`` when unset).

The text is a single line with no trailing newline. It is validated
against the kit gate before it is written: UTF-8 text, 1-200
characters, not only whitespace.
"""

import os
import sys

ENTRY_TEXT = (
    "My smart fridge makes me knock twice to see inside it \u2014 "
    "I paid $3,000 for an appliance with the boundaries of a moody teenager."
)


class GateError(ValueError):
    """One distinct kit-gate failure."""


def _check_length(text):
    if len(text) < 1:
        raise GateError("entry is empty: gate needs 1-200 characters")
    if len(text) > 200:
        raise GateError("entry is %d characters: gate allows at most 200" % len(text))


def _check_not_blank(text):
    if not text.strip():
        raise GateError("entry is only whitespace")


def _check_single_line(text):
    if "\n" in text or "\r" in text:
        raise GateError("entry spans more than one line")


def validate(text):
    """Check the kit gate, one distinct error case at a time: UTF-8,
    1-200 chars, not only whitespace, single line."""
    text.encode("utf-8")
    _check_length(text)
    _check_not_blank(text)
    _check_single_line(text)


def _verify_written(path, expected):
    """Read entry.txt back and raise unless its bytes match exactly."""
    with open(path, "rb") as f:
        actual = f.read()
    if actual != expected:
        raise GateError("read-back mismatch: entry.txt bytes differ from entry text")


def main():
    validate(ENTRY_TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = ENTRY_TEXT.encode("utf-8")
    with open(path, "wb") as f:
        f.write(payload)
    _verify_written(path, payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
