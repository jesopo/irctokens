from typing import List, Optional
from .protocol import Line, tokenise

class StatefulDecoder(object):
    def __init__(self, encoding: str="utf8", fallback: str="latin-1"):
        self._encoding = encoding
        self._fallback = fallback
        self.clear()

    def clear(self):
        self._buffer = b""

    def pending(self) -> bytes:
        return self._buffer

    def push(self, data: bytes) -> Optional[List[Line]]:
        if not data:
            return None

        self._buffer += data
        lines = [l.strip(b"\r") for l in self._buffer.split(b"\n")]
        self._buffer = lines.pop(-1)

        decode_lines: List[str] = []
        for line in lines:
            try:
                decode_lines.append(line.decode(self._encoding))
            except UnicodeDecodeError as e:
                decode_lines.append(line.decode(self._fallback))
        return [tokenise(l) for l in decode_lines]

class StatefulEncoder(object):
    def __init__(self, encoding: str="utf8"):
        self._encoding = encoding
        self.clear()

    def clear(self):
        self._buffer = b""
        self._buffered_lines: List[Line] = []

    def pending(self) -> bytes:
        return self._buffer

    def push(self, line: Line):
        self._buffer += f"{line.format()}\r\n".encode(self._encoding)
        self._buffered_lines.append(line)

    def pop(self, byte_count: int):
        sent = self._buffer[:byte_count].count(b"\n")
        self._buffer = self._buffer[byte_count:]
        return [self._buffered_lines.pop(0) for _ in range(sent)]
