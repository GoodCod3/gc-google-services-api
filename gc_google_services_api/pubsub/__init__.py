import json
import logging
import time
import uuid
from typing import Callable

from google.cloud import pubsub_v1
from google.auth import impersonated_credentials
from google.auth.transport import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

MAX_SIMULTANEOUS_MESSAGES = 1
TIME_TO_WAIT_BETWEEN_MESSAGES = 10  # Seconds
DEFAULT_TIMEOUT_FOR_ANY_MESSAGE = 6 * 60  # 6 minutes


class PubSub:
    def __init__(self, project, service_account_email):
        self.project = project
        self.service_account_email = service_account_email

        self.credentials = self._get_impersonated_credentials()
        self.publisher = pubsub_v1.PublisherClient.from_service_account_info(
            info=GOOGLE_SERVICE_ACCOUNT_CREDENTIALS,
        )
        self.subscriber = pubsub_v1.SubscriberClient.from_service_account_info(
            info=GOOGLE_SERVICE_ACCOUNT_CREDENTIALS,
        )

    def _get_impersonated_credentials(self):
        target_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        target_credentials = impersonated_credentials.Credentials(
            source_credentials=requests.Request(),
            target_principal=self.service_account_email,
            target_scopes=target_scopes,
        )
        return target_credentials
    
    def send_message(self, topic_name: str, data: dict):
        topic_path = self.publisher.topic_path(self.project, topic_name)
        self.publisher.publish(
            topic_path,
            json.dumps(
                {
                    "data": data,
                    "id": str(uuid.uuid4()),
                }
            ).encode("utf-8"),
        )

    def terminate_message(
        self,
        ack_id: str,
        message_id: str,
        subscription_path,
    ):
        logging.info(f"Terminating message: {message_id}")
        self.subscriber.acknowledge(
            subscription=subscription_path,
            ack_ids=[ack_id],
        )

    def subscribe_topic(self, topic_name: str, callback: Callable[[], str]):
        subscription_path = self.subscriber.subscription_path(
            self.project,
            f"{topic_name}-sub",
        )

        request = pubsub_v1.types.PullRequest(
            subscription=subscription_path,
            max_messages=MAX_SIMULTANEOUS_MESSAGES,
        )

        while True:
            try:
                response = self.subscriber.pull(
                    request=request,
                    timeout=DEFAULT_TIMEOUT_FOR_ANY_MESSAGE,
                )

                if not response.received_messages:
                    logging.error("Closing the subscription to the topic due to lack of messages")
                    break
                else:
                    for received_message in response.received_messages:
                        message_id = received_message.ack_id
                        message_data = received_message.message.data

                        message_data_json = json.loads(message_data)
                        batch_message_id = message_data_json["id"]

                        # logging.info(f"Processing message ({batch_message_id})")

                        # Processing projects
                        callback(message_data)

                        logging.info(f"Message ({batch_message_id}) processed.")
                        time.sleep(TIME_TO_WAIT_BETWEEN_MESSAGES)
                        self.terminate_message(
                            ack_id=message_id,
                            message_id=batch_message_id,
                            subscription_path=subscription_path,
                        )
            except Exception as e:
                import traceback
                traceback.print_exc()

                logging.error(f"Error processing project with error: {e}")
