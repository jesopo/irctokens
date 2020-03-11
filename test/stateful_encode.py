import unittest
import irctokens

class EncodeTestPush(unittest.TestCase):
    def test(self):
        e = irctokens.StatefulEncoder()
        line = irctokens.tokenise("PRIVMSG #channel hello")
        e.push(line)
        self.assertEqual(e.pending(), b"PRIVMSG #channel hello\r\n")

class EncodeTestPop(unittest.TestCase):
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

class EncodeTestClear(unittest.TestCase):
    def test(self):
        e = irctokens.StatefulEncoder()
        e.push(irctokens.tokenise("PRIVMSG #channel hello"))
        e.clear()
        self.assertEqual(e.pending(), b"")

class EncodeTestEncoding(unittest.TestCase):
    def test(self):
        e = irctokens.StatefulEncoder(encoding="iso-8859-2")
        e.push(irctokens.tokenise("PRIVMSG #channel :hello Č"))
        self.assertEqual(e.pending(),
            "PRIVMSG #channel :hello Č\r\n".encode("iso-8859-2"))
