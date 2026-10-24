import unittest

from nasa_potd.message import build_message


class BuildMessageTest(unittest.TestCase):

    def test_format(self):
        message = build_message('Title', 'Body', 'https://example.com/a.png')
        self.assertEqual(message, '<b>Title</b>\n\nBody\nhttps://example.com/a.png')

    def test_escapes_html(self):
        message = build_message('A & B <tag>', "It's", 'https://example.com/a?x=1&y=2')
        self.assertEqual(
            message,
            '<b>A &amp; B &lt;tag&gt;</b>\n\nIt&#x27;s\nhttps://example.com/a?x=1&amp;y=2',
        )


if __name__ == '__main__':
    unittest.main()
