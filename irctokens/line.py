from typing      import Dict, List, Optional
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

def _tokenise(
        tags_s: Optional[str],
        line:   str
        ) -> Line:

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

    return Line(tags, source, command, params)

def tokenise_b(
        line_b:   bytes,
        encoding: str="utf8",
        fallback: str="latin-1"
        ) -> Line:

    if b"\x00" in line_b:
        line_b, _ = line_b.split(b"\x00", 1)

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
    if "\x00" in line:
        line, _ = line.split("\x00", 1)

    if line[0] == "@":
        tags, _, line = line.partition(" ")
        return _tokenise(tags, line)
    else:
        return _tokenise(None, line)
