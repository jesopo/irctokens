import typing
from .protocol import Line, tokenise

class StatefulDecoder(object):
    def __init__(self, fallback: str="iso-8859"):
        self._fallback = fallback
        self._buffer = b""

    def push(self, data: bytes) -> typing.Optional[typing.List[Line]]:
        if not data:
            return None

        self._buffer += data
        lines = [l.strip(b"\r") for l in self._buffer.split(b"\n")]
        self._buffer = lines.pop(-1)

        decode_lines: typing.List[str] = []
        for line in lines:
            try:
                decode_lines.append(line.decode("utf8"))
            except UnicodeDecodeError as e:
                decode_lines.append(line.decode(self._fallback))
        return [tokenise(l) for l in decode_lines]

class StatefulEncoder(object):
    def __init__(self):
        self._buffer = b""
        self._buffered_lines: typing.List[Line] = []

    def pending(self) -> bytes:
        return self._buffer

    def push(self, line: Line) -> bytes:
        self._buffer += f"{line.format()}\r\n".encode("utf8")
        self._buffered_lines.append(line)
    def pop(self, byte_count: int):
        sent = self._buffer[:byte_count].count("\n")
        self._buffer = self._buffer[byte_count:]
        return [self._buffered_lines.pop(0) for _ in range(sent)]
