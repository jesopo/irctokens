import unittest
import irctokens

class DecodeTestPartial(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder()
        lines = d.push(b"PRIVMSG ")
        self.assertEqual(lines, [])

        lines = d.push(b"#channel hello\r\n")
        self.assertEqual(len(lines), 1)
        line = irctokens.tokenise("PRIVMSG #channel hello")
        self.assertEqual(lines, [line])

class DecodeTestMultiple(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder()
        lines = d.push(b"PRIVMSG #channel1 hello\r\n"
                       b"PRIVMSG #channel2 hello\r\n")
        self.assertEqual(len(lines), 2)

        line1 = irctokens.tokenise("PRIVMSG #channel1 hello")
        line2 = irctokens.tokenise("PRIVMSG #channel2 hello")
        self.assertEqual(lines[0], line1)
        self.assertEqual(lines[1], line2)

class DecodeTestEncoding(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder(encoding="iso-8859-2")
        lines = d.push("PRIVMSG #channel :hello Č\r\n".encode("iso-8859-2"))
        line = irctokens.tokenise("PRIVMSG #channel :hello Č")
        self.assertEqual(lines[0], line)
    def test_fallback(self):
        d = irctokens.StatefulDecoder(fallback="latin-1")
        lines = d.push("PRIVMSG #channel hélló\r\n".encode("latin-1"))
        self.assertEqual(len(lines), 1)
        line = irctokens.tokenise("PRIVMSG #channel hélló")
        self.assertEqual(lines[0], line)

class DecodeTestEmpty(unittest.TestCase):
    def test_immediate(self):
        d = irctokens.StatefulDecoder()
        lines = d.push(b"")
        self.assertIsNone(lines)

    def test_buffer_unfinished(self):
        d = irctokens.StatefulDecoder()
        d.push(b"PRIVMSG #channel hello")
        lines = d.push(b"")
        self.assertIsNone(lines)

class DecodeTestClear(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder()
        d.push(b"PRIVMSG ")
        d.clear()
        self.assertEqual(d.pending(), b"")

class DecodeTestTagEncodingMismatch(unittest.TestCase):
    def test(self):
        d = irctokens.StatefulDecoder()
        d.push("@asd=á ".encode("utf8"))
        lines = d.push("PRIVMSG #chan :á\r\n".encode("latin-1"))

        self.assertEqual(lines[0].params[1],   "á")
        self.assertEqual(lines[0].tags["asd"], "á")
