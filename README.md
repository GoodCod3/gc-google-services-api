[![Publish to PyPI.org](https://github.com/GoodCod3/gc-google-services-api/actions/workflows/pr.yml/badge.svg)](https://github.com/GoodCod3/gc-google-services-api/actions/workflows/pr.yml)

# How to contribute
After clone repository
## 1.- Install dependencies
```bash
poetry install
```

## 2.- Run test
```bash
make test
```

# Publish new version
When your Pull Request is approved and merged with master, then to can generate new version running the next command:

```bash
make v=X.Y.Z release
```
or you can execute
```bash
poetry version X.Y.Z <-- (New version)
git commit -am "Release vX.Y.Z"
git tag vX.Y.Z
git push --follow-tags
```

Google services API
=============================
This repository is a suite that exposes Google services to easily integrate with our project (Big query, Google sheet, Gmail, etc...).

Each api needs a different form of authentication, either because it requires the interaction of a person who approves the api to extract sensitive information or because we want to connect automatically without user intervention.



What APIs and methods does it support?
=======================
This project will grow as new services and methods are integrated.

Here is a list of current support

## Big Query
----------------------------------

### execute_query (Method):
Allows you to run a query on a Big Query table.

In order for the api to connect to the table, it is necessary to configure the environment variable `$GOOGLE_APPLICATION_CREDENTIALS` indicating the path of the file with the credentials (service account json file)

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/service_account_file.json
```

### Usage example

```python
from gc_google_services_api.bigquery import execute_query


query = "SELECT * FROM users;"
users = execute_query(query)

for user in users:
    print(user)
```

## Google sheet
----------------------------------

## 1.- **read_gsheet** (Method of a class):
Allows to read and return the content of a Google sheet link.
It is necessary to indicate the range of columns that we want to return

In order for the api to connect with Google, it is necessary to send the JSON content of your service account.
the format of the service account should be something like this:

```
{
  "type": "service_account",
  "project_id": "XXXXXX",
  "private_key_id": "XXXXXX",
  "private_key": "XXXXXX",
  "client_email": "XXXXXX",
  "client_id": "XXXXXX",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/XXXXXX"
}

```

### Usage example

```python
from gc_google_services_api.gsheet import GSheet


name = 'Sheet 1'
spreadsheet_id = '11111111'
spreadsheet_range = 'A2:B12'

gsheet_api = GSheet('subject_email@test.com')
result = gsheet_api.read_gsheet(sheet_name, spreadsheet_id, spreadsheet_range)

for row in result['values']:
    print(row)
```

## 2.-  **get_sheetnames** (Method of a class):
Get the list of sheetnames given a spreadsheet id.


### Usage example

```python
from gc_google_services_api.gsheet import GSheet


spreadsheet_id = '11111111'

gsheet_api = GSheet('subject_email@test.com')
result = gsheet_api.get_sheetnames(spreadsheet_id)

for row in result['sheets']:
    print(row)
```

## Gmail
----------------------------------
Send emails with Gmail API.

This module needs to have configured an environment variable called `AUTHENTICATION_EMAIL` that will be the email used as sender.

### Usage example

```python
import os
from gc_google_services_api.gmail import Gmail


gmail_api = Gmail('subject-email@test.com')
gmail_api.send_email(
    'email message',
    'email title',
    ['to_email1@gmail.com'],
)
```

## Calendar
----------------------------------
Get calendars info and events.

This module needs to have configured an environment variable called `AUTHENTICATION_EMAIL` that will be the email used to authenticate with Google services.

### Usage example

```python
import os
from datetime import datetime, timedelta
from gc_google_services_api.calenda_api import Calendar


start_date = datetime.today()
end_date = datetime.today() + timedelta(days=1)
creator = 'test@test.com'

calendar_api = Calendar(start_date, end_date, creator)

# Getting calendar resources
resources = calendar_api.get_all_resources()
print(resources)

# Getting calendars
calendar_api.request_calendars()
print(calendar_api.calendars)

# Getting events from a calendar
calendar_id = '1'
calendar_api.request_calendar_events(calendar_id)
print(calendar_api.calendar_events)

# Delete calendar event
calendar_id = '1'
event_id = '2'
calendar_api.remove_event(calendar_id, event_id)
```

## Pub/Sub
This module allows us to send messages to a Pub/Sub topic, Subscribe to a Pub/Sub topic and execute a callback for each message and mark a message as finished so that Pub/Sub does not download it again

### Initializing the PubSub Instance
To use the PubSub class, you need to initialize an instance with the required credentials and project name:

* **credentials**: This would be the JSON of the service account used to authenticate with the Pub/Sub service
* **project_name**: It is the name of the project that appears in the Pub/Sub console

### Methods

* `send_message(topic_name, data)`
Sends a message to a specified Pub/Sub topic.

    * `topic_name` (str): Name of the Pub/Sub topic.
    * `data` (dict): Data to be sent as the message payload.

    Example
    ```python
    from gc_google_services_api.pubsub import PubSub


    pubsub_instance = PubSub(credentials, project_name)

    # To send a message into a Topic
    pubsub_instance.send_message("TOPIC_NAME", payload)
    ```


* `terminate_message(ack_id, message_id, subscription_path)`
Marks a message as processed and prevents it from being reprocessed.

    * `ack_id` (str): Acknowledgment ID of the message.
    * `message_id` (str): ID of the message.
    * `subscription_path` (str): Path to the Pub/Sub subscription.
    ```python
    from gc_google_services_api.pubsub import PubSub


    pubsub_instance = PubSub(credentials, project_name)

    ack_id = "1"
    message_id = "2"
    subscription_path = "your_subscription_path"

    pubsub_instance.terminate_message(ack_id, message_id, subscription_path)

    ```

* `subscribe_topic(topic_name, callback, max_simultaneous_messages=1, time_to_wait_between_messages=10, default_timeout_for_any_message=360)`
Subscribes to a Pub/Sub topic and continuously listens for new messages.

    * `topic_name` (str): Name of the Pub/Sub topic to subscribe to.
    callback (callable): Callback function to be executed for each received message.
    * `max_simultaneous_messages` (int): Maximum number of messages to process simultaneously.
    * `time_to_wait_between_messages` (int): Time (in seconds) to wait between processing each message.
    * `default_timeout_for_any_message` (int): Timeout (in seconds) for pulling any message from the subscription.

    Example
    ```python
    from gc_google_services_api.pubsub import PubSub



    def process_message(message_data):
        print("Received message:", message_data)

    pubsub_instance = PubSub(credentials, project_name)
    topic_name = "test_topic"

    pubsub_instance.subscribe_topic(
        topic_name,
        callback=process_message,
        max_simultaneous_messages=1,
        time_to_wait_between_messages=5,
        default_timeout_for_any_message=600
    )

    ```
