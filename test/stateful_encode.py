import unittest
import irctokens

class TestPush(unittest.TestCase):
    def test(self):
        e = irctokens.StatefulEncoder()
        line = irctokens.tokenise("PRIVMSG #channel hello")
        e.push(line)
        self.assertEqual(e.pending(), b"PRIVMSG #channel hello\r\n")

class TestPop(unittest.TestCase):
    def test_partial(self):
        e = irctokens.StatefulEncoder()
        line = irctokens.tokenise("PRIVMSG #channel hello")
        e.push(line)
        e.pop(len(b"PRIVMSG #channel hello"))
        self.assertEqual(e.pending(), b"\r\n")

    def test_returned(self):
        e = irctokens.StatefulEncoder()
        line = irctokens.tokenise("PRIVMSG #channel hello")
        e.push(line)
        e.push(line)
        lines = e.pop(len(b"PRIVMSG #channel hello\r\nPRIVMSG"))
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], line)

    def test_none_returned(self):
        e = irctokens.StatefulEncoder()
        line = irctokens.tokenise("PRIVMSG #channel hello")
        e.push(line)
        lines = e.pop(1)
        self.assertEqual(len(lines), 0)

class TestClear(unittest.TestCase):
    def test(self):
        e = irctokens.StatefulEncoder()
        e.push(irctokens.tokenise("PRIVMSG #channel hello"))
        e.clear()
        self.assertEqual(e.pending(), b"")
