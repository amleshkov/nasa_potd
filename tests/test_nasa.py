import os
import unittest
from unittest import mock

from nasa_potd import config
from nasa_potd.nasa import NasaData


class ApiKeyTest(unittest.TestCase):

    @mock.patch('nasa_potd.nasa.requests.get')
    def test_key_from_env(self, get):
        get.return_value.json.return_value = [{'title': 'title'}]
        with mock.patch.dict('os.environ', {'NASA_API_KEY': 'MY_KEY'}):
            NasaData()
        self.assertEqual(get.call_args.kwargs['params']['api_key'], 'MY_KEY')

    @mock.patch('nasa_potd.nasa.requests.get')
    def test_key_defaults_to_demo(self, get):
        get.return_value.json.return_value = [{'title': 'title'}]
        env = {k: v for k, v in os.environ.items() if k != 'NASA_API_KEY'}
        with mock.patch.dict('os.environ', env, clear=True):
            NasaData()
        self.assertEqual(get.call_args.kwargs['params']['api_key'], 'DEMO_KEY')


class ProxyConfigTest(unittest.TestCase):

    def setUp(self):
        self.saved_proxy = config.proxy
        get_patcher = mock.patch('nasa_potd.nasa.requests.get')
        self.get = get_patcher.start()
        self.get.return_value.json.return_value = [{'title': 'title'}]
        self.addCleanup(get_patcher.stop)

    def tearDown(self):
        config.proxy = self.saved_proxy

    def test_disabled_by_default(self):
        config.proxy = None
        NasaData()
        self.assertIsNone(self.get.call_args.kwargs['proxies'])

    def test_enabled(self):
        config.proxy = 'socks5h://user:pass@host:1080'
        NasaData()
        self.assertEqual(
            self.get.call_args.kwargs['proxies'],
            {'http': 'socks5h://user:pass@host:1080',
             'https': 'socks5h://user:pass@host:1080'},
        )


class CleanTextTest(unittest.TestCase):

    def test_strips_html_and_service_lines(self):
        raw = (
            '<strong>Explanation:</strong> A <a href="https://example.com">comet</a> near '
            "Earth &amp; Mars.<br><br><strong>Tomorrow's picture:</strong> dark matters"
        )
        self.assertEqual(NasaData._clean_text(raw), 'A comet near Earth & Mars.')

    def test_removes_bare_urls(self):
        raw = 'See https://apod.nasa.gov/apod/ap260101.html and www.esa.int for details.'
        self.assertEqual(NasaData._clean_text(raw), 'See  and  for details.')

    def test_collapses_blank_lines(self):
        raw = 'One.<br><br><br><br>Two.'
        self.assertEqual(NasaData._clean_text(raw), 'One.\n\nTwo.')

    def test_keeps_plain_text(self):
        self.assertEqual(NasaData._clean_text('  Plain text.  '), 'Plain text.')


if __name__ == '__main__':
    unittest.main()
