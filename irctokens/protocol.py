from typing   import Dict, List, Optional
from .objects import Hostmask, Line

TAG_UNESCAPED = ["\\",   " ",   ";",   "\r",  "\n"]
TAG_ESCAPED =   ["\\\\", "\\s", "\\:", "\\r", "\\n"]

def _unescape_tag(value: str):
    unescaped, escaped = "", list(value)
    while escaped:
        current = escaped.pop(0)
        if current == "\\":
            if escaped:
                next = escaped.pop(0)
                duo = current+next
                if duo in TAG_ESCAPED:
                    index = TAG_ESCAPED.index(duo)
                    unescaped += TAG_UNESCAPED[index]
                else:
                    unescaped += next
        else:
            unescaped += current
    return unescaped
def _escape_tag(value: str):
    for i, char in enumerate(TAG_UNESCAPED):
        value = value.replace(char, TAG_ESCAPED[i])
    return value

def format(line: Line) -> str:
    outs: List[str] = []
    if line.tags:
        tags_str = []
        for key in sorted(line.tags.keys()):
            if line.tags[key]:
                value = line.tags[key] or ""
                tags_str.append(f"{key}={_escape_tag(value)}")
            else:
                tags_str.append(key)
        outs.append(f"@{';'.join(tags_str)}")

    if line.source:
        outs.append(f":{line.source}")
    outs.append(line.command)

    params = line.params.copy()
    if line.params:
        last = params.pop(-1)
        for param in params:
            if " " in param:
                raise ValueError("non last params cannot have spaces")
            elif param.startswith(":"):
                raise ValueError("non last params cannot start with colon")
        outs.extend(params)

        if (not last or
                " " in last or
                last.startswith(":")):
            last = f":{last}"
        outs.append(last)
    return " ".join(outs)

def build(
        command: str,
        params:  List[str]=[],
        source:  Optional[str]=None,
        tags:    Optional[Dict[str, str]]=None
        ) -> Line:
    return Line(tags, source, command, params, format)

def _tokenise(tags_s: Optional[str], line: str) -> Line:
    tags: Optional[Dict[str, str]] = None
    if not tags_s is None:
        tags = {}
        for part in tags_s[1:].split(";"):
            key, _, value = part.partition("=")
            tags[key] = _unescape_tag(value)

    line, trailing_sep, trailing = line.partition(" :")
    params = list(filter(bool, line.split(" ")))

    source: Optional[str] = None
    if params[0][0] == ":":
        source = params.pop(0)[1:]

    command = params.pop(0).upper()

    if trailing_sep:
        params.append(trailing)

    return build(command, params, source, tags)

def tokenise_b(line_b: bytes,
        encoding: str="utf8",
        fallback: str="latin-1") -> Line:

    tags: Optional[str] = None
    if line_b[0] == ord(b"@"):
        tags_b, _, line_b = line_b.partition(b" ")
        tags = tags_b.decode("utf8")

    try:
        line = line_b.decode(encoding)
    except UnicodeDecodeError:
        line = line_b.decode(fallback)

    return _tokenise(tags, line)

def tokenise(line: str) -> Line:
    if line[0] == "@":
        tags, _, line = line.partition(" ")
        return _tokenise(tags, line)
    else:
        return _tokenise(None, line)
