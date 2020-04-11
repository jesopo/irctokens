from typing import Callable, Dict, List, Optional

class Hostmask(object):
    def __init__(self, source: str,
            nickname: str,
            username: Optional[str],
            hostname: Optional[str]):
        self._source = source
        self.nickname = nickname
        self.username = username
        self.hostname = hostname

    def __str__(self) -> str:
        return self._source
    def __repr__(self) -> str:
        return (f"Hostmask(nick={self.nickname!r}, user={self.username!r}"
           f", host={self.hostname!r})")
    def __eq__(self, other) -> bool:
        if isinstance(other, Hostmask):
            return str(self) == str(other)
        else:
            return False

    @staticmethod
    def from_source(source: str):
        username, _, hostname = source.partition("@")
        nickname, _, username = username.partition("!")
        return Hostmask(source, nickname, username or None, hostname or None)

class Line(object):
    def __init__(self,
            tags:    Optional[Dict[str, str]],
            source:  Optional[str],
            command: str,
            params:  List[str],
            format:  Callable[["Line"], str]):
        self.tags    = tags
        self.source  = source
        self.command = command
        self.params  = params
        self._format = format

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
        if self.source and not self._hostmask:
            self._hostmask = Hostmask.from_source(self.source)
        return self._hostmask

    def format(self) -> str:
        return self._format(self)