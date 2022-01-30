from __future__ import annotations

from .line import Line, tokenise


class StatefulDecoder:
    def __init__(self, encoding: str = "utf8", fallback: str = "latin-1"):
        self._encoding = encoding
        self._fallback = fallback
        self.clear()

    def clear(self):
        self._buffer = b""

    def pending(self) -> bytes:
        return self._buffer

    def push(self, data: bytes) -> list[Line] | None:
        if not data:
            return None

        self._buffer += data
        lines_b = [ln.strip(b"\r") for ln in self._buffer.split(b"\n")]
        self._buffer = lines_b.pop(-1)

        lines: list[Line] = []
        for line in lines_b:
            lines.append(tokenise(line, self._encoding, self._fallback))

        return lines


class StatefulEncoder:
    def __init__(self, encoding: str = "utf8"):
        self._encoding = encoding
        self.clear()

    def clear(self):
        self._buffer = b""
        self._buffered_lines: list[Line] = []

    def pending(self) -> bytes:
        return self._buffer

    def push(self, line: Line):
        self._buffer += f"{line.format()}\r\n".encode(self._encoding)
        self._buffered_lines.append(line)

    def pop(self, byte_count: int):
        sent = self._buffer[:byte_count].count(b"\n")
        self._buffer = self._buffer[byte_count:]

        return [self._buffered_lines.pop(0) for _ in range(sent)]
