#!/usr/bin/env python3
"""Offline structural checks; actual Helm lint/template run in validate-helm.sh."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = re.compile(r"{{-?\s*(.*?)\s*-?}}", re.DOTALL)
OPENERS = {"if", "with", "range", "define", "block"}
errors: list[str] = []
definitions: set[str] = set()
includes: list[tuple[Path, str]] = []
files = sorted(p for p in (ROOT / "charts" / "all").rglob("*") if p.suffix in {".yaml", ".tpl"} and "templates" in p.parts)

for path in files:
    text = path.read_text(encoding="utf-8")
    if text.count("{{") != text.count("}}"):
        errors.append(f"{path.relative_to(ROOT)}: unbalanced delimiters")
        continue
    stack: list[tuple[str, int]] = []
    for match in TAG.finditer(text):
        expression = match.group(1).strip()
        line = text.count("\n", 0, match.start()) + 1
        if not expression or expression.startswith("/*"):
            continue
        command = expression.split(maxsplit=1)[0]
        if command in OPENERS:
            stack.append((command, line))
        elif command == "else":
            if not stack or stack[-1][0] not in {"if", "with", "range"}:
                errors.append(f"{path.relative_to(ROOT)}:{line}: unmatched else")
        elif command == "end":
            if not stack:
                errors.append(f"{path.relative_to(ROOT)}:{line}: unmatched end")
            else:
                stack.pop()
        if command == "define":
            found = re.match(r'define\s+"([^"]+)"', expression)
            if found:
                definitions.add(found.group(1))
        for found in re.finditer(r'include\s+"([^"]+)"', expression):
            includes.append((path, found.group(1)))
    for command, line in stack:
        errors.append(f"{path.relative_to(ROOT)}:{line}: unclosed {command}")

for path, name in includes:
    if name not in definitions:
        errors.append(f"{path.relative_to(ROOT)}: undefined named template {name!r}")

if errors:
    print("Helm template structural checks failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)
print(f"Helm template structure successful: {len(files)} files, {len(definitions)} named templates.")
