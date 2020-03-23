import os.path, unittest
import yaml
import irctokens

# run test cases sourced from:
# https://github.com/ircdocs/parser-tests

dir      = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(dir, "_data")

class ParserTestsSplit(unittest.TestCase):
    def test_split(self):
        data_path = os.path.join(data_dir, "msg-split.yaml")
        with open(data_path) as data_file:
            tests = yaml.safe_load(data_file.read())["tests"]

        for test in tests:
            input = test["input"]
            atoms = test["atoms"]

            tokens = irctokens.tokenise(input)

            self.assertEqual(tokens.tags,    atoms.get("tags", None))
            self.assertEqual(tokens.source,  atoms.get("source", None))
            self.assertEqual(tokens.command, atoms["verb"].upper())
            self.assertEqual(tokens.params,  atoms.get("params", []))

    def test_join(self):
        data_path = os.path.join(data_dir, "msg-join.yaml")
        with open(data_path) as data_file:
            tests = yaml.safe_load(data_file.read())["tests"]

        for test in tests:
            atoms   = test["atoms"]
            matches = test["matches"]

            line = irctokens.build(
                atoms["verb"],
                atoms.get("params", []),
                source=atoms.get("source", None),
                tags=atoms.get("tags", None)).format()

            self.assertIn(line, matches)
