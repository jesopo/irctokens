import unittest
import irctokens

class FormatTestTags(unittest.TestCase):
    def test(self):
        line = irctokens.build("PRIVMSG", ["#channel", "hello"],
            tags={"id": "\\" + " " + ";" + "\r\n"}).format()
        self.assertEqual(line, "@id=\\\\\\s\\:\\r\\n PRIVMSG #channel hello")

    def test_missing(self):
        line = irctokens.build("PRIVMSG", ["#channel", "hello"]).format()
        self.assertEqual(line, "PRIVMSG #channel hello")

    def test_none_value(self):
        line = irctokens.build("PRIVMSG", ["#channel", "hello"],
            tags={"a": None}).format()
        self.assertEqual(line, "@a PRIVMSG #channel hello")

    def test_empty_value(self):
        line = irctokens.build("PRIVMSG", ["#channel", "hello"], tags={"a": ""}
            ).format()
        self.assertEqual(line, "@a PRIVMSG #channel hello")

class FormatTestSource(unittest.TestCase):
    def test(self):
        line = irctokens.build("PRIVMSG", ["#channel", "hello"],
            source="nick!user@host").format()
        self.assertEqual(line, ":nick!user@host PRIVMSG #channel hello")

class FormatTestCommand(unittest.TestCase):
    def test_lowercase(self):
        line = irctokens.build("privmsg").format()
        self.assertEqual(line, "privmsg")
    def test_uppercase(self):
        line = irctokens.build("PRIVMSG").format()
        self.assertEqual(line, "PRIVMSG")

class FormatTestTrailing(unittest.TestCase):
    def test_space(self):
        line = irctokens.build("PRIVMSG", ["#channel", "hello world"]).format()
        self.assertEqual(line, "PRIVMSG #channel :hello world")

    def test_no_space(self):
        line = irctokens.build("PRIVMSG", ["#channel", "helloworld"]).format()
        self.assertEqual(line, "PRIVMSG #channel helloworld")

    def test_double_colon(self):
        line = irctokens.build("PRIVMSG", ["#channel", ":helloworld"]).format()
        self.assertEqual(line, "PRIVMSG #channel ::helloworld")

class FormatTestInvalidParam(unittest.TestCase):
    def test_non_last_space(self):
        def _inner():
            irctokens.build("USER", ["user", "0 *", "real name"]).format()
        self.assertRaises(ValueError, _inner)

    def test_non_last_colon(self):
        def _inner():
            irctokens.build("PRIVMSG", [":#channel", "hello"]).format()
        self.assertRaises(ValueError, _inner)
