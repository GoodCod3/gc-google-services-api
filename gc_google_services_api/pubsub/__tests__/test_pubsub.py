import json
import unittest
from unittest.mock import Mock, patch

from gc_google_services_api.pubsub import PubSub

UUID_TEST = "84790aab-465c-4d91-808f-e8d6bfad6198"


def create_pubsub_mock(mock_pubsub_v1):
    publisher_mock = Mock()
    publisher_mock.topic_path.return_value = "TEST_TOPIC_RESPONSE"
    publisher_mock.publish.return_value = True

    mock_pubsub_v1.PublisherClient.from_service_account_info.return_value = (
        publisher_mock
    )

    return mock_pubsub_v1


def uuid_mock():
    uuid_mock = Mock()

    uuid_mock.uuid4.return_value = UUID_TEST

    return uuid_mock


class TestPubSub(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.project_name = "project_name"
        self.topic_name = "test_topic"
        self.credentials = "test_credentials"

    @patch("gc_google_services_api.pubsub.uuid", new=uuid_mock())
    @patch("gc_google_services_api.pubsub.pubsub_v1")
    def test_send_message_execute_publish_method_from_pubsub(
        self,
        mock_pubsub_v1,
    ):
        mock_pubsub_v1 = create_pubsub_mock(mock_pubsub_v1)
        data = {"key": "value"}
        pubsub_instance = PubSub(self.credentials, self.project_name)

        # Assert
        mock_pubsub_v1.PublisherClient.from_service_account_info.assert_called_once_with(  # noqa: E501
            info=self.credentials,
        )

        # Running send message
        pubsub_instance.send_message(self.topic_name, data)

        # Asserts
        expected_topic_path = "TEST_TOPIC_RESPONSE"
        expected_data = {"projects": data, "id": UUID_TEST}

        mock_pubsub_v1.PublisherClient.from_service_account_info().topic_path.assert_called_once_with(  # noqa: E501
            self.project_name,
            self.topic_name,
        )

        mock_pubsub_v1.PublisherClient.from_service_account_info().publish.assert_called_once_with(  # noqa: E501
            expected_topic_path,
            json.dumps(expected_data).encode("utf-8"),
        )

    # @patch("gc_google_services_api.pubsub_v1")
    # def test_terminate_message(self, mock_pubsub_v1):
    #     # Arrange
    #     pubsub = PubSub("credentials", "project")
    #     ack_id = "test_ack_id"
    #     message_id = "test_message_id"
    #     subscription_path = "test_subscription_path"

    #     # Act
    #     pubsub.terminate_message(ack_id, message_id, subscription_path)

    #     # Assert
    #     mock_pubsub_v1.SubscriberClient().acknowledge.assert_called_once_with(
    #         subscription=subscription_path,
    #         ack_ids=[ack_id],
    #     )

    # @patch("gc_google_services_api.pubsub_v1")
    # def test_subscribe_topic(self, mock_pubsub_v1):
    #     # Arrange
    #     pubsub = PubSub("credentials", "project")
    #     mock_response = MagicMock()
    #     mock_response.received_messages = [
    #         MagicMock(
    #             ack_id="test_ack_id",
    #             message=MagicMock(
    #                 data=b'{"projects": {"key": "value"}, "id": "test_message_id"}'  # noqa: E501
    #             ),
    #         )
    #     ]
    #     mock_pubsub_v1.types.PullResponse.return_value = mock_response

    #     topic_name = "test_topic"
    #     callback = MagicMock()
    #     max_simultaneous_messages = 2
    #     time_to_wait_between_messages = 5
    #     default_timeout_for_any_message = 60

    #     # Act
    #     pubsub.subscribe_topic(
    #         topic_name,
    #         callback,
    #         max_simultaneous_messages,
    #         time_to_wait_between_messages,
    #         default_timeout_for_any_message,
    #     )

    #     # Assert
    #     mock_pubsub_v1.SubscriberClient().pull.assert_called_once_with(
    #         request=mock_pubsub_v1.types.PullRequest(
    #             subscription=f"projects/{pubsub.project}/{topic_name}-sub",
    #             max_messages=max_simultaneous_messages,
    #         ),
    #         timeout=default_timeout_for_any_message,
    #     )
