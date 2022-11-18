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
import os
from gc_google_services_api.gsheet import GSheet


credentials_content = os.getenv('SERVICE_ACCOUNT_JSON')
scope = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
]
sheet_name = 'Sheet 1'
spreadsheet_id = '11111111'
spreadsheet_range = 'A2:B12'

gsheet_api = GSheet(credentials_content, scope)
result = gsheet_api.read_gsheet(sheet_name, spreadsheet_id, spreadsheet_range)

for row in result['values']:
    print(row)
```

## 2.-  **get_sheetnames** (Method of a class):
Get the list of sheetnames given a spreadsheet id.


### Usage example

```python
import os
from gc_google_services_api.gsheet import GSheet


credentials_content = os.getenv('SERVICE_ACCOUNT_JSON')
scope = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
]
sheet_name = 'Sheet 1'
spreadsheet_id = '11111111'
spreadsheet_range = 'A2:B12'

gsheet_api = GSheet(credentials_content, scope)
result = gsheet_api.get_sheetnames(spreadsheet_id)

for row in result['sheets']:
    print(row)
```