from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Hostmask:
    source: str
    nickname: str
    username: str | None
    hostname: str | None

    def __str__(self) -> str:
        return self.source

    def __repr__(self) -> str:
        return f"Hostmask({self.source})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hostmask):
            return False

        return self.source == other.source


def hostmask(source: str) -> Hostmask:
    username, _, hostname = source.partition("@")
    nickname, _, username = username.partition("!")

    return Hostmask(
        source=source,
        nickname=nickname,
        username=username or None,
        hostname=hostname or None,
    )
