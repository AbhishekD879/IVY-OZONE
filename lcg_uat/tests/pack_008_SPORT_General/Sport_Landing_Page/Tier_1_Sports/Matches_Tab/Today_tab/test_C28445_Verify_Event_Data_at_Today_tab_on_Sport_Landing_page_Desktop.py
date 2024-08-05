import pytest
import tests
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
from voltron.environments import constants as vec


@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.smoke
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.sports
@pytest.mark.medium
@vtest
class Test_C28445_Verify_Event_Data_at_Today_tab_on_Sport_Landing_page_Desktop(BaseSportTest):
    """
    TR_ID: C28445
    VOL_ID: C24537653
    NAME: Verify Event Data at 'Today' tab on <Sport> Landing page: Desktop
    DESCRIPTION: This test case verifies event data at 'Today' tab on <Sport> Landing page for Desktop/tablet
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get odds headers from CMS
        DESCRIPTION: Create test event
        """
        if tests.settings.backend_env == 'prod':
            streaming_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.INTERSECTS, 'EVFLAG_PVM,EVFLAG_IVM')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=streaming_filter)
            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.eventID = events[0]['event']['id']
            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=events[0])
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(perform_stream=True)
            self.__class__.eventID = event.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'*** Event name: "{self.event_name}"')
            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self._logger.info(f'*** Using event "{self.event_name}" with id "{self.eventID}" from section "{self.section_name}"')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page
        EXPECTED: <Sport> Landing Page is opened
        EXPECTED: 'Matches' tab is opened by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is "{current_tab_name}", instead of "{expected_tab_name}"')

    def test_003_verify_event_name(self):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *  Event name corresponds to **name** attribute
        EXPECTED: *  Event name is displayed in the following format:
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        EXPECTED: **For Desktop:**
        EXPECTED: <Team1/Player1> v <Team2/Player2>
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)

        self.assertEqual(self.event_name, self.event.event_name,
                         msg=f'Expected event name: "{self.event_name}" '
                             f'is not equal to actual: "{self.event.event_name}"')

    def test_004_verify_favourite_icon(self):
        """
        DESCRIPTION: Verify 'Favourite' icon
        EXPECTED: 'Favourite' icon is displayed on the left side, before event name
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled, self.event.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}" for "{self.event_name}" event')

    def test_005_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start Time
        EXPECTED: *   Event start time corresponds to **startTime** attribute
        EXPECTED: *   Event Start Time is shown below event name
        EXPECTED: *   For events that occur Today date format is 24 hours:
        EXPECTED: **HH:MM, Today** (e.g. "14:00 or 05:00, Today")
        """
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_time_resp = event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.event_card_today_time_format_pattern,
                                                               ss_data=True
                                                               )

        self.assertEqual(event_time_resp_converted, self.event.event_time,
                         msg=f'Expected event time: "{event_time_resp_converted}" '
                             f'is not equal to actual: "{self.event.event_time}"')

    def test_006_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: * EVFLAG_AVA / EVFLAG_IVM / EVFLAG_PVM / EVFLAG_RVA / EVFLAG_RPM / EVFLAG_GVM
        EXPECTED: * 'Watch live' icon/text is displayed next to event start time
        EXPECTED: * 'Watch live' icon and text are displayed for mobile/tablet, icon only is shown for desktop
        """
        self.assertTrue(self.event.has_stream_icon(), msg='"Watch Live" icon is not found')

        expected_label = vec.sb.WATCH.upper() if self.brand == 'ladbrokes' else vec.sb.WATCH_LIVE_LABEL.title()
        self.assertEqual(expected_label, self.event.watch_live_label,
                         msg=f'Expected label name: "{expected_label}" '
                             f'is not equal to actual: "{self.event.watch_live_label}"')

    def test_007_click_anywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section (except 'Price/Odds' button)
        EXPECTED: Event Details Page is opened
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
