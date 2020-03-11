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
import sockets
import irctokens

sock = socket.socket()
sock.connect(("127.0.0.1", 6667))

line = irctokens.format("USER", ["user", "0", "*", "real name"])
to_send = "%s\r\n" % line
sock.send(to_send.encode("utf8"))
```
