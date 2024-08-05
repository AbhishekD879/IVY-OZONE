import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot wait until the event goes live
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28449_Verify_started_events_removing_from_the_Today_tab_Desktop(Common):
    """
    TR_ID: C28449
    NAME: Verify started events removing from the 'Today' tab: Desktop
    DESCRIPTION: This test case verifies started events removing from the 'Today' tab for Desktop
    DESCRIPTION: **Jira tickets:** BMA-4660
    PRECONDITIONS: 1) There should be events within 'Today' tab's view
    PRECONDITIONS: 2) To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        minutes = -4
        start_time = self.get_date_time_formatted_string(minutes=-minutes)
        for i in range(2):
            event = self.ob_config.add_autotest_premier_league_football_event(start_time=start_time)
        self.__class__.event_id = event.event_id
        self.__class__.event_name = event.ss_response['event']['name']
        self.__class__.section_name = event.ss_response['event']['className'].replace("Football ", "") + " - " + event.ss_response['event']['typeName']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches'->'Today' tab is opened by default (Desktop/tablet only)
        """
        self.site.header.sport_menu.items_as_ordered_dict[vec.football.FOOTBALL_TITLE.upper()].click()
        self.site.wait_content_state(state_name='FOOTBALL')
        self.assertTrue(self.site.sports_page.tabs_menu.items_as_ordered_dict['MATCHES'].is_selected())
        current_tab_name = self.site.football.tabs_menu.current
        matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                   self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, matches_tab_name,
                         msg=f'Current active tab: "{current_tab_name}", instead of "{matches_tab_name}"')

    def test_003_find_an_event_within_verified_page(self):
        """
        DESCRIPTION: Find an event within verified page
        EXPECTED: Event is displayed correctly with outcomes
        """
        league = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(self.section_name.upper())
        events = list(league.items_as_ordered_dict)
        self.assertIn(self.event_name, events,
                      msg=f'Expected event "{self.event_name}" is not found in list of existing events "{events}"')

    def test_004_triggerwait_until_for_verified_event_isstartedtrue_attribute_will_be_set_and_refresh_the_page(self):
        """
        DESCRIPTION: Trigger/wait until for verified event '**isStarted="true"**' attribute will be set and refresh the page
        EXPECTED: Started event is removed from 'Today' tab's view
        """
        self.ob_config.change_is_off_flag(event_id=self.event_id, is_off=True)
        self.device.refresh_page()
        league = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(self.section_name.upper())
        events = list(league.items_as_ordered_dict)
        self.assertNotIn(self.event_name, events,
                         msg=f'Expected event "{self.event_name}" is not found in list of existing events "{events}"')
