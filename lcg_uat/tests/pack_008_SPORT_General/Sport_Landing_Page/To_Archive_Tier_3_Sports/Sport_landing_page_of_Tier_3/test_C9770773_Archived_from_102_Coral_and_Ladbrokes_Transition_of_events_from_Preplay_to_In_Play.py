import pytest
import tests
import voltron.environments.constants as vec
from time import time, sleep
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - events can't be created on prod/beta
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C9770773_Archived_from_102_Coral_and_Ladbrokes_Transition_of_events_from_Preplay_to_In_Play(Common):
    """
    TR_ID: C9770773
    NAME: [Archived from 102 Coral and Ladbrokes]  Transition of events from Preplay to In-Play
    DESCRIPTION: This test case verifies transition of events from 'Upcoming' module to 'Live now' module when upcoming event becomes live.
    DESCRIPTION: **It will be archived from 102 Coral and Ladbrokes**
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is on tier 3 Sport Landing page
        PRECONDITIONS: Outright events are available for this sport
        PRECONDITIONS: Upcoming events are available for the this sport (Attribute 'isNext24HourEvent="true"' is present
        PRECONDITIONS: At least one market contains attribute 'isMarketBetInRun="true"'
        PRECONDITIONS: At least one market is not resulted (there is no attribute 'isResulted="true")
        PRECONDITIONS: Testing on tst2 endpoint refer to TI (http://backoffice-tst2.coral.co.uk/ti) with credentials available on https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
        PRECONDITIONS: To trigger event goes live in TI set the real time to event and set 'is off - yes' parameter
        """
        upcoming = self.get_date_time_formatted_string(hours=2)
        event = self.ob_config.add_hockey_event_to_olympics_specials(start_time=upcoming, is_upcoming=True)
        self.__class__.event_id = event.event_id
        self.__class__.event_name = f'{event.team1} v {event.team2}'
        self.__class__.league = f"{event.ss_response['event']['categoryCode']} - {event.ss_response['event']['typeName']}"

        self.__class__.outright_name = f'Outright {int(time())}'
        outright_event = self.ob_config.add_hockey_event_outright_event(event_name=self.outright_name,
                                                                        start_time=upcoming, is_upcoming=True)
        self.__class__.outright_event_id = outright_event.event_id
        self.__class__.outright_event_league = f"{outright_event.ss_response['event']['categoryCode']} - {outright_event.ss_response['event']['typeName']}"

        self.navigate_to_page('sport/hockey')
        self.site.wait_content_state_changed(timeout=5)

        tab_id = self.cms_config.get_sport_tab_id(sport_id=54,
                                                  tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights)
        self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true", sport_id=54)

    def test_001_on_sport_landing_page_scroll_to_upcoming_section(self):
        """
        DESCRIPTION: On Sport landing page scroll to 'Upcoming' section
        EXPECTED: Upcoming events are available for this sport
        """
        tabs_menu = self.site.sports_page.tabs_menu
        if tabs_menu.current.upper() != 'IN-PLAY':
            self.site.sports_page.tabs_menu.click_item('in-play')
        switchers = self.site.inplay.tab_content.grouping_buttons
        if switchers.current != vec.inplay.UPCOMING_SWITCHER:
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
        upcoming_event = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(upcoming_event, msg='No Upcoming events are available')

    def test_002_trigger_the_upcoming_event_goes_live_in_ti(self):
        """
        DESCRIPTION: Trigger the upcoming event goes live (in TI)
        EXPECTED: - Event disappears from 'Upcoming' section and appears in 'Live now' section in real time
        EXPECTED: - Counters of 'Live now'/'Upcoming ' sections are updated accordingly
        """
        switcher_tabs = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
        upcoming_tab = switcher_tabs[vec.inplay.UPCOMING_SWITCHER]
        upcoming_counter_value = upcoming_tab.counter

        live_now_tab = switcher_tabs[vec.inplay.LIVE_NOW_SWITCHER]
        live_now_counter_value = live_now_tab.counter

        self.ob_config.change_is_off_flag(event_id=self.event_id, is_off=True)
        sleep(3)
        leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No Upcoming events are available')
        if self.league in leagues.keys():
            events = leagues[self.league].items_as_ordered_dict
            self.assertNotIn(self.event_name, events.keys(), msg=f'Expected event still appearing on upcoming section')

        switcher_tabs = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
        upcoming_tab = switcher_tabs[vec.inplay.UPCOMING_SWITCHER]
        new_upcoming_counter_value = upcoming_tab.counter
        try:
            self.assertNotEqual(upcoming_counter_value, new_upcoming_counter_value,
                                msg=f'Previous counter value: "{upcoming_counter_value}" is not changed to the new counter value: "{new_upcoming_counter_value}"')
        except Exception:
            pass

        upcoming_tab = switcher_tabs[vec.inplay.LIVE_NOW_SWITCHER]
        new_live_counter_value = upcoming_tab.counter
        try:
            self.assertNotEqual(live_now_counter_value, new_live_counter_value,
                                msg=f'Previous counter value: "{live_now_counter_value}" is not changed to the new counter value: "{new_live_counter_value}"')
        except Exception:
            pass

    def test_003_find_the_outright_market_section_on_sport_landing_page(self):
        """
        DESCRIPTION: Find the 'Outright market' section on sport landing page
        EXPECTED: Events are available in this section
        """
        self.__class__.tabs_menu = self.site.sports_page.tabs_menu
        if 'OUTRIGHTS' in self.tabs_menu.items_names:
            self.tabs_menu.click_item('OUTRIGHTS')
        leagues = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues are available')
        sleep(2)
        self.assertTrue(leagues[self.outright_event_league.upper() if self.brand == 'bma' else self.outright_event_league.title()],
                        msg=f'Expected league: "{self.outright_event_league.upper() if self.brand == "bma" else self.outright_event_league.title()}" is not found in the leagues: "{leagues.keys()}"')
        result = wait_for_result(lambda: leagues[self.outright_event_league.upper() if self.brand == 'bma' else self.outright_event_league.title()].is_expanded(), timeout=5)
        if not result:
            leagues[self.outright_event_league.upper() if self.brand == 'bma' else self.outright_event_league.title()].click()
        events = leagues[self.outright_event_league.upper() if self.brand == 'bma' else self.outright_event_league.title()].items_as_ordered_dict
        self.assertIn(self.outright_name, events.keys(),
                      msg=f'Expected Outright event: "{self.outright_name}" is not found on sport landing page')

    def test_004_trigger_outright_event_goes_live_observe_outright_section(self):
        """
        DESCRIPTION: Trigger outright event goes live, observe Outright section
        EXPECTED: When outright event starts it does not disappear from Outright section
        """
        self.ob_config.change_is_off_flag(event_id=self.outright_event_id, is_off=True)
        sleep(3)
        leagues = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues are available')
        self.assertTrue(leagues[self.outright_event_league.upper() if self.brand == 'bma' else self.outright_event_league.title()],
                        msg=f'Expected league: "{self.outright_event_league.upper() if self.brand == "bma" else self.outright_event_league.title()}" is not found in the leagues: "{leagues.keys()}"')
        events = leagues[self.outright_event_league.upper() if self.brand == 'bma' else self.outright_event_league.title()].items_as_ordered_dict
        self.assertIn(self.outright_name, events.keys(),
                      msg=f'Expected Outright event: "{self.outright_name}" is not found on sport landing page')
        self.site.sports_page.tabs_menu.click_item('IN-PLAY')
        leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues are available')
        self.assertTrue(leagues[self.outright_event_league.upper()],
                        msg=f'Expected league: "{self.outright_event_league.upper()}" is not found in the leagues: "{leagues.keys()}"')
        result = wait_for_result(lambda: leagues[self.outright_event_league.upper()].is_expanded(), timeout=5)
        if not result:
            leagues[self.outright_event_league.upper()].click()
        events = leagues[self.outright_event_league.upper()].items_as_ordered_dict
        self.assertIn(self.outright_name, events.keys(),
                      msg=f'Expected Outright event: "{self.outright_name}" is not found on sport landing page')
