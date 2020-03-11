import unittest
import irctokens

class TestPush(unittest.TestCase):
    def test(self):
        e = irctokens.StatefulEncoder()
        line = irctokens.tokenise("PRIVMSG #channel hello")
        e.push(line)
        self.assertEqual(e.pending(), b"PRIVMSG #channel hello\r\n")

class TestPop(unittest.TestCase):
    def test(self):
        e = irctokens.StatefulEncoder()
        line = irctokens.tokenise("PRIVMSG #channel hello")
        e.push(line)
        e.pop(len(b"PRIVMSG #channel hello"))
        self.assertEqual(e.pending(), b"\r\n")
