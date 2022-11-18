import unittest
from unittest.mock import Mock, patch

from gc_google_services_api.gsheet import GSheet, API_NAME, API_VERSION


class TestSuite(unittest.TestCase):
    def _create_discovery_mock(self, discovery):
        service_mock = Mock()
        values_mock = Mock()
        get_mock = Mock()
        execute_mock = Mock()

        execute_mock.execute.return_value = 'RESULT'
        get_mock.get.return_value = execute_mock
        values_mock.values.return_value = get_mock
        values_mock.get.return_value = execute_mock

        service_mock.spreadsheets.return_value = values_mock

        discovery.build.return_value = service_mock

        return discovery

    def _create_service_account_mock(self, service_account):
        service_account.Credentials.from_service_account_info.return_value = 'CREDENTIALS_TEST'

        return service_account

    @patch('gc_google_services_api.gsheet.discovery')
    @patch('gc_google_services_api.gsheet.service_account')
    def test_read_gsheet_should_call_google_api_with_credentials_and_correct_params(self, service_account, discovery):
        discovery = self._create_discovery_mock(discovery)
        service_account = self._create_service_account_mock(service_account)

        expected_result = 'RESULT'
        credentials_content = 'CREDENTIALS_CONTENT_TEST'
        credentials = 'CREDENTIALS_TEST'
        scope = ['SCOPE_TEST_1']
        sheet_name = 'SHEET_NAME_TEST'
        spreadsheet_id = 'SPREADSHEET_ID_TEST'
        spreadsheet_range = 'SPREADSHEET_RANGE_TEST'

        response = GSheet(credentials_content, scope).read_gsheet(
            sheet_name, spreadsheet_id, spreadsheet_range)

        self.assertEqual(response, expected_result)

        service_account.Credentials.from_service_account_info.assert_called_once_with(
            credentials_content,
            scopes=scope)

        discovery.build.assert_called_once_with(
            API_NAME,
            API_VERSION,
            credentials=credentials)

        discovery.build().spreadsheets().values().get.assert_called_once_with(
            spreadsheetId=spreadsheet_id,
            range='SHEET_NAME_TEST!SPREADSHEET_RANGE_TEST')
        
        discovery.build().spreadsheets().values().get().execute.assert_called_once()

    @patch('gc_google_services_api.gsheet.discovery')
    @patch('gc_google_services_api.gsheet.service_account')
    def test_get_sheetnames_should_call_google_api_with_credentials_and_correct_params(self, service_account, discovery):
        discovery = self._create_discovery_mock(discovery)
        service_account = self._create_service_account_mock(service_account)

        expected_result = 'RESULT'
        credentials_content = 'CREDENTIALS_CONTENT_TEST'
        credentials = 'CREDENTIALS_TEST'
        scope = ['SCOPE_TEST_1']
        spreadsheet_id = 'SPREADSHEET_ID_TEST'

        response = GSheet(credentials_content, scope)\
            .get_sheetnames(spreadsheet_id)

        self.assertEqual(response, expected_result)

        service_account.Credentials.from_service_account_info.assert_called_once_with(
            credentials_content,
            scopes=scope)

        discovery.build.assert_called_once_with(
            API_NAME,
            API_VERSION,
            credentials=credentials)

        discovery.build().spreadsheets().get.assert_called_once_with(
            spreadsheetId=spreadsheet_id)
        
        discovery.build().spreadsheets().get().execute.assert_called_once()
