# irctokens

[![Build Status](https://travis-ci.org/jesopo/irctokens.svg?branch=master)](https://travis-ci.org/jesopo/irctokens)

## rationale

there's far too many IRC client implementations out in the world that do not
tokenise data correctly and thus fall victim to things like colons either being
where you don't expect them or not being where you expect them.

## usage

### tokenisation
```python
import irctokens

line = irctokens.tokenise(
    "@id=123 :jess!~jess@hostname PRIVMSG #chat :hello there!")

if line.command == "PRIVMSG":
    print(f"received message from {line.source}"
          f" to {line.params[0]}: {line.params[1]}")
```

### formatting

```python
>>> import irctokens
>>> irctokens.format("USER", ["user", "0", "*", "real name"])
'USER user 0 * :real name'
```

### stateful
```python
import irctokens, socket

d = irctokens.StatefulDecoder()
s = socket.socket()
s.connect(("127.0.0.1", 6667))

def _send(line):
    s.send(f"{line}\r\n".encode("utf8"))

_send(irctokens.format("USER", ["username", "0", "*", "real name"]))
_send(irctokens.format("NICK", ["nickname"]))

while True:
    lines = d.push(s.recv(1024))
    if lines == None:
        print("! disconnected")
        break

    for line in lines:
        if line.command == "PING":
            to_send = irctokens.format("PONG", [line.params[0]])
            _send(to_send)

        elif line.command == "001":
            to_send = irctokens.format("JOIN", ["#test"])
            _send(to_send)
```
