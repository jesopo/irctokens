from typing import Optional

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
        return f"Hostmask({self._source})"
    def __eq__(self, other) -> bool:
        if isinstance(other, Hostmask):
            return str(self) == str(other)
        else:
            return False

def hostmask(source: str) -> Hostmask:
    username, _, hostname = source.partition("@")
    nickname, _, username = username.partition("!")
    return Hostmask(
        source,
        nickname,
        username or None,
        hostname or None)
