import unittest
from unittest.mock import patch, MagicMock

from gc_google_services_api.pubsub import PubSub


class TestPubSub(unittest.TestCase):

    @patch('gc_google_services_api.pubsub_v1')
    def test_send_message(self, mock_pubsub_v1):
        # Arrange
        pubsub = PubSub()
        topic_name = "test_topic"
        data = {"key": "value"}

        # Act
        pubsub.send_message(topic_name, data)

        # Assert
        expected_topic_path = f"projects/{pubsub.PUBSUB_PROJECT}/topics/{topic_name}"
        expected_data = {"projects": data, "id": mock_pubsub_v1.UUID}
        mock_pubsub_v1.PublisherClient().publish.assert_called_once_with(expected_topic_path, expected_data)
