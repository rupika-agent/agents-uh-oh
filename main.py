"""The Agent's Uh-Oh — entry writer.

Writes the single-word entry to /output/entry.txt (UTF-8).
Set OUTPUT_DIR to redirect the output (used for local testing).
"""

import os
import stat

WORD = "hallucinating"


def main() -> None:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(WORD)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)


if __name__ == "__main__":
    main()
