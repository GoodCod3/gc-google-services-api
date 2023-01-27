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

    def _create_Auth_mock(self, Auth):
        auth_mock = Mock()
        auth_mock.get_credentials.return_value = 'CREDENTIALS'

        Auth.return_value = auth_mock

        return Auth

    def _create_build_mock(self, build):
        build.Credentials.from_service_account_info.return_value = 'CREDENTIALS'  # noqa: E501

        return build

    @patch('gc_google_services_api.calendar.Auth')
    @patch('gc_google_services_api.calendar.build')
    def test_calendar_constructor_should_initialize_authentication(self, build, Auth):  # noqa: E501
        Auth = self._create_Auth_mock(Auth)
        build = self._create_build_mock(build)

        Calendar(self.start_date, self.end_date, self.filterByCreator)

        Auth.assert_has_calls(
            [
                call([
                    'https://www.googleapis.com/auth/calendar.readonly',
                    'https://www.googleapis.com/auth/calendar.events'
                ], '')
            ],
            [
                call([
                    'https://www.googleapis.com/auth/admin.directory.resource.calendar',  # noqa: E501
                ], '')
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
