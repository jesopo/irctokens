# irctokens

[![Build Status](https://travis-ci.org/jesopo/irctokens.svg?branch=master)](https://travis-ci.org/jesopo/irctokens)

## rationale

there's far too many IRC client implementations out in the world that do not
tokenise data correctly and thus fall victim to things like colons either being
where you don't expect them or not being where you expect them.

## usage

### installation

`$ pip3 install irctokens`

### tokenisation
```python
>>> import irctokens
>>> line = irctokens.tokenise(
...     "@id=123 :jess!~jess@hostname PRIVMSG #chat :hello there!")
>>>
>>> line.tags
{'id': '123'}
>>> line.source
'jess!~jess@hostname'
>>> line.hostmask
Hostmask(nickname='jess', username='~jess', hostname='hostname')
>>> line.command
'PRIVMSG'
>>> line.params
['#chat', 'hello there!']
```

### formatting

```python
>>> irctokens.build("USER", ["user", "0", "*", "real name"]).format()
'USER user 0 * :real name'
```

### stateful

below is an example of a fully socket-wise safe IRC client connection that will
connect and join a channel. both protocol sending and receiving are handled by
irctokens.

```python

import irctokens, socket

NICK = "nickname"
CHAN = "#channel"

d = irctokens.StatefulDecoder()
e = irctokens.StatefulEncoder()
s = socket.socket()
s.connect(("127.0.0.1", 6667))

def _send(line):
    print(f"> {line.format()}")
    e.push(line)
    while e.pending():
        e.pop(s.send(e.pending()))

_send(irctokens.build("USER", ["username", "0", "*", "real name"]))
_send(irctokens.build("NICK", [NICK]))

while True:
    lines = d.push(s.recv(1024))
    if lines == None:
        print("! disconnected")
        break

    for line in lines:
        print(f"< {line.format()}")
        if line.command == "PING":
            to_send = irctokens.build("PONG", [line.params[0]])
            _send(to_send)

        elif line.command == "001":
            to_send = irctokens.build("JOIN", [CHAN])
            _send(to_send)
```

## contact

Come say hi at `#irctokens` on irc.libera.chat
