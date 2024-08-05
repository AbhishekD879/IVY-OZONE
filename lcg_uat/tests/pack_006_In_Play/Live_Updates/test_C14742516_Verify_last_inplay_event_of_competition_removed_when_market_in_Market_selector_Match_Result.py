import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from selenium.webdriver.support.ui import Select


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C14742516_Verify_last_inplay_event_of_competition_removed_when_market_in_Market_selector_Match_Result(BaseSportTest):
    """
    TR_ID: C14742516
    NAME: Verify last inplay event of competition removed when market in Market selector !=Match Result
    DESCRIPTION: This test case verifies that last inplay event of competition is removed from In-play page/tab when market in Market selector !=Match Result
    PRECONDITIONS: **TI (Backoffice) config:**
    PRECONDITIONS: * Several football inplay events should be configured in different competitions
    PRECONDITIONS: * 1 of competitions should have ONLY 1 event in it. This event should have other markets except Match Result, e.g: Both Teams To Score, Total Goals Over/Under 1.5. To Qualify. This event should be the only one with other markets
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to In-play page > 'Football' tab
    """
    keep_browser_open = True
    markets = [('to_qualify',),
               ('draw_no_bet', )]
    market_name = 'Draw No Bet'

    def inplay_event_check(self):
        result = False
        accordion = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.get(self.expected_market)
        if accordion is None:
            return result
        if not accordion.is_expanded():
            accordion.expand()
        events = list(accordion.items_as_ordered_dict.keys())
        for event in events:
            if self.__class__.inplay_team_1 in event and self.__class__.inplay_team_2 in event:
                result = True
                break
        return result

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and log in
        """
        self.__class__.expected_market = 'AUTO TEST - AUTOTEST PREMIER LEAGUE' if self.device_type == 'desktop' \
            else 'AUTOTEST PREMIER LEAGUE'
        self.__class__.sport_name = 'Football' if self.brand == 'bma' else 'FOOTBALL'
        self.__class__.in_play_event = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                                 perform_stream=True,
                                                                                                 markets=self.markets)
        self.__class__.inplay_event_id = self.in_play_event.event_id
        self.__class__.inplay_team_1 = self.in_play_event.team1
        self.__class__.inplay_team_2 = self.in_play_event.team2

        self.navigate_to_page('/in-play/football')
        if self.device_type == 'mobile':
            page_headers = list(self.site.inplay.tab_content.items_as_ordered_dict.keys())
            self.assertIn(vec.inplay.LIVE_NOW_EVENTS_SECTION, page_headers,
                          msg=f'No "{vec.inplay.LIVE_NOW_EVENTS_SECTION}" section is found on In-Play page')
            self.assertIn(vec.inplay.UPCOMING_EVENTS_SECTION, page_headers,
                          msg=f'No "{vec.inplay.UPCOMING_EVENTS_SECTION}" section is found on In-Play page')

    def test_001_select_any_other_market_in_market_selector_eg_total_goals_overunder_15(self):
        """
        DESCRIPTION: Select any other market in Market Selector (e.g 'Total Goals Over/Under 1.5')
        EXPECTED:
        """
        if self.device_type == 'desktop' and self.brand == 'bma':
            select = Select(self.site.football.tab_content.market_selector_element)
            select.select_by_visible_text(self.market_name)
        else:
            self.site.football.tab_content.dropdown_market_selector.select_value(self.market_name)

    def test_002_in_ti_undisplay_the_event_from_preconditions_this_event_should_be_the_only_one_with_other_markets(self):
        """
        DESCRIPTION: In TI undisplay the event from preconditions. (This event should be the only one with other markets)
        EXPECTED: * Event is removed from In Play page
        EXPECTED: * Default market becomes selected in Market selector
        EXPECTED: * Events containing default market are loaded
        EXPECTED: * Upcoming events (if there are any) remain displayed unchanged
        """
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
        sleep(5)
        result_inplay = self.inplay_event_check()
        self.assertFalse(result_inplay, msg='The inplay event is still visible on the page')
        if self.device_type == 'desktop' and self.brand == 'bma':
            select = Select(self.site.football.tab_content.market_selector_element)
            default_market = select.first_selected_option
        else:
            default_market = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertTrue(default_market, msg="Default market is not selected")

    def test_003__navigate_to_football_landing_page__in_play_tab_repeat_steps_1_2(self):
        """
        DESCRIPTION: * Navigate to Football Landing page > 'In-play' tab
        DESCRIPTION: * Repeat steps 1-2
        EXPECTED:
        """
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=True, active=True)
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(button_name=in_play_tab)
        if self.device_type == 'desktop' and self.brand == 'bma':
            select = Select(self.site.football.tab_content.market_selector_element)
            select.select_by_visible_text(self.market_name)
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
        sleep(5)
        result_inplay = self.inplay_event_check()
        self.assertFalse(result_inplay, msg='The inplay event is still visible on the page')
        if self.device_type == 'desktop' and self.brand == 'bma':
            select = Select(self.site.football.tab_content.market_selector_element)
            default_market = select.first_selected_option
        elif self.device_type == 'desktop' and self.brand == 'ladbrokes':
            default_market = self.site.inplay.tab_content.dropdown_market_selector.selected_market_selector_item
        else:
            default_market = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertTrue(default_market, msg="Default market is not selected")
