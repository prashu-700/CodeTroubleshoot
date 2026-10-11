
import re


def format_recognized_text(text):
    if text is None:
        return ""

    text = str(text)

    # Normalize line breaks and whitespace.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        # Ignore lines containing only punctuation or symbols.
        if not re.search(r"[A-Za-z0-9]", line):
            continue

        lines.append(line)

    return "\n".join(lines)

