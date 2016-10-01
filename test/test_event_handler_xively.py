#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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


if __name__ == "__main__":
    unittest.main()
