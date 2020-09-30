import unittest
import irctokens

class TokenTestTags(unittest.TestCase):
    def test_missing(self):
        line = irctokens.tokenise("PRIVMSG #channel")
        self.assertIsNone(line.tags)

    def test_value_missing(self):
        line = irctokens.tokenise("@id= PRIVMSG #channel")
        self.assertEqual(line.tags["id"], "")

    def test_equal_missing(self):
        line = irctokens.tokenise("@id PRIVMSG #channel")
        self.assertEqual(line.tags["id"], "")

    def test_unescape(self):
        line = irctokens.tokenise(r"@id=1\\\:\r\n\s2 PRIVMSG #channel")
        self.assertEqual(line.tags["id"], "1\\;\r\n 2")

    def test_overlap(self):
        line = irctokens.tokenise(r"@id=1\\\s\\s PRIVMSG #channel")
        self.assertEqual(line.tags["id"], "1\\ \\s")

    def test_lone_end_slash(self):
        line = irctokens.tokenise("@id=1\\ PRIVMSG #channel")
        self.assertEqual(line.tags["id"], "1")

class TokenTestSource(unittest.TestCase):
    def test_without_tags(self):
        line = irctokens.tokenise(":nick!user@host PRIVMSG #channel")
        self.assertEqual(line.source, "nick!user@host")

    def test_with_tags(self):
        line = irctokens.tokenise("@id=123 :nick!user@host PRIVMSG #channel")
        self.assertEqual(line.source, "nick!user@host")

    def test_missing_without_tags(self):
        line = irctokens.tokenise("PRIVMSG #channel")
        self.assertIsNone(line.source)

    def test_missing_with_tags(self):
        line = irctokens.tokenise("@id=123 PRIVMSG #channel")
        self.assertIsNone(line.source)

class TokenTestCommand(unittest.TestCase):
    def test_lowercase(self):
        line = irctokens.tokenise("privmsg #channel")
        self.assertEqual(line.command, "PRIVMSG")

class TokenTestParams(unittest.TestCase):
    def test_trailing(self):
        line = irctokens.tokenise("PRIVMSG #channel :hello world")
        self.assertEqual(line.params, ["#channel", "hello world"])

    def test_only_trailing(self):
        line = irctokens.tokenise("PRIVMSG :hello world")
        self.assertEqual(line.params, ["hello world"])

    def test_no_params(self):
        line = irctokens.tokenise("PRIVMSG")
        self.assertEqual(line.command, "PRIVMSG")
        self.assertEqual(line.params, [])

class TokenTestAll(unittest.TestCase):
    def test_all(self):
        line = irctokens.tokenise(
            "@id=123 :nick!user@host PRIVMSG #channel :hello world")
        self.assertEqual(line.tags, {"id": "123"})
        self.assertEqual(line.source, "nick!user@host")
        self.assertEqual(line.command, "PRIVMSG")
        self.assertEqual(line.params, ["#channel", "hello world"])

class TokenTestNul(unittest.TestCase):
    def test(self):
        line = irctokens.tokenise(
            ":nick!user@host PRIVMSG #channel :hello\x00 world")
        self.assertEqual(line.params, ["#channel", "hello"])

class TokenTestNoCommand(unittest.TestCase):
    def test(self):
        def _test1():
            line = irctokens.tokenise(":n!u@h")
        def _test2():
            line = irctokens.tokenise("@tag=1 :n!u@h")

        self.assertRaises(ValueError, _test1)
        self.assertRaises(ValueError, _test2)

class TokenTestBytes(unittest.TestCase):
    def test(self):
        _str   = irctokens.tokenise("@a=1 :n!u@h PRIVMSG #chan :hello word")
        _bytes = irctokens.tokenise(b"@a=1 :n!u@h PRIVMSG #chan :hello word")

        self.assertEqual(_str, _bytes)
