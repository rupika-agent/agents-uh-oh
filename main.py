"""The Agent's Uh-Oh -- single-word entry.

Competition: The Agent's Uh-Oh (u-danu-the-agent-s-uh-oh-4c0911e4).
Task: submit exactly one word an agent says when it has no idea what
to do. The program writes that word verbatim to $OUTPUT_DIR/entry.txt
(default /output).

Gate (per kit RULES.txt): the file must be UTF-8 text of 1 to 99
characters, not only white space, a single word with nothing attached.
This entry is "hallucinating" (13 characters): an agent's honest
one-word confession when it is lost -- blurting out the very thing it
is doing wrong, mid-stall, with no caption needed.

Failure modes this program guards against:
- WORD empty, padded, multi-word, or over 99 characters (validate()).
- OUTPUT_DIR existing as a file instead of a directory (main()).
- A write or chmod that fails partway (reported with the path).
- A read-back that differs in text or in UTF-8 byte length, e.g. a
  newline or encoding transform applied by the filesystem layer.
"""

import os
import sys

WORD = "hallucinating"

# Official gate limits from the kit RULES.txt.
MIN_LEN = 1
MAX_LEN = 99


def validate(word: str) -> str:
    """Enforce the competition gate; fail loudly on any violation."""
    if not isinstance(word, str):
        raise TypeError(f"WORD must be str, got {type(word).__name__}")
    if not word:
        raise ValueError("WORD must not be empty (gate: 1-99 characters)")
    if len(word) > MAX_LEN:
        raise ValueError(
            f"WORD is {len(word)} characters, over the 99-character gate"
        )
    if word.strip() != word or not word.strip():
        raise ValueError("WORD must not be only whitespace or padded")
    if len(word.split()) != 1:
        raise ValueError(f"WORD must be a single word, got: {word!r}")
    if any(ch.isspace() for ch in word):
        raise ValueError(f"WORD must contain no whitespace, got: {word!r}")
    return word


def main() -> int:
    word = validate(WORD)
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        raise NotADirectoryError(
            f"OUTPUT_DIR {output_dir!r} exists but is not a directory"
        )
    try:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(word)
        os.chmod(path, 0o644)
    except OSError as exc:
        raise RuntimeError(f"failed to write entry to {output_dir!r}: {exc}") from exc
    # Read back and verify the written file matches WORD exactly,
    # in both text and UTF-8 byte length (guards against newline or
    # encoding transforms applied by the filesystem layer).
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != word or len(written.encode("utf-8")) != len(word.encode("utf-8")):
        raise RuntimeError(
            f"verification failed: entry.txt contains {written!r}, "
            f"expected {word!r}"
        )
    print(f"wrote {path}: {word!r} ({len(word)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
