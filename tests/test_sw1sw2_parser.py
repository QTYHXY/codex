import unittest

from sw1sw2_parser import Meaning, decode_sw1sw2, normalize, parse_status


class SwParserTests(unittest.TestCase):
    def test_normalize_accepts_formats(self):
        self.assertEqual(normalize("6a82"), "6A82")
        self.assertEqual(normalize("0x6A 0x82"), "6A82")

    def test_exact_mapping(self):
        self.assertEqual(parse_status("9000"), Meaning("Normal processing", "Command successfully executed."))

    def test_retry_pattern(self):
        meaning = parse_status("63C2")
        self.assertEqual(meaning.category, "Warning")
        self.assertIn("2 retry", meaning.description)

    def test_6c_pattern(self):
        meaning = parse_status("6C10")
        self.assertIn("Correct Le is 16", meaning.description)

    def test_decode_helper(self):
        sw, meaning = decode_sw1sw2("0x6A 0x82")
        self.assertEqual(sw, "6A82")
        self.assertEqual(meaning.description, "File or application not found.")

    def test_unknown(self):
        self.assertEqual(parse_status("1234").category, "Unknown")


if __name__ == "__main__":
    unittest.main()
