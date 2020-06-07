import unittest
from Data import DataParser


class TestProxy(unittest.TestCase):
    data = b'GET http://fanserials.haus/images/logo-grey.svg HTTP/1.1'\
           b'Host: fanserials.haus'\
           b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'\
           b'Accept: image/webp,*/*'\
           b'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'\
           b'Accept-Encoding: gzip, deflate'\
           b'Connection: keep-alive'\
           b'Referer: http://fanserials.haus/see/'\
           b'Cookie: _ym_uid=15759939561017780263; _ym_d=1575993956; _ym_wasSynced=%7B%22time%22%3A1575993956752%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; _ga=GA1.2.1332315211.1575993960; _gid=GA1.2.655025453.1575993960; _ym_hostIndex=0-2%2C1-2; __cfduid=d9f4fd90f9f6e616ec660d4530c8254ea1576081021; PHPSESSID=vp1f1cnhfmlnjq1h79j2fj3u1f; _ym_isad=2; _ym_visorc_50058067=b'\
           b'If-Modified-Since: Mon, 15 Jul 2019 10:57:08 GMT'\
           b'If-None-Match: "5d2c5c04-733"'\
           b'Cache-Control: max-age=0'

    def test_parse_method(self):
        method = DataParser.parse_method(TestProxy.data)
        expected = b'GET'
        self.assertEqual(expected, method)

    def test_parse_host(self):
        host = DataParser.parse_host_get(TestProxy.data)
        expected = b'fanserials.haus'
        self.assertEqual(expected, host)

    def test_parse_port_get(self):
        port = DataParser.parse_server_port_get(TestProxy.data)
        expected = 80
        self.assertEqual(expected, port)

    def test_create_config_get(self):
        config = DataParser.create_config(TestProxy.data)
        expected = {
            "port": 80,
            "host": b'fanserials.haus',
            "method": b'GET',
            "data": TestProxy.data
        }
        self.assertDictEqual(expected, config)

