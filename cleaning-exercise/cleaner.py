from pathlib import Path
import re

source = Path("Pasted text.txt")
titles = []

for line in source.read_text(encoding="utf-8").splitlines():
    # Remove whitespace and ranking numbers, such as "12."
    text = re.sub(r"^\d+\.\s*", "", line.strip())

    # Skip metadata, empty lines, and navigation.
    if (
        not text
        or re.match(r"^\d+ points? by ", text)
        or "save to pocket" in text
        or text == "More"
        or text.startswith("Hacker News new |")
    ):
        continue

    # Remove a trailing website domain, preserving other parentheses.
    text = re.sub(r" \([^()\s]+\.[^()\s]+\)$", "", text)
    titles.append(text)

Path("titles.txt").write_text(
    "\n".join(titles) + "\n",
    encoding="utf-8",
)

print(f"Saved {len(titles)} titles")