from apiclient import discovery
from google.oauth2 import service_account


API_NAME = 'sheets'
API_VERSION = 'v4'


class GSheet(object):
    def __init__(self, credentials_content, scopes, api_version=API_VERSION, api_name=API_NAME) -> None:
        self.credentials_content = credentials_content
        self.scopes = scopes
        self.api_version = api_version
        self.api_name = api_name

    def _set_credentials(self):
        return service_account.Credentials.from_service_account_info(
            self.credentials_content,
            scopes=self.scopes)

    def read_gsheet(self, sheet_name, spreadsheet_id, spreadsheet_range):
        service = discovery.build(
            self.api_name,
            self.api_version,
            credentials=self._set_credentials())

        return service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='{}!{}'.format(sheet_name, spreadsheet_range),
        ).execute()
