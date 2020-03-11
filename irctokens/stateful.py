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

    def pending(self) -> bytes:
        return self._buffer

    def push(self, line: Line) -> bytes:
        self._buffer += f"{line.format()}\r\n".encode("utf8")
        return self._buffer
    def pop(self, byte_count: int):
        self._buffer = self._buffer[byte_count:]
