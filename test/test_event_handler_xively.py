#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import time
import unittest
from datetime import datetime
from event_listener.handler import XivelyEventHandler

try:
    from unittest.mock import call
except ImportError:
    from mock import call

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


class TestXivelyEventHandler(unittest.TestCase):
    """test KeenIoHandler class."""

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("event_listener.handler.xively.Datastream", autospec=True)
    @patch("event_listener.handler.xively.XivelyAPIClient", autospec=True)
    def test_post_data_to_xively(self, mocked_api_client, mocked_datastream):
        client = MagicMock()
        client.update = MagicMock(return_value=None)
        api = MagicMock()
        api.feeds = MagicMock()
        api.feeds.get = MagicMock(return_value=client)
        mocked_api_client.return_value = api

        xively_handler = XivelyEventHandler(
            api_key="dummy_api_key",
            feed_key="dummy_feed_key")

        data = {}
        data['source'] = 'solar'
        data['at'] = datetime.now()
        data['data'] = {
            'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.4},
            'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41}}

        xively_handler.start()
        xively_handler.put_q(data)
        xively_handler.join_q()
        xively_handler.stop()
        xively_handler.join()

        mocked_api_client.assert_called_once_with("dummy_api_key")
        api.feeds.get.assert_called_once_with("dummy_feed_key")

        calls = [
            call(id="ArrayCurrent", current_value=1.4, at=data["at"]),
            call(id="ArrayVoltage", current_value=53.41, at=data["at"]),
        ]
        mocked_datastream.assert_has_calls(calls, any_order=True)

        self.assertEqual(2, len(client.datastreams))
        client.update.assert_called_once_with()

    def test_init_xively_with_invalid_key(self):
        import requests

        self.assertRaises(
            requests.exceptions.HTTPError,
            XivelyEventHandler,
            api_key="dummy_api_key",
            feed_key="dummy_feed_key")

    @patch("event_listener.handler.xively.XivelyAPIClient", autospec=True)
    def test_post_data_failed_with_exception(self, mocked_api_client):
        class ConnectionError(Exception):
            pass

        client = MagicMock()
        client.update = MagicMock(return_value=None)
        api = MagicMock()
        api.feeds = MagicMock()
        api.feeds.get = MagicMock(return_value=client)
        mocked_api_client.side_effect = ConnectionError

        xively_handler = XivelyEventHandler(
            api_key="dummy_api_key",
            feed_key="dummy_feed_key")

        data = {}
        data['source'] = 'solar'
        data['at'] = datetime.now()
        data['data'] = {
            'Array Current': {'group': 'Array', 'unit': 'A', 'value': 1.4},
            'Array Voltage': {'group': 'Array', 'unit': 'V', 'value': 53.41}}

        xively_handler.start()
        xively_handler.put_q(data)
        xively_handler.join_q()

        # ConnectionError発生時は１秒待って再送を３回繰り返す
        time.sleep(5)

        xively_handler.stop()
        xively_handler.join()

        self.assertEqual(mocked_api_client.call_count, 3)

        if sys.version_info[:3] >= (3, 5, 0):
            api.feeds.get.assert_not_called()
            client.update.assert_not_called()
        else:
            self.assertEqual(api.feeds.get.call_count, 0)
            self.assertEqual(client.update.call_count, 0)


if __name__ == "__main__":
    unittest.main()
