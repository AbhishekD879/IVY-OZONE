import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot switch upcoming event to inplay
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.in_play
@pytest.mark.medium
@vtest
class Test_C9770767_Transition_of_events_from_Preplay_to_In_Play(Common):
    """
    TR_ID: C9770767
    NAME: Transition of events from Preplay to In-Play
    DESCRIPTION: This test case verifies transition of events from 'Upcoming' module to 'Live now' module when upcoming event becomes live.
    PRECONDITIONS: User is on Sport Landing page
    PRECONDITIONS: Upcoming events are available for the this sport (Attribute 'isNext24HourEvent="true"' is present
    PRECONDITIONS: At least one market contains attribute 'isMarketBetInRun="true"'
    PRECONDITIONS: At least one market is not resulted (there is no attribute 'isResulted="true")
    PRECONDITIONS: Testing on tst2 endpoint refer to TI (http://backoffice-tst2.coral.co.uk/ti) with credentials available on https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: To trigger event goes live in TI set the real time to event and set 'is off - yes' parameter
    """
    keep_browser_open = True

    def change_market(self):
        actual = self.site.inplay.tab_content.selected_market
        markets = self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict
        for market_name, market in markets.items():
            if market_name != actual:
                market_dropdown = self.site.football.tab_content.dropdown_market_selector
                dropdown = market_dropdown.is_expanded()
                if not dropdown:
                    market_dropdown = self.site.football.tab_content.dropdown_market_selector
                market_dropdown.click_item(market_name)
                break

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True)
        self.__class__.event_id = event.event_id
        self.__class__.event_name = event.ss_response['event']['name']
        self.__class__.section_name = event.ss_response['event']['typeName']

    def test_001_on_sport_landing_page_navigate_to_in_play_tab(self):
        """
        DESCRIPTION: On Sport landing page navigate to In-Play tab
        EXPECTED: In-Play tab content loads with
        EXPECTED: - Live now section
        EXPECTED: - Upcoming section
        """
        self.site.wait_content_state('Homepage')
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(state_name='FOOTBALL')
        sleep(1)
        self.site.sports_page.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
        live_now_sections_name = self.site.inplay.tab_content.live_now.name
        self.assertEqual(live_now_sections_name, vec.inplay.LIVE_NOW_EVENTS_SECTION,
                         msg=f"{vec.inplay.LIVE_NOW_EVENTS_SECTION} is not loaded, actual '{live_now_sections_name}'")
        upcoming_sections_name = self.site.inplay.tab_content.upcoming.name
        self.assertEqual(upcoming_sections_name, vec.inplay.UPCOMING_EVENTS_SECTION,
                         msg=f"{vec.inplay.UPCOMING_EVENTS_SECTION} is not loaded, actual '{upcoming_sections_name}'")

    def test_002_scroll_down_to_upcoming_section_trigger_the_event_goes_live_in_ti(self, switch_market=False):
        """
        DESCRIPTION: Scroll down to Upcoming section, trigger the event goes live in TI
        EXPECTED: - Event disappears from Upcoming section and appears in Live now section in real time
        EXPECTED: - Counters of 'Live now'/'Upcoming' sections are updated accordingly
        """
        league = self.site.inplay.tab_content.upcoming.items_as_ordered_dict.get(self.section_name.upper())
        if not league.is_expanded():
            league.expand()
        events = list(league.items_as_ordered_dict)
        self.assertIn(self.event_name, events,
                      msg=f'Expected event "{self.event_name}" is not found in list of existing events "{events}"')
        live_now_counter = self.site.inplay.tab_content.live_now_counter
        upcoming_counter = self.site.inplay.tab_content.upcoming_counter
        self.ob_config.change_is_off_flag(event_id=self.event_id, is_off=True)
        sleep(1)
        self.device.refresh_page()
        self.site.sports_page.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
        if switch_market:
            self.change_market()
        updated_live_now_counter = self.site.inplay.tab_content.live_now_counter
        updated_upcoming_counter = self.site.inplay.tab_content.upcoming_counter
        self.assertEqual(updated_live_now_counter, live_now_counter + 1,
                         msg='"Live Now counter" is not increased by 1 on switching the upcoming event to the inplay event')
        self.assertEqual(updated_upcoming_counter, upcoming_counter - 1,
                         msg='"Upcoming counter" is not decreased by 1 on switching the upcoming event to the inplay event')

    def test_003_change_market_in_market_selector_football_only_to_any_other_available(self):
        """
        DESCRIPTION: Change market in Market selector (football only) to any other available
        EXPECTED: Available events are displayed
        """
        self.test_000_preconditions()
        self.change_market()

    def test_004_trigger_event_transition_from_preplay_to_inplay(self):
        """
        DESCRIPTION: Trigger event transition from preplay to inplay
        EXPECTED: - Event disappears from upcoming section and appears in live now
        EXPECTED: - Counters of 'Live now'/'Upcoming' sections are updated accordingly
        """
        self.test_002_scroll_down_to_upcoming_section_trigger_the_event_goes_live_in_ti(switch_market=True)
