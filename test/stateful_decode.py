import unittest
import irctokens

class TestPartial(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder()
        lines = d.push(b"PRIVMSG ")
        self.assertEqual(lines, [])

        lines = d.push(b"#channel hello\r\n")
        self.assertEqual(len(lines), 1)
        line = irctokens.tokenise("PRIVMSG #channel hello")
        self.assertEqual(lines, [line])

class TestMultiple(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder()
        lines = d.push(b"PRIVMSG #channel1 hello\r\n"
                       b"PRIVMSG #channel2 hello\r\n")
        self.assertEqual(len(lines), 2)

        line1 = irctokens.tokenise("PRIVMSG #channel1 hello")
        line2 = irctokens.tokenise("PRIVMSG #channel2 hello")
        self.assertEqual(lines[0], line1)
        self.assertEqual(lines[1], line2)

class TestFallback(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder(fallback="latin-1")
        lines = d.push("PRIVMSG #channel hélló\r\n".encode("latin-1"))
        self.assertEqual(len(lines), 1)
        line = irctokens.tokenise("PRIVMSG #channel hélló")
        self.assertEqual(lines[0], line)
