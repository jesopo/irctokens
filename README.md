# irctokens

## rationale

there's far too many IRC client implementations out in the world that do not
tokenise data correctly and thus fall victim to things like colons either being
where you don't expect them or not being where you expect them.

## usage

```python
import irctokens
line = irctokens.tokenise(
    "@id=123 :jess!~jess@hostname PRIVMSG #chat :hello there!")

print(f"tags:    {line.tags}")
print(f"source:  {line.source}")
print(f"command: {line.command}")
print(f"params:  {line.params}")
```
