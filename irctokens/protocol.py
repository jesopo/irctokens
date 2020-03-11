import typing

TAG_ESCAPE =   ["\\",   " ",  ";",   "\r",  "\n"]
TAG_UNESCAPE = ["\\\\", "\s", "\:", r"\r", r"\n"]

def _unescape_tag(value: str):
    for i, char in enumerate(TAG_UNESCAPE):
        value = value.replace(char, TAG_ESCAPE[i])
    return value
def _escape_tag(value: str):
    for i, char in enumerate(TAG_ESCAPE):
        value = value.replace(char, TAG_UNESCAPE[i])
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

class Line(object):
    def __init__(self,
            tags:
                typing.Optional[typing.Dict[str, typing.Optional[str]]]=None,
            source:  typing.Optional[str]=None,
            command: str="",
            params:  typing.List[str]=[]):
        self.tags    = tags
        self.source  = source
        self.command = command
        self.params  = params

    def __eq__(self, other):
        if isinstance(other, Line):
            return self.format() == other.format()
        else:
            return False

    def format(self) -> str:
        outs: typing.List[str] = []
        if self.tags:
            tags_str = []
            for key in sorted(self.tags.keys()):
                if self.tags[key]:
                    tags_str.append(
                        "%s=%s" % (key, _escape_tag(self.tags[key] or "")))
                else:
                    tags_str.append(key)
            outs.append("@%s" % ";".join(tags_str))

        if self.source:
            outs.append(":%s" % self.source)
        outs.append(self.command.upper())

        params = self.params.copy()
        if self.params:
            last = params.pop(-1)
            outs.extend(params)
            if " " in last:
                last = ":%s" % last
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

def format(
        command: str,
        params:  typing.List[str]=[],
        source:  typing.Optional[str]=None,
        tags:    typing.Optional[typing.Dict[str, typing.Optional[str]]]=None
        ) -> str:
    return Line(tags, source, command, params).format()
