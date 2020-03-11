import typing

TAG_ESCAPE =   ["\\",   " ",  ";",   "\r",  "\n"]
TAG_UNESCAPE = ["\\\\", "\s", "\:", r"\r", r"\n"]

class Line(object):
    tags: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    source: typing.Optional[str] = None
    command: str = ""
    params: typing.List[str] = []

def _escape_tag(value: str):
    for i, char in enumerate(TAG_ESCAPE):
        value = value.replace(char, TAG_UNESCAPE[i])
    return value

def tokenise(line: str) -> Line:
    line_obj = Line()

    if line[0] == "@":
        message_tags, _, line = line.partition(" ")
        tags = {}
        for part in message_tags[1:].split(";"):
            key, _, value = part.partition("=")
            tags[key] = _escape_tag(value)
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
