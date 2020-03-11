import unittest
import irctokens

class TestTags(unittest.TestCase):
    def test(self):
        line = irctokens.format("PRIVMSG", ["#channel", "hello"],
            tags={"id": "\\" + " " + ";" + "\r\n"})
        self.assertEqual(line, r"@id=\\\s\:\r\n PRIVMSG #channel hello")

    def test_missing(self):
        line = irctokens.format("PRIVMSG", ["#channel", "hello"])
        self.assertEqual(line, "PRIVMSG #channel hello")

    def test_none_value(self):
        line = irctokens.format("PRIVMSG", ["#channel", "hello"],
            tags={"a": None})
        self.assertEqual(line, "@a PRIVMSG #channel hello")

    def test_empty_value(self):
        line = irctokens.format("PRIVMSG", ["#channel", "hello"],
            tags={"a": ""})
        self.assertEqual(line, "@a PRIVMSG #channel hello")

class TestSource(unittest.TestCase):
    def test(self):
        line = irctokens.format("PRIVMSG", ["#channel", "hello"],
            source="nick!user@host")
        self.assertEqual(line, ":nick!user@host PRIVMSG #channel hello")

class TestCommand(unittest.TestCase):
    def test_lowercase(self):
        line = irctokens.format("privmsg")
        self.assertEqual(line, "PRIVMSG")

class TestTrailing(unittest.TestCase):
    def test_space(self):
        line = irctokens.format("PRIVMSG", ["#channel", "hello world"])
        self.assertEqual(line, "PRIVMSG #channel :hello world")

    def test_no_space(self):
        line = irctokens.format("PRIVMSG", ["#channel", "helloworld"])
        self.assertEqual(line, "PRIVMSG #channel helloworld")
