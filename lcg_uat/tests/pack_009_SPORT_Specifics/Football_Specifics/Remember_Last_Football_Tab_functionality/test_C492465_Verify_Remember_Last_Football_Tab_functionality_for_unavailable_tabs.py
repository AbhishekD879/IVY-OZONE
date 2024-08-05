import pytest
import time
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C492465_Verify_Remember_Last_Football_Tab_functionality_for_unavailable_tabs(BaseSportTest):
    """
    TR_ID: C492465
    NAME: Verify Remember Last Football Tab functionality for unavailable tabs
    """
    keep_browser_open = True
    events_ids = []

    def make_special_events_suspended(self):
        s = SiteServeRequests(env=tests.settings.backend_env,
                              class_id=self.ob_config.backend.ti.football.autotest_class.class_id,
                              category_id=self.ob_config.backend.ti.football.category_id,
                              brand=self.brand)
        classes_dict = s.ss_class()
        classes = [class_['class']['id'] for class_ in classes_dict]
        self.assertTrue(classes, msg='No classes ids found for category')
        specials_filter = self.ss_query_builder \
            .add_filter(exists_filter(LEVELS.EVENT,
                                      simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.INTERSECTS,
                                                    'MKTFLAG_SP')))
        events = s.ss_event_to_outcome_for_class(class_id=classes, query_builder=specials_filter)

        if events:
            events_ids = [event['event']['id'] for event in events]
            self.assertTrue(events_ids,
                            msg=f'No events\' ids found, however found %s events: %s' % (len(events), events))
            for event in events_ids:
                self.ob_config.change_event_state(event_id=event, displayed=False, active=False)
            self.__class__.events_ids = events_ids

            timeout = 15 if tests.settings.backend_env == 'tst2' else 50
            result = wait_for_result(
                lambda: s.ss_event_to_outcome_for_class(class_id=classes, query_builder=specials_filter),
                name='Specials events disappear from SiteServe',
                expected_result=False,
                timeout=timeout)
            self.assertFalse(result, msg='Specials events still present after suspending')

    def wait_special_tab_appearance(self, appear: bool, timeout: int = 140) -> bool:
        tabs_menu = self.site.football.tabs_menu
        tabs = tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='Tabs are empty')
        result = self.expected_sport_tabs.specials in tabs.keys()
        if result if not appear else not result:
            if not appear:
                self.make_special_events_suspended()
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline and result if not appear else not result:
                self.device.refresh_page()
                self.site.wait_splash_to_hide()
                self.site.wait_content_state(state_name='Football')
                tabs_menu = self.site.football.tabs_menu
                tabs = tabs_menu.items_as_ordered_dict
                self.assertTrue(tabs, msg='Tabs are empty')
                result = self.expected_sport_tabs.specials in tabs.keys()
                time.sleep(1)
        return result

    @classmethod
    def custom_tearDown(cls, **kwargs):
        ob_config = cls.get_ob_config()
        for event in cls.events_ids:
            ob_config.change_event_state(event_id=event, displayed=True, active=True)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check if there are any Football Specials events available
        EXPECTED: Continue test and add Special event if there are no Football Specials events
        EXPECTED: Suspend active Football Specials events till the end of test if Football Specials events are present
        """
        self.make_special_events_suspended()

        self.__class__.eventID = self.ob_config.add_autotest_premier_league_football_event(suspend_at=self.get_date_time_formatted_string(days=2), special=True).event_id

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application and login
        EXPECTED: Homepage is loaded
        EXPECTED: User is logged in
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.site.close_all_dialogs()

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: Matches tab is selected by default and highlighted
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.assertEqual(self.site.football.tabs_menu.current, self.expected_sport_tabs.matches, msg='Matches tab is not active by default')

    def test_003_choose_specials_tab(self):
        """
        DESCRIPTION: Choose 'SPECIALS' tab
        EXPECTED: 'SPECIALS' tab is selected and highlighted
        EXPECTED: Appropriate content is  displayed on Specials page
        """
        self.wait_special_tab_appearance(True)
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.specials)
        self.verify_last_football_tab(tab=self.expected_sport_tabs.specials)

    def test_004_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        """
        self.navigate_to_page(name='home')
        self.site.wait_content_state('HomePage')

    def test_005_trigger_situation_that_tab_from_step_3_is_no_longer_available(self):
        """
        DESCRIPTION: Trigger situation that tab from step 3 is no longer available
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)

    def test_006_return_to_football_landing_page(self):
        """
        DESCRIPTION: Return to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: 'SPECIALS' tab is no longer available
        EXPECTED: 'MATCHES' tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for Matches tab
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        result = self.wait_special_tab_appearance(False)
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        tabs_menu = self.site.football.tabs_menu
        tabs = tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='Tabs are empty')
        self.assertFalse(result, msg=f'Unexpected tab "{self.expected_sport_tabs.specials}" was found in "{tabs.keys()}"')
        self.assertEqual(tabs_menu.current, self.expected_sport_tabs.matches,
                         msg=f'Active tab is "{tabs_menu.current}" but "{self.expected_sport_tabs.matches}" is expected to be active')
        self.verify_last_football_tab(tab=self.expected_sport_tabs.matches)

    def test_007_trigger_situation_that_tab_from_step_3_is_available_again(self):
        """
        DESCRIPTION: Trigger situation that tab from step 3 is available again
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

    def test_008_repeat_steps_1_3(self):
        """
        DESCRIPTION: Repeat steps 1-3
        EXPECTED: 'SPECIALS' tab is selected and highlighted
        EXPECTED: Appropriate content is displayed on Specials page
        """
        self.navigate_to_page(name='home')
        self.site.wait_content_state('HomePage')
        self.test_002_navigate_to_football_landing_page()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.test_003_choose_specials_tab()

    def test_009_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is successfully logged out
        """
        self.site.logout()

    def test_010_trigger_situation_that_tab_from_step_3_is_no_longer_available(self):
        """
        DESCRIPTION: Trigger situation that tab from step 3 is no longer available
        """
        self.test_005_trigger_situation_that_tab_from_step_3_is_no_longer_available()

    def test_011_log_into_app_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app and return to Football Landing page
        EXPECTED: User is successfully logged in
        EXPECTED: Football Landing page is opened
        EXPECTED: 'SPECIALS' tab is no longer available
        EXPECTED: 'MATCHES' tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for Matches tab
        """
        self.test_001_load_oxygen_application_and_login()
        self.test_006_return_to_football_landing_page()
