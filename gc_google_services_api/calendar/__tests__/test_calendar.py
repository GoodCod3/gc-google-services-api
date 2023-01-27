import unittest
from unittest.mock import Mock, patch, call
from datetime import datetime, timedelta

from gc_google_services_api.calendar import Calendar


class TestSuite(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_date = datetime.today()
        self.end_date = datetime.today() + timedelta(days=1)
        self.filterByCreator = 'test@test.com'

    def _create_build_mock(self, build):
        build.return_value = 'build_service'

        return build

    def _create_service_account_mock(self, service_account):
        service_account.Credentials.from_service_account_info.return_value = 'CREDENTIALS'  # noqa: E501

        return service_account

    @patch('gc_google_services_api.calendar.build')
    @patch('gc_google_services_api.auth.service_account')
    def test_calendar_constructor_should_initialize_authentication(self, service_account, build):  # noqa: E501
        self._create_build_mock(build)
        service_account = self._create_service_account_mock(service_account)

        Calendar(self.start_date, self.end_date, self.filterByCreator)

        service_account.Credentials.from_service_account_info.assert_has_calls(
            [
                call('',
                     scopes=[
                         'https://www.googleapis.com/auth/calendar.readonly',
                         'https://www.googleapis.com/auth/calendar.events'
                     ])
            ],
            [
                call('',
                     scopes=[
                         'https://www.googleapis.com/auth/admin.directory.resource.calendar',
                     ])
            ],
        )

        build.assert_has_calls(
            [
                call('calendar', 'v3', credentials='CREDENTIALS')
            ],
            [
                call('admin', 'directory_v1', credentials='CREDENTIALS')
            ]
        )
