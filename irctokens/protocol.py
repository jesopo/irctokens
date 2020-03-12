from typing import Dict, List, Optional

TAG_UNESCAPED = ["\\",   " ",   ";",   "\r",  "\n"]
TAG_ESCAPED =   ["\\\\", "\\s", "\\:", "\\r", "\\n"]

def _unescape_tag(value: str):
    if value.endswith("\\") and not value.endswith("\\\\"):
        value = value[:-1]
    parts = value.split("\\\\")
    for i, piece in enumerate(TAG_ESCAPED):
        for j, part in enumerate(parts):
            parts[j] = part.replace(piece, TAG_UNESCAPED[i])
    return "\\".join(parts)
def _escape_tag(value: str):
    for i, char in enumerate(TAG_UNESCAPED):
        value = value.replace(char, TAG_ESCAPED[i])
    return value

class Hostmask(object):
    def __init__(self, source: str):
        self._raw = source
        username,      _, hostname = source.partition("@")
        self.nickname, _, username = username.partition("!")
        self.username = username or None
        self.hostname = hostname or None

    def __str__(self) -> str:
        return self._raw
    def __repr__(self) -> str:
        return (f"Hostmask(nick={self.nickname!r}, user={self.username!r}"
           f", host={self.hostname!r})")
    def __eq__(self, other) -> bool:
        if isinstance(other, Hostmask):
            return str(self) == str(other)
        else:
            return False

class Line(object):
    def __init__(self,
            tags:    Optional[Dict[str, Optional[str]]]=None,
            source:  Optional[str]=None,
            command: str="",
            params:  List[str]=None):
        self.tags    = tags
        self.source  = source
        self.command = command
        self.params  = params or []

    def __eq__(self, other) -> bool:
        if isinstance(other, Line):
            return self.format() == other.format()
        else:
            return False
    def __repr__(self) -> str:
        return (f"Line(tag={self.tags!r}, source={self.source!r}"
            f", command={self.command!r}, params={self.params!r})")

    _hostmask: Optional[Hostmask] = None
    @property
    def hostmask(self):
        if self.source:
            self._hostmask = self._hostmask or Hostmask(self.source)
        return self._hostmask

    def format(self) -> str:
        outs: List[str] = []
        if self.tags:
            tags_str = []
            for key in sorted(self.tags.keys()):
                if self.tags[key]:
                    value = self.tags[key] or ""
                    tags_str.append(f"{key}={_escape_tag(value)}")
                else:
                    tags_str.append(key)
            outs.append(f"@{';'.join(tags_str)}")

        if self.source:
            outs.append(f":{self.source}")
        outs.append(self.command.upper())

        params = self.params.copy()
        if self.params:
            last = params.pop(-1)
            for param in params:
                if " " in param:
                    raise ValueError("non last params cannot have spaces")
                elif param.startswith(":"):
                    raise ValueError("non last params cannot start with colon")
            outs.extend(params)

            if " " in last or last.startswith(":"):
                last = f":{last}"
            outs.append(last)
        return " ".join(outs)

def tokenise(line: str) -> Line:
    line_obj = Line()

    if line[0] == "@":
        message_tags, _, line = line.partition(" ")
        tags = {}
        for part in message_tags[1:].split(";"):
            key, _, value = part.partition("=")
            if value:
                tags[key] = _unescape_tag(value)
            else:
                tags[key] = None
        line_obj.tags = tags

    line, _, trailing = line.partition(" :")
    params = list(filter(bool, line.split(" ")))

    if params[0][0] == ":":
        line_obj.source = params.pop(0)[1:]

    line_obj.command = params.pop(0).upper()

    if trailing:
        params.append(trailing)
    line_obj.params = params

    return line_obj

def build(
        command: str,
        params:  List[str]=[],
        source:  Optional[str]=None,
        tags:    Optional[Dict[str, Optional[str]]]=None
        ) -> Line:
    return Line(tags, source, command, params)
