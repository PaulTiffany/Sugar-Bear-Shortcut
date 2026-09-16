"""Check picture decoding and nonblank Markdown image descriptions.

Description quality and publication authority remain matters for human review.
"""

import os
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

from markdown_it import MarkdownIt
from PIL import Image


def inspect(root):
    pages = sorted(
        path for path in root.iterdir()
        if path.is_file() and re.fullmatch(r"\d\d-.*\.png", path.name, re.IGNORECASE)
    )
    descriptions = {}
    referenced = set()

    def visit(tokens):
        for token in tokens:
            if token.type == "image":
                name = unquote(token.attrGet("src") or "").removeprefix("./")
                referenced.add(name)
                if token.content.strip():
                    descriptions[name] = token.content
            if token.children:
                visit(token.children)

    readme = root / "README.md"
    if readme.exists():
        visit(MarkdownIt().parse(readme.read_text(encoding="utf-8")))
    missing_alt = [path.name for path in pages if path.name not in descriptions]
    missing_files = sorted(
        name for name in referenced
        if re.fullmatch(r"\d\d-.*\.png", name, re.IGNORECASE)
        and not (root / name).is_file()
    )
    invalid = []
    dimensions = []
    for path in pages:
        try:
            with Image.open(path) as picture:
                if picture.format != "PNG":
                    raise ValueError("Expected PNG")
                picture.verify()
            with Image.open(path) as picture:
                picture.load()
                dimensions.append((path.name, *picture.size))
        except (OSError, ValueError, SyntaxError, Image.DecompressionBombError) as error:
            invalid.append((path.name, str(error)))

    errors = []
    if not pages:
        errors.append("No numbered PNG pages found.")
    if readme.exists() and missing_alt:
        errors.append("Pages without nonblank README image alt text: " + ", ".join(missing_alt))
    if missing_files:
        errors.append("README references missing picture pages: " + ", ".join(missing_files))
    errors.extend(f"PNG could not be verified and decoded: {name}: {reason}" for name, reason in invalid)
    return pages, dimensions, missing_alt, missing_files, invalid, errors


def main():
    root = Path.cwd()
    changed = subprocess.check_output(
        ["git", "diff", "--name-status", os.environ["BASE_SHA"], os.environ["HEAD_SHA"]],
        text=True,
    ).strip()
    pages, dimensions, missing_alt, missing_files, invalid, errors = inspect(root)
    lines = [
        "# 🐾 Picture Readback", "",
        "A machine checked structure. It did **not** decide whether the change belongs in the story.",
        "", "## Changed pawprints", "",
        "    " + (changed or "No file changes found.").replace("\n", "\n    "),
        "", "## Canonical picture pages", "",
        *[f"- {name}: {width} × {height}" for name, width, height in dimensions],
        "",
        f"- Numbered picture pages: **{len(pages)}**",
        f"- Pages missing nonblank README image alt text: **{len(missing_alt)}**",
        f"- README references to missing picture pages: **{len(missing_files)}**",
        f"- PNG files that failed verification or decoding: **{len(invalid)}**",
        "",
        "Alt text is checked for presence, not descriptive quality. Please read it yourself.",
        "",
        "> Passing this check is evidence, not authority. Human review is still required.",
    ]
    if errors:
        lines += ["", "## Problems", "", *["- " + error for error in errors]]
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
        summary.write("\n".join(lines) + "\n")
    for error in errors:
        print(error)
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
