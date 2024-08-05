import pytest
import tests_ios_fully_native_regression as tests
from tests_ios_fully_native_regression.common import Common


@pytest.mark.ios
class Test_CRLAT_Libraries(Common):
    """
    NAME: Test CRLAT Libraries
    DESCRIPTION: This test case verifies CRLAT libraries work
    """

    def test_001_verify_libraries(self):
        """
        Home Page
        """
        self.assertTrue(self.get_initial_data_system_configuration(), msg='Can not get Initial Data from CMS')
        if tests.settings.backend_env == 'tst2':
            event_id = self.ob_config.add_autotest_premier_league_football_event().event_id
            event_data = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
            self.assertTrue(event_data, msg=f'Can not get event info with id {event_id} from SiteServe')

        event_id = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]['event']['id']
        event_data = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        self.assertTrue(event_data, msg=f'Can not get event info with id {event_id} from SiteServe')
