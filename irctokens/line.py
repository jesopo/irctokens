from typing      import Dict, List, Optional, Union
from .const      import TAG_ESCAPED, TAG_UNESCAPED
from .hostmask   import Hostmask, hostmask
from .formatting import format as format_

class Line(object):
    def __init__(self,
            tags:    Optional[Dict[str, str]],
            source:  Optional[str],
            command: str,
            params:  List[str]):
        self.tags    = tags
        self.source  = source
        self.command = command
        self.params  = params

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
    def hostmask(self) -> Hostmask:
        if self.source is not None:
            if self._hostmask is None:
                self._hostmask = hostmask(self.source)
            return self._hostmask
        else:
            raise ValueError("cannot parse hostmask from null source")

    def format(self) -> str:
        return format_(self.tags, self.source, self.command, self.params)

    def with_source(self, source: str) -> "Line":
        return Line(self.tags, source, self.command, self.params)
    def copy(self) -> "Line":
        return Line(self.tags, self.source, self.command, self.params)

def build(
        command: str,
        params:  List[str]=[],
        source:  Optional[str]=None,
        tags:    Optional[Dict[str, str]]=None
        ) -> Line:
    return Line(tags, source, command, params)

def _unescape_tag(value: str) -> str:
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

def _tokenise(line: str) -> Line:
    tags: Optional[Dict[str, str]] = None
    if line[0] == "@":
        tags_s, _, line = line.partition(" ")
        tags = {}
        for part in tags_s[1:].split(";"):
            key, _, value = part.partition("=")
            tags[key]     = _unescape_tag(value)

    line, trailing_sep, trailing = line.partition(" :")
    params = list(filter(bool, line.split(" ")))

    source: Optional[str] = None
    if params[0][0] == ":":
        source = params.pop(0)[1:]

    if not params:
        raise ValueError("Cannot tokenise command-less line")
    command = params.pop(0).upper()

    if trailing_sep:
        params.append(trailing)

    return Line(tags, source, command, params)

def tokenise(
        line:     Union[str, bytes],
        encoding: str="utf8",
        fallback: str="latin-1"
        ) -> Line:

    dline: str = ""
    if isinstance(line, bytes):
        if line[0] == ord(b"@"):
            tags_b, sep, line = line.partition(b" ")
            dline += (tags_b+sep).decode("utf8")
        try:
            dline += line.decode(encoding)
        except UnicodeDecodeError:
            dline += line.decode(fallback)
    else:
        dline = line

    if "\x00" in dline:
        dline, _ = dline.split("\x00", 1)

    return _tokenise(dline)
