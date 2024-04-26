import unittest
from unittest.mock import patch, MagicMock

from gc_google_services_api.pubsub import PubSub


class TestPubSub(unittest.TestCase):

    @patch("gc_google_services_api.pubsub_v1")
    def test_send_message(self, mock_pubsub_v1):
        # Arrange
        pubsub = PubSub("credentials", "project")
        topic_name = "test_topic"
        data = {"key": "value"}

        # Act
        pubsub.send_message(topic_name, data)

        # Assert
        expected_topic_path = f"projects/{pubsub.PUBSUB_PROJECT}/topics/{topic_name}"
        expected_data = {"projects": data, "id": mock_pubsub_v1.UUID}
        mock_pubsub_v1.PublisherClient().publish.assert_called_once_with(
            expected_topic_path, expected_data
        )

    @patch("gc_google_services_api.pubsub_v1")
    def test_terminate_message(self, mock_pubsub_v1):
        # Arrange
        pubsub = PubSub("credentials", "project")
        ack_id = "test_ack_id"
        message_id = "test_message_id"
        subscription_path = "test_subscription_path"

        # Act
        pubsub.terminate_message(ack_id, message_id, subscription_path)

        # Assert
        mock_pubsub_v1.SubscriberClient().acknowledge.assert_called_once_with(
            subscription=subscription_path,
            ack_ids=[ack_id],
        )

    @patch("gc_google_services_api.pubsub_v1")
    def test_subscribe_topic(self, mock_pubsub_v1):
        # Arrange
        pubsub = PubSub("credentials", "project")
        mock_response = MagicMock()
        mock_response.received_messages = [
            MagicMock(
                ack_id="test_ack_id",
                message=MagicMock(
                    data=b'{"projects": {"key": "value"}, "id": "test_message_id"}'
                ),
            )
        ]
        mock_pubsub_v1.types.PullResponse.return_value = mock_response

        topic_name = "test_topic"
        callback = MagicMock()
        max_simultaneous_messages = 2
        time_to_wait_between_messages = 5
        default_timeout_for_any_message = 60

        # Act
        pubsub.subscribe_topic(
            topic_name,
            callback,
            max_simultaneous_messages,
            time_to_wait_between_messages,
            default_timeout_for_any_message,
        )

        # Assert
        mock_pubsub_v1.SubscriberClient().pull.assert_called_once_with(
            request=mock_pubsub_v1.types.PullRequest(
                subscription=f"projects/{pubsub.project}/{topic_name}-sub",
                max_messages=max_simultaneous_messages,
            ),
            timeout=default_timeout_for_any_message,
        )
