from typing import Dict, List, Optional
from .const import TAG_ESCAPED, TAG_UNESCAPED

def _escape_tag(value: str):
    for i, char in enumerate(TAG_UNESCAPED):
        value = value.replace(char, TAG_ESCAPED[i])
    return value

def format(
        tags:    Optional[Dict[str, str]],
        source:  Optional[str],
        command: str,
        params:  List[str]):
    outs: List[str] = []
    if tags:
        tags_str = []
        for key in sorted(tags.keys()):
            if tags[key]:
                value = tags[key]
                tags_str.append(f"{key}={_escape_tag(value)}")
            else:
                tags_str.append(key)
        outs.append(f"@{';'.join(tags_str)}")

    if source is not None:
        outs.append(f":{source}")
    outs.append(command)

    params = params.copy()
    if params:
        last = params.pop(-1)
        for param in params:
            if " " in param:
                raise ValueError("non last params cannot have spaces")
            elif param.startswith(":"):
                raise ValueError("non last params cannot start with colon")
        outs.extend(params)

        if (not last or
                " " in last or
                last.startswith(":")):
            last = f":{last}"
        outs.append(last)
    return " ".join(outs)
